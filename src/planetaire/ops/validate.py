"""Font validation — check glyph coverage, metrics, and features."""

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

    return issues
