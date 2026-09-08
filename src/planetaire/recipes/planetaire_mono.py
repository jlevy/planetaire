"""
Full Planetaire Mono build pipeline.

Composes ops/ functions to produce all Planetaire Mono font variants
from B612 and Hack source fonts.

B612 source: original polarsys/b612. ExtraBold variants are generated
from Bold via FontForge emboldening if not already present.
"""

from __future__ import annotations

import logging
import shutil
from collections.abc import Callable
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path

from fontTools.ttLib import TTFont

from planetaire.config import (
    FAMILY_NAME,
    PLANETAIRE_GSUB_FEATURES,
    PLANETAIRE_LETTER_RANGES,
    TEXT_FAMILY_NAME,
    TEXT_SLIM_WEB_ITALIC_VARIANTS,
    TEXT_SLIM_WEB_SUBSETS,
    TEXT_SLIM_WEB_VARIANTS,
    TEXT_SUBSET_GROUPS,
    TEXT_SUBSET_RANGES,
    TEXT_WEB_CSS_NAME,
    VARIANTS,
    TextSubsetDef,
    VariantDef,
    font_stack_css_var,
)
from planetaire.ops.fix import fix_font
from planetaire.ops.merge import (
    WinBox,
    apply_win_box,
    derive_os2_metrics,
    font_win_box,
    merge_glyphs,
)
from planetaire.ops.monospace import normalize_monospace, set_fixed_pitch_flags
from planetaire.ops.rename import rename_font
from planetaire.ops.subset import save_web_font, subset_font
from planetaire.ops.validate import Issue, validate_font
from planetaire.ops.zero import add_dotted_zero
from planetaire.version import get_version, to_font_version

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class FontFaceEntry:
    """One generated @font-face block."""

    stem: str
    weight: int
    is_italic: bool
    unicode_range: str | None = None


@dataclass(frozen=True)
class FontFallbackMetrics:
    """CSS metric overrides measured from a generated font."""

    size_adjust: float
    ascent_override: float
    descent_override: float
    line_gap_override: float


def resolve_font_version(version: str | None) -> str:
    """Return the version to stamp into the fonts, explicit input taking precedence.

    Without an argument this is the canonical version, which comes from the latest
    reachable git tag. That is right for every build except the one that matters
    most: a release builds its artifacts *before* `scripts/release.py finalize`
    creates the tag, so resolving there stamps the previous release into name ID 5
    and `head.fontRevision`, and the committed `fonts/web/` then disagrees with a
    rebuild at the tagged commit. The release passes the version explicitly for the
    same reason the specimen already does (plt-0204).
    """
    font_version = to_font_version(version) if version else to_font_version(get_version())
    if version:
        log.info("Stamping explicitly requested version %s", font_version)
    return font_version


# Mapping from ExtraBold variants to their Bold source for emboldening.
_EXTRABOLD_FROM_BOLD: dict[str, str] = {
    "B612Mono-ExtraBold.ttf": "B612Mono-Bold.ttf",
    "B612Mono-ExtraBoldItalic.ttf": "B612Mono-BoldItalic.ttf",
}

# Mapping for intermediate weight generation from Regular sources.
# (target_file, source_file, target_weight, change_amount, max_points)
# max_points caps which glyphs are emboldened: glyphs denser than the cap keep
# their source outline. A few dozen ultra-dense Nerd Font logo icons (up to
# ~4,700 points) would otherwise dominate runtime, since changeWeight's
# self-intersection removal is pathologically slow on them (a full-font pass ran
# 2+ hours). The cap keeps generation to minutes with no visible difference; see
# TODO.md (plt-ddjw) to revisit full fidelity. B612 has no glyph near the cap, so
# it is unaffected there; only Hack's icons are. Hack Medium and SemiBold use
# the cap; otherwise a clean regeneration stalls in the dense Nerd Font logos.
_INTERMEDIATE_WEIGHTS: list[tuple[str, str, int, int, int | None]] = [
    ("B612Mono-Medium.ttf", "B612Mono-Regular.ttf", 500, 40, None),
    ("B612Mono-MediumItalic.ttf", "B612Mono-Italic.ttf", 500, 40, None),
    ("B612Mono-SemiBold.ttf", "B612Mono-Regular.ttf", 600, 75, 500),
    ("B612Mono-SemiBoldItalic.ttf", "B612Mono-Italic.ttf", 600, 75, 500),
    ("HackNerdFont-Medium.ttf", "HackNerdFont-Regular.ttf", 500, 40, 500),
    ("HackNerdFont-MediumItalic.ttf", "HackNerdFont-Italic.ttf", 500, 40, 500),
    ("HackNerdFont-SemiBold.ttf", "HackNerdFont-Regular.ttf", 600, 75, 500),
    ("HackNerdFont-SemiBoldItalic.ttf", "HackNerdFont-Italic.ttf", 600, 75, 500),
]


