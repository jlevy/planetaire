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
    VARIANTS,
    TextSubsetDef,
    VariantDef,
)
from planetaire.ops.fix import fix_font
from planetaire.ops.merge import merge_glyphs
from planetaire.ops.monospace import normalize_monospace, set_fixed_pitch_flags
from planetaire.ops.rename import rename_font
from planetaire.ops.subset import save_web_font, subset_font
from planetaire.ops.validate import validate_font
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
# it is unaffected there; only Hack's icons are. The cap is applied to SemiBold
# (newly added); Medium keeps the original full pass so its vendored masters
# reproduce exactly.
_INTERMEDIATE_WEIGHTS: list[tuple[str, str, int, int, int | None]] = [
    ("B612Mono-Medium.ttf", "B612Mono-Regular.ttf", 500, 40, None),
    ("B612Mono-MediumItalic.ttf", "B612Mono-Italic.ttf", 500, 40, None),
    ("B612Mono-SemiBold.ttf", "B612Mono-Regular.ttf", 600, 75, 500),
    ("B612Mono-SemiBoldItalic.ttf", "B612Mono-Italic.ttf", 600, 75, 500),
    ("HackNerdFont-Medium.ttf", "HackNerdFont-Regular.ttf", 500, 40, None),
    ("HackNerdFont-MediumItalic.ttf", "HackNerdFont-Italic.ttf", 500, 40, None),
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


def build_planetaire_mono(
    source_dir: Path,
    output_dir: Path,
    variant: str | None = None,
    *,
    formats: tuple[str, ...] = ("ttf", "woff2"),
) -> list[Path]:
    """
    Build Planetaire Mono font family.

    For each variant: load Hack as base, merge B612 letter glyphs,
    rename to "Planetaire Mono Extended", apply fixes, validate, and save.

    ExtraBold B612 variants are auto-generated from Bold via FontForge
    if not already present in source_dir.

    Returns list of output font paths.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Resolve the canonical font version once (shared with the Python package).
    font_version = to_font_version(get_version())
    log.info("Building Planetaire Mono version %s", font_version)

    # Generate intermediate (Medium) and ExtraBold weights if needed
    _ensure_generated_weights(source_dir)

    outputs: list[Path] = []
    css_entries: list[FontFaceEntry] = []

    for v, hack_path, b612_path in _resolve_variant_sources(source_dir, variant):
        name = v["name"]
        log.info("Building %s %s", FAMILY_NAME, name)

        fixed = _process_variant(
            hack_path=hack_path,
            b612_path=b612_path,
            family=FAMILY_NAME,
            subfamily=v["subfamily"],
            weight=v["weight"],
            version=font_version,
        )

        # Validate
        issues = validate_font(fixed, expected_weight=v["weight"])
        for issue in issues:
            log.warning("Validation %s: %s", issue.severity, issue.message)

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
        _write_font_face_css(css_path, css_entries, formats, family=FAMILY_NAME)
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
) -> list[Path]:
    """
    Build the lightweight Planetaire Mono Text family.

    Same letterforms as the full build. By default, output is subset to the full
    standard-Unicode Text coverage and emitted as WOFF2/WOFF/TTF plus a generated
    ``@font-face`` stylesheet. With ``split=True``, emit Google Fonts-style WOFF2
    subsets for the slim web profile: Regular/Bold upright, Latin + Latin Extended;
    optionally add the matching italic companion.

    Returns the list of written paths (fonts and the CSS file).
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    font_version = to_font_version(get_version())
    log.info("Building %s version %s", TEXT_FAMILY_NAME, font_version)

    _ensure_generated_weights(source_dir)

    outputs: list[Path] = []
    css_entries: list[FontFaceEntry] = []
    italic_css_entries: list[FontFaceEntry] = []
    split_subset_defs = _resolve_text_subset_defs(subsets) if split else []
    split_formats = tuple(fmt for fmt in formats if fmt in {"woff2", "woff"})
    if split and not split_formats:
        split_formats = ("woff2",)
    variant_names: set[str] | None = None
    if split and variant is None:
        variant_names = set(TEXT_SLIM_WEB_VARIANTS)
        if include_italics:
            variant_names.update(TEXT_SLIM_WEB_ITALIC_VARIANTS)

    for v, hack_path, b612_path in _resolve_variant_sources(source_dir, variant):
        if variant_names is not None and v["name"] not in variant_names:
            continue

        name = v["name"]
        log.info("Building %s %s", TEXT_FAMILY_NAME, name)

        font = _process_variant(
            hack_path=hack_path,
            b612_path=b612_path,
            family=TEXT_FAMILY_NAME,
            subfamily=v["subfamily"],
            weight=v["weight"],
            version=font_version,
        )

        issues = validate_font(font, expected_weight=v["weight"])
        for issue in issues:
            log.warning("Validation %s: %s", issue.severity, issue.message)

        stem = f"{TEXT_FAMILY_NAME.replace(' ', '')}-{name}"
        is_italic = "Italic" in name

        if split:
            for subset_def in split_subset_defs:
                subset_font_obj = deepcopy(font)
                subset_font(subset_font_obj, subset_def["ranges"], drop_hinting=True)
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

        subset_font(font, TEXT_SUBSET_RANGES, drop_hinting=True)
        for fmt in formats:
            flavor = None if fmt == "ttf" else fmt
            out_path = output_dir / f"{stem}.{fmt}"
            save_web_font(font, out_path, flavor=flavor)
            log.info("Wrote %s", out_path)
            outputs.append(out_path)

        css_entries.append(FontFaceEntry(stem, v["weight"], is_italic))

    if css_entries and ("woff2" in formats or "woff" in formats or split):
        css_path = output_dir / "planetaire-mono-text.css"
        _write_font_face_css(
            css_path,
            css_entries,
            split_formats if split else formats,
            family=TEXT_FAMILY_NAME,
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
) -> None:
    """Write a generated @font-face stylesheet for `family`'s web fonts."""
    blocks: list[str] = []
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
    header = (
        f"/* {family} @font-face declarations.\n"
        f"   Generated by `planetaire build` — do not edit by hand. */\n\n"
    )
    path.write_text(header + "\n\n".join(blocks) + "\n")
