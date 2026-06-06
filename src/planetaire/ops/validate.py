"""Font validation: check glyph coverage, metrics, and features."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from fontTools.ttLib import TTFont


@dataclass
class Issue:
    """A validation issue found in a font."""

    severity: Literal["error", "warning", "info"]
    category: str
    message: str
    details: dict[str, object] | None = None


def validate_font(
    font: TTFont,
    *,
    expected_ranges: list[tuple[int, int]] | None = None,
    expected_weight: int | None = None,
    expected_features: list[str] | None = None,
    expect_monospace: bool = True,
) -> list[Issue]:
    """
    Validate font against expected properties.

    Returns a list of issues found. Empty list means the font passes all checks.
    """
    issues: list[Issue] = []

    # Basic sanity
    glyph_count = len(font.getGlyphOrder())
    if glyph_count == 0:
        issues.append(Issue("error", "sanity", "Font has no glyphs"))

    upm = font["head"].unitsPerEm
    if upm <= 0 or upm > 16384:
        issues.append(Issue("error", "sanity", f"Unusual UPM value: {upm}"))

    # Monospace invariant: every non-zero glyph shares one advance width, and
    # no text/coding glyph's ink bleeds past the cell.
    if expect_monospace:
        issues.extend(_check_monospace_invariant(font))

    # Weight class
    if expected_weight is not None and "OS/2" in font:
        actual_weight = font["OS/2"].usWeightClass
        if actual_weight != expected_weight:
            issues.append(
                Issue(
                    "error",
                    "metrics",
                    f"Weight mismatch: expected {expected_weight}, got {actual_weight}",
                )
            )

    # Glyph coverage
    if expected_ranges:
        from planetaire.unicode_ranges import codepoints_in_ranges

        expected_cps = codepoints_in_ranges(expected_ranges)
        cmap = font.getBestCmap() or {}
        missing = expected_cps - set(cmap.keys())
        if missing:
            sample = sorted(missing)[:10]
            sample_str = ", ".join(f"U+{cp:04X}" for cp in sample)
            issues.append(
                Issue(
                    "error",
                    "glyph_coverage",
                    f"Missing {len(missing)} glyph(s): {sample_str}{'...' if len(missing) > 10 else ''}",
                    details={"missing_count": len(missing), "sample": sample},
                )
            )

    # GSUB features
    if expected_features:
        actual_features: set[str] = set()
        if "GSUB" in font and font["GSUB"].table.FeatureList:
            for rec in font["GSUB"].table.FeatureList.FeatureRecord:
                actual_features.add(rec.FeatureTag)
        missing_features = set(expected_features) - actual_features
        if missing_features:
            issues.append(
                Issue(
                    "warning",
                    "features",
                    f"Missing GSUB features: {', '.join(sorted(missing_features))}",
                )
            )

    # Name table consistency
    name_table = font["name"]
    family = name_table.getName(1, 3, 1, 0x0409)
    if family is None:
        issues.append(Issue("warning", "naming", "Missing name ID 1 (family name)"))

    # Style-linking consistency (italic/bold bits vs subfamily name)
    issues.extend(_check_style_linking(font))

    return issues


def _check_monospace_invariant(font: TTFont) -> list[Issue]:
    """Check the single-advance-width invariant and ink-within-cell."""
    from planetaire.ops.monospace import check_monospace

    issues: list[Issue] = []
    if "glyf" not in font or "hmtx" not in font:
        return issues
    report = check_monospace(font)
    if report.nonuniform:
        from collections import Counter

        widths = Counter(aw for _, aw in report.nonuniform)
        sample = ", ".join(f"{n}={aw}" for n, aw in report.nonuniform[:6])
        issues.append(
            Issue(
                "error",
                "monospace",
                f"{len(report.nonuniform)} glyph(s) deviate from cell width "
                f"{report.cell_width} (widths {dict(sorted(widths.items()))}): {sample}"
                f"{'...' if len(report.nonuniform) > 6 else ''}",
                details={"cell_width": report.cell_width, "count": len(report.nonuniform)},
            )
        )
    if report.bleed:
        sample = ", ".join(f"{n}[{x0},{x1}]" for n, _, x0, x1 in report.bleed[:6])
        issues.append(
            Issue(
                "warning",
                "monospace",
                f"{len(report.bleed)} text glyph(s) bleed past cell "
                f"[0,{report.cell_width}]: {sample}{'...' if len(report.bleed) > 6 else ''}",
                details={"count": len(report.bleed)},
            )
        )
    return issues


def _name_str(name_table: object, name_id: int) -> str:
    """Read a name record (Windows then Mac), returning "" if absent."""
    record = name_table.getName(name_id, 3, 1, 0x0409)  # pyright: ignore
    if record is None:
        record = name_table.getName(name_id, 1, 0, 0)  # pyright: ignore
    return str(record) if record else ""


def _check_style_linking(font: TTFont) -> list[Issue]:
    """Verify italic/bold flags agree across head.macStyle, OS/2.fsSelection, and name.

    These three must tell the same story or apps disagree about which face is which.
    Returns errors for contradictions and a warning if the REGULAR bit is unset on a
    regular-style face.
    """
    issues: list[Issue] = []
    if "head" not in font or "OS/2" not in font or "name" not in font:
        return issues

    subfamily = _name_str(font["name"], 17) or _name_str(font["name"], 2)
    if not subfamily:
        return issues
    sub_l = subfamily.lower()
    name_italic = "italic" in sub_l or "oblique" in sub_l
    name_bold = "bold" in sub_l

    mac_style = font["head"].macStyle
    fs_selection = font["OS/2"].fsSelection
    mac_italic = bool(mac_style & 0x02)
    mac_bold = bool(mac_style & 0x01)
    os2_italic = bool(fs_selection & 0x01)
    os2_bold = bool(fs_selection & 0x20)
    os2_regular = bool(fs_selection & 0x40)

    if mac_italic != os2_italic:
        issues.append(
            Issue(
                "error",
                "style_linking",
                f"Italic flag mismatch: head.macStyle italic={mac_italic}, "
                f"OS/2.fsSelection italic={os2_italic}",
            )
        )
    if name_italic != mac_italic:
        issues.append(
            Issue(
                "error",
                "style_linking",
                f"Italic flags ({mac_italic}) do not match subfamily '{subfamily}'",
            )
        )
    if mac_bold != os2_bold:
        issues.append(
            Issue(
                "error",
                "style_linking",
                f"Bold flag mismatch: head.macStyle bold={mac_bold}, "
                f"OS/2.fsSelection bold={os2_bold}",
            )
        )
    if name_bold != mac_bold:
        issues.append(
            Issue(
                "error",
                "style_linking",
                f"Bold flags ({mac_bold}) do not match subfamily '{subfamily}'",
            )
        )
    if not name_bold and not name_italic and not os2_regular:
        issues.append(
            Issue(
                "warning",
                "style_linking",
                "OS/2.fsSelection REGULAR bit not set for a regular-style face",
            )
        )

    return issues