def _ensure_generated_weights(source_dir: Path) -> None:
    """Generate intermediate and ExtraBold weight variants if not already present.

    Uses FontForge emboldening (changeWeight). If FontForge is not
    installed, logs a warning. Pre-generated files must exist in
    the source directory.
    """
    from planetaire.ops.embolden import embolden_font

    # Generate intermediate weights (Medium, SemiBold) for both B612 and Hack.
    for target_file, source_file, target_weight, change_amount, max_points in _INTERMEDIATE_WEIGHTS:
        # Determine which subdirectory based on filename prefix.
        subdir = "b612" if target_file.startswith("B612") else "hack"
        font_dir = source_dir / subdir
        target_path = font_dir / target_file
        source_path = font_dir / source_file

        if target_path.exists():
            continue

        if not source_path.exists():
            log.warning("Cannot generate %s: source %s not found", target_file, source_path)
            continue

        if shutil.which("fontforge") is None:
            log.warning(
                "Cannot generate %s: FontForge not installed. Place pre-generated files in %s",
                target_file,
                font_dir,
            )
            continue

        log.info("Generating %s from %s via FontForge emboldening", target_file, source_file)
        embolden_font(
            source_path,
            target_path,
            target_weight=target_weight,
            change_amount=change_amount,
            max_points=max_points,
        )

    # Generate ExtraBold B612 from Bold.
    b612_dir = source_dir / "b612"
    for extrabold_file, bold_file in _EXTRABOLD_FROM_BOLD.items():
        extrabold_path = b612_dir / extrabold_file
        bold_path = b612_dir / bold_file

        if extrabold_path.exists():
            continue

        if not bold_path.exists():
            log.warning("Cannot generate %s: Bold source %s not found", extrabold_file, bold_path)
            continue

        if shutil.which("fontforge") is None:
            log.warning(
                "Cannot generate %s: FontForge not installed. "
                "Place pre-generated ExtraBold files in %s",
                extrabold_file,
                b612_dir,
            )
            continue

        log.info("Generating %s from %s via FontForge emboldening", extrabold_file, bold_file)
        embolden_font(bold_path, extrabold_path, target_weight=800, change_amount=30)


def _process_variant(
    *,
    hack_path: Path,
    b612_path: Path,
    family: str,
    subfamily: str,
    weight: int,
    version: str,
) -> TTFont:
    """Build one fully-processed variant: merge, rename, dotted zero, fixes.

    Returns the in-memory font; subsetting and saving are the caller's job.
    """
    base = TTFont(hack_path)
    donor = TTFont(b612_path)

    merged = merge_glyphs(
        base,
        donor,
        PLANETAIRE_LETTER_RANGES,
        copy_gsub_features=PLANETAIRE_GSUB_FEATURES,
    )
    renamed = rename_font(
        merged,
        family=family,
        subfamily=subfamily,
        weight=weight,
        version=version,
    )
    dotted = add_dotted_zero(renamed)
    fixed = fix_font(dotted)
    # Enforce true monospace: B612 letters (1300) and FontForge-emboldened
    # Medium/SemiBold/ExtraBold letters (1360-1420) are pinned to the Hack base
    # cell, recentered, and condensed only where ink would otherwise bleed. Must
    # run after the dotted zero so the modified zero is normalized too.
    normalize_monospace(fixed)
    set_fixed_pitch_flags(fixed)
    # Last: the OS/2 measurement fields describe the outlines as finally drawn,
    # so they are derived once nothing will move a contour or an advance again.
    derive_os2_metrics(fixed)
    return fixed


