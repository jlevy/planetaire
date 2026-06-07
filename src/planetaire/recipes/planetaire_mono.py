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
from pathlib import Path

from fontTools.ttLib import TTFont

from planetaire.config import (
    FAMILY_NAME,
    PLANETAIRE_GSUB_FEATURES,
    PLANETAIRE_LETTER_RANGES,
    TEXT_FAMILY_NAME,
    TEXT_SUBSET_RANGES,
    VARIANTS,
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

# Mapping from ExtraBold variants to their Bold source for emboldening.
_EXTRABOLD_FROM_BOLD: dict[str, str] = {
    "B612Mono-ExtraBold.ttf": "B612Mono-Bold.ttf",
    "B612Mono-ExtraBoldItalic.ttf": "B612Mono-BoldItalic.ttf",
}

# Mapping for intermediate weight generation from Regular sources.
# (target_file, source_file, target_weight, change_amount)
_INTERMEDIATE_WEIGHTS: list[tuple[str, str, int, int]] = [
    ("B612Mono-Medium.ttf", "B612Mono-Regular.ttf", 500, 40),
    ("B612Mono-MediumItalic.ttf", "B612Mono-Italic.ttf", 500, 40),
    ("HackNerdFont-Medium.ttf", "HackNerdFont-Regular.ttf", 500, 40),
    ("HackNerdFont-MediumItalic.ttf", "HackNerdFont-Italic.ttf", 500, 40),
]


def _ensure_generated_weights(source_dir: Path) -> None:
    """Generate intermediate and ExtraBold weight variants if not already present.

    Uses FontForge emboldening (changeWeight). If FontForge is not
    installed, logs a warning. Pre-generated files must exist in
    the source directory.
    """
    from planetaire.ops.embolden import embolden_font

    # Generate intermediate weights (Medium) for both B612 and Hack.
    for target_file, source_file, target_weight, change_amount in _INTERMEDIATE_WEIGHTS:
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
            source_path, target_path, target_weight=target_weight, change_amount=change_amount
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
    # Medium/ExtraBold letters (1360-1420) are pinned to the Hack base cell,
    # recentered, and condensed only where ink would otherwise bleed. Must run
    # after the dotted zero so the modified zero is normalized too.
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
    css_entries: list[tuple[str, int, bool]] = []  # (stem, weight, is_italic)

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

        css_entries.append((stem, v["weight"], "Italic" in name))

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
) -> list[Path]:
    """
    Build the lightweight Planetaire Mono Text family.

    Same letterforms as the full build, subset to standard-Unicode text glyphs
    (dropping the Nerd Font icons and Powerline) and emitted as WOFF2/WOFF/TTF plus
    a generated ``@font-face`` stylesheet for the web.

    Returns the list of written paths (fonts and the CSS file).
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    font_version = to_font_version(get_version())
    log.info("Building %s version %s", TEXT_FAMILY_NAME, font_version)

    _ensure_generated_weights(source_dir)

    outputs: list[Path] = []
    css_entries: list[tuple[str, int, bool]] = []  # (stem, weight, is_italic)

    for v, hack_path, b612_path in _resolve_variant_sources(source_dir, variant):
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
        subset_font(font, TEXT_SUBSET_RANGES, drop_hinting=True)

        issues = validate_font(font, expected_weight=v["weight"])
        for issue in issues:
            log.warning("Validation %s: %s", issue.severity, issue.message)

        stem = f"{TEXT_FAMILY_NAME.replace(' ', '')}-{name}"
        for fmt in formats:
            flavor = None if fmt == "ttf" else fmt
            out_path = output_dir / f"{stem}.{fmt}"
            save_web_font(font, out_path, flavor=flavor)
            log.info("Wrote %s", out_path)
            outputs.append(out_path)

        css_entries.append((stem, v["weight"], "Italic" in name))

    if css_entries and ("woff2" in formats or "woff" in formats):
        css_path = output_dir / "planetaire-mono-text.css"
        _write_font_face_css(css_path, css_entries, formats, family=TEXT_FAMILY_NAME)
        log.info("Wrote %s", css_path)
        outputs.append(css_path)

    return outputs


def _write_font_face_css(
    path: Path,
    entries: list[tuple[str, int, bool]],
    formats: tuple[str, ...],
    *,
    family: str,
) -> None:
    """Write a generated @font-face stylesheet for `family`'s web fonts."""
    blocks: list[str] = []
    for stem, weight, is_italic in entries:
        srcs: list[str] = []
        if "woff2" in formats:
            srcs.append(f"url('{stem}.woff2') format('woff2')")
        if "woff" in formats:
            srcs.append(f"url('{stem}.woff') format('woff')")
        src = ",\n       ".join(srcs)
        style = "italic" if is_italic else "normal"
        blocks.append(
            f"@font-face {{\n"
            f"  font-family: '{family}';\n"
            f"  font-style: {style};\n"
            f"  font-weight: {weight};\n"
            f"  font-display: swap;\n"
            f"  src: {src};\n"
            f"}}"
        )
    header = (
        f"/* {family} @font-face declarations.\n"
        f"   Generated by `planetaire build` — do not edit by hand. */\n\n"
    )
    path.write_text(header + "\n\n".join(blocks) + "\n")