def _resolve_variant_sources(
    source_dir: Path, variant: str | None
) -> list[tuple[VariantDef, Path, Path]]:
    """Resolve (variant, hack_path, b612_path) for buildable variants."""
    variants_to_build = (
        VARIANTS if variant is None else [v for v in VARIANTS if v["name"] == variant]
    )
    resolved: list[tuple[VariantDef, Path, Path]] = []
    for v in variants_to_build:
        hack_path = source_dir / "hack" / v["hack_file"]
        b612_path = source_dir / "b612" / v["b612_file"]
        if not hack_path.exists():
            log.warning("Skipping %s: Hack source not found at %s", v["name"], hack_path)
            continue
        if not b612_path.exists():
            log.warning("Skipping %s: B612 source not found at %s", v["name"], b612_path)
            continue
        resolved.append((v, hack_path, b612_path))
    return resolved


def _log_issues(label: str, issues: list[Issue]) -> None:
    """Log validation issues, keeping informational ones out of the warning stream."""
    for issue in issues:
        emit = log.warning if issue.severity in ("error", "warning") else log.info
        emit("Validation %s in %s: %s", issue.severity, label, issue.message)


def _process_family(
    source_dir: Path,
    variant: str | None,
    *,
    family: str,
    version: str,
    emit_names: set[str] | None = None,
    prepare: Callable[[TTFont], tuple[TTFont, TTFont]] | None = None,
) -> tuple[list[tuple[VariantDef, TTFont]], WinBox | None]:
    """Process a family's faces, returning the selected ones and the family's usWin box.

    The `usWin` clipping box has to be one box for the whole family (see
    `family_win_box` for why), which means it cannot be measured from whichever
    faces a single invocation happens to emit: building `--variant Regular` alone
    has to stamp the same box as building the family, or that one file disagrees
    with its siblings. So every face the sources can build is processed and
    measured here, and the ones not selected are dropped again — only what will
    actually be written stays in memory.

    `prepare` maps a processed face to `(the face whose ink defines the box, the
    face to emit)`. Text measures its box after dropping the Private-Use icons,
    and its split build still emits from the full merged face, because the script
    subsets keep a few glyphs the Text subset drops.
    """
    selected = {v["name"] for v, _, _ in _resolve_variant_sources(source_dir, variant)}
    if emit_names is not None:
        selected &= emit_names

    faces: list[tuple[VariantDef, TTFont]] = []
    win_box: WinBox | None = None
    measured_count = 0

    for v, hack_path, b612_path in _resolve_variant_sources(source_dir, None):
        name = v["name"]
        log.info("Building %s %s", family, name)
        font = _process_variant(
            hack_path=hack_path,
            b612_path=b612_path,
            family=family,
            subfamily=v["subfamily"],
            weight=v["weight"],
            version=version,
        )
        measured, emitted = prepare(font) if prepare is not None else (font, font)
        face_box = font_win_box(measured)
        if face_box is not None:
            win_box = face_box if win_box is None else win_box.enclosing(face_box)
            measured_count += 1
        if name in selected:
            faces.append((v, emitted))

    log.info("%s usWin box across %d face(s): %s", family, measured_count, win_box)
    return faces, win_box


def build_planetaire_mono(
    source_dir: Path,
    output_dir: Path,
    variant: str | None = None,
    *,
    formats: tuple[str, ...] = ("ttf", "woff2"),
    version: str | None = None,
) -> list[Path]:
    """
    Build Planetaire Mono font family.

    For each variant: load Hack as base, merge B612 letter glyphs,
    rename to "Planetaire Mono Extended", apply fixes, validate, and save.

    ExtraBold B612 variants are auto-generated from Bold via FontForge
    if not already present in source_dir.

    `version` stamps an explicit release version instead of resolving the canonical
    one; pass it when building the artifacts of a release whose tag does not exist
    yet (see `resolve_font_version`).

    Returns list of output font paths.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    font_version = resolve_font_version(version)
    log.info("Building Planetaire Mono version %s", font_version)

    # Generate intermediate (Medium) and ExtraBold weights if needed
    _ensure_generated_weights(source_dir)

    outputs: list[Path] = []
    css_entries: list[FontFaceEntry] = []
    fallback_metrics: FontFallbackMetrics | None = None

    faces, win_box = _process_family(
        source_dir,
        variant,
        family=FAMILY_NAME,
        version=font_version,
    )

    for v, fixed in faces:
        name = v["name"]
        # One clipping box for the whole family, measured over every face above.
        if win_box is not None:
            apply_win_box(fixed, win_box)
        if fallback_metrics is None:
            fallback_metrics = _font_fallback_metrics(fixed)

        # Validate
        _log_issues(name, validate_font(fixed, expected_weight=v["weight"]))

        # Emit each requested format from the full glyph set (no subsetting): TTF for
        # local install plus WOFF2/WOFF for the web. This makes Extended a true superset
        # of Text in both glyph coverage and formats. Filenames track the family name,
        # e.g. PlanetaireMonoExtended-Regular.ttf.
        stem = f"{FAMILY_NAME.replace(' ', '')}-{name}"
        for fmt in formats:
            flavor = None if fmt == "ttf" else fmt
            out_path = output_dir / f"{stem}.{fmt}"
            save_web_font(fixed, out_path, flavor=flavor)
            log.info("Wrote %s", out_path)
            outputs.append(out_path)

        css_entries.append(FontFaceEntry(stem, v["weight"], "Italic" in name))

    if css_entries and ("woff2" in formats or "woff" in formats):
        css_path = output_dir / "planetaire-mono-extended.css"
        _write_font_face_css(
            css_path,
            css_entries,
            formats,
            family=FAMILY_NAME,
            fallback_metrics=fallback_metrics,
        )
        log.info("Wrote %s", css_path)
        outputs.append(css_path)

    return outputs


def build_text(
    source_dir: Path,
    output_dir: Path,
    variant: str | None = None,
    *,
    formats: tuple[str, ...] = ("woff2", "ttf"),
    split: bool = False,
    subsets: tuple[str, ...] = TEXT_SLIM_WEB_SUBSETS,
    include_italics: bool = False,
    version: str | None = None,
) -> list[Path]:
    """
    Build the lightweight Planetaire Mono Text family.

    Same letterforms as the full build. By default, output is subset to the full
    standard-Unicode Text coverage and emitted as WOFF2/WOFF/TTF plus a generated
    ``@font-face`` stylesheet. With ``split=True``, emit Google Fonts-style WOFF2
    subsets for the slim web profile: Regular/Bold upright, Latin, Greek, and Cyrillic;
    optionally add the matching italic companion.

    `version` stamps an explicit release version instead of resolving the canonical
    one; see `resolve_font_version`.

    Returns the list of written paths (fonts and the CSS file).
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    font_version = resolve_font_version(version)
    log.info("Building %s version %s", TEXT_FAMILY_NAME, font_version)

    _ensure_generated_weights(source_dir)

    outputs: list[Path] = []
    css_entries: list[FontFaceEntry] = []
    italic_css_entries: list[FontFaceEntry] = []
    fallback_metrics: FontFallbackMetrics | None = None
    split_subset_defs = _resolve_text_subset_defs(subsets) if split else []
    split_formats = tuple(fmt for fmt in formats if fmt in {"woff2", "woff"})
    ignored_split_formats = tuple(fmt for fmt in formats if fmt not in {"woff2", "woff"})
    if split and ignored_split_formats:
        ignored = ", ".join(ignored_split_formats)
        log.warning("Split Text web build ignores non-web format(s): %s", ignored)
    if split and not split_formats:
        split_formats = ("woff2",)
    variant_names: set[str] | None = None
    if split and variant is None:
        variant_names = set(TEXT_SLIM_WEB_VARIANTS)
        if include_italics:
            variant_names.update(TEXT_SLIM_WEB_ITALIC_VARIANTS)

    def prepare(font: TTFont) -> tuple[TTFont, TTFont]:
        """Measure the box on Text coverage; emit from whichever face is written.

        Dropping the Private-Use Nerd Font icons is what separates the Text
        family's box from Extended's, so the box is measured after that cut. The
        split build still emits from the full merged face: its script subsets keep
        a handful of glyphs (U+02BB, U+02BC, U+2C7D, U+FEFF) that the Text subset
        drops, so cutting them from the Text face would silently lose those.
        """
        measured = deepcopy(font) if split else font
        subset_font(measured, TEXT_SUBSET_RANGES, drop_hinting=True)
        return measured, (font if split else measured)

    faces, win_box = _process_family(
        source_dir,
        variant,
        family=TEXT_FAMILY_NAME,
        version=font_version,
        emit_names=variant_names,
        prepare=prepare,
    )

    for v, font in faces:
        name = v["name"]
        stem = f"{TEXT_FAMILY_NAME.replace(' ', '')}-{name}"
        is_italic = "Italic" in name
        if fallback_metrics is None and (not split or not is_italic):
            fallback_metrics = _font_fallback_metrics(font)

        if split:
            for subset_def in split_subset_defs:
                if not _font_has_codepoints_in_ranges(font, subset_def["ranges"]):
                    log.warning(
                        "Skipping %s %s subset %s: no codepoints match %s",
                        TEXT_FAMILY_NAME,
                        name,
                        subset_def["name"],
                        subset_def["unicode_range"],
                    )
                    continue
                subset_font_obj = deepcopy(font)
                subset_font(subset_font_obj, subset_def["ranges"], drop_hinting=True)
                # A script subset is a slice of its face, not a face of its own: it
                # declares the family's box, not the smaller box its own ink would
                # allow. Re-measuring here is what gave one weight three different
                # line boxes across its own subsets.
                if win_box is not None:
                    apply_win_box(subset_font_obj, win_box)
                _log_issues(f"{stem}-{subset_def['name']}", validate_font(subset_font_obj))
                for fmt in split_formats:
                    out_stem = f"{stem}-{subset_def['name']}"
                    out_path = output_dir / f"{out_stem}.{fmt}"
                    save_web_font(subset_font_obj, out_path, flavor=fmt)
                    log.info("Wrote %s", out_path)
                    outputs.append(out_path)
                entry = FontFaceEntry(
                    f"{stem}-{subset_def['name']}",
                    v["weight"],
                    is_italic,
                    subset_def["unicode_range"],
                )
                if is_italic:
                    italic_css_entries.append(entry)
                else:
                    css_entries.append(entry)
            continue

        # Already subset to Text coverage by `prepare`, where the box was measured.
        if win_box is not None:
            apply_win_box(font, win_box)
        _log_issues(name, validate_font(font, expected_weight=v["weight"]))
        for fmt in formats:
            flavor = None if fmt == "ttf" else fmt
            out_path = output_dir / f"{stem}.{fmt}"
            save_web_font(font, out_path, flavor=flavor)
            log.info("Wrote %s", out_path)
            outputs.append(out_path)

        css_entries.append(FontFaceEntry(stem, v["weight"], is_italic))

    if css_entries and ("woff2" in formats or "woff" in formats or split):
        css_path = output_dir / TEXT_WEB_CSS_NAME
        _write_font_face_css(
            css_path,
            css_entries,
            split_formats if split else formats,
            family=TEXT_FAMILY_NAME,
            fallback_metrics=fallback_metrics,
        )
        log.info("Wrote %s", css_path)
        outputs.append(css_path)
    if italic_css_entries and split:
        css_path = output_dir / "planetaire-mono-text-italics.css"
        _write_font_face_css(css_path, italic_css_entries, split_formats, family=TEXT_FAMILY_NAME)
        log.info("Wrote %s", css_path)
        outputs.append(css_path)

    return outputs


def _resolve_text_subset_defs(subsets: tuple[str, ...]) -> list[TextSubsetDef]:
    """Resolve requested split subset names from config."""
    resolved: list[TextSubsetDef] = []
    for subset in subsets:
        try:
            resolved.append(TEXT_SUBSET_GROUPS[subset])
        except KeyError as e:
            known = ", ".join(TEXT_SUBSET_GROUPS)
            raise ValueError(f"Unknown text subset {subset!r}; expected one of: {known}") from e
    return resolved


def _write_font_face_css(
    path: Path,
    entries: list[FontFaceEntry],
    formats: tuple[str, ...],
    *,
    family: str,
    fallback_metrics: FontFallbackMetrics | None = None,
) -> None:
    """Write a generated @font-face stylesheet for `family`'s web fonts."""
    blocks: list[str] = []
    fallback_family = f"{family} Fallback"
    stack_var = font_stack_css_var(family)
    for entry in entries:
        srcs: list[str] = []
        if "woff2" in formats:
            srcs.append(f"url('{entry.stem}.woff2') format('woff2')")
        if "woff" in formats:
            srcs.append(f"url('{entry.stem}.woff') format('woff')")
        src = ",\n       ".join(srcs)
        style = "italic" if entry.is_italic else "normal"
        unicode_range = f"  unicode-range: {entry.unicode_range};\n" if entry.unicode_range else ""
        blocks.append(
            f"@font-face {{\n"
            f"  font-family: '{family}';\n"
            f"  font-style: {style};\n"
            f"  font-weight: {entry.weight};\n"
            f"  font-display: swap;\n"
            f"{unicode_range}"
            f"  src: {src};\n"
            f"}}"
        )
    if fallback_metrics is not None:
        blocks.append(
            f":root {{\n"
            f"  --{stack_var}: '{family}', '{fallback_family}', ui-monospace, monospace;\n"
            f"}}\n\n"
            f"@font-face {{\n"
            f"  font-family: '{fallback_family}';\n"
            f"  src: local('Menlo'), local('Consolas'), local('Liberation Mono'),\n"
            f"       local('DejaVu Sans Mono'), local('Courier New');\n"
            f"  size-adjust: {_css_percentage(fallback_metrics.size_adjust)};\n"
            f"  ascent-override: {_css_percentage(fallback_metrics.ascent_override)};\n"
            f"  descent-override: {_css_percentage(fallback_metrics.descent_override)};\n"
            f"  line-gap-override: {_css_percentage(fallback_metrics.line_gap_override)};\n"
            f"}}"
        )
    header_lines = [
        f"/* {family} @font-face declarations.",
        "   Generated by `planetaire build` — do not edit by hand.",
    ]
    if fallback_metrics is not None:
        header_lines.append(f"   Use: font-family: var(--{stack_var});")
    header = "\n".join(header_lines) + " */\n\n"
    path.write_text(header + "\n\n".join(blocks) + "\n")


def _font_fallback_metrics(font: TTFont) -> FontFallbackMetrics:
    """Measure CSS fallback metric overrides from the font's horizontal metrics."""
    units_per_em = font["head"].unitsPerEm
    hhea = font["hhea"]
    return FontFallbackMetrics(
        size_adjust=100.0,
        ascent_override=(hhea.ascent / units_per_em) * 100,
        descent_override=(abs(hhea.descent) / units_per_em) * 100,
        line_gap_override=(hhea.lineGap / units_per_em) * 100,
    )


def _css_percentage(value: float) -> str:
    """Format a CSS percentage compactly while keeping one decimal when needed."""
    text = f"{value:.1f}".rstrip("0").rstrip(".")
    return f"{text}%"


def _font_has_codepoints_in_ranges(font: TTFont, ranges: list[tuple[int, int]]) -> bool:
    """Return true when at least one encoded glyph falls within `ranges`."""
    cmap = font.getBestCmap() or {}
    return any(start <= codepoint <= end for codepoint in cmap for start, end in ranges)
