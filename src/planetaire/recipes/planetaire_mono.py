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
from strif import atomic_output_file

from planetaire.config import (
    PLANETAIRE_GSUB_FEATURES,
    PLANETAIRE_LETTER_RANGES,
    VARIANTS,
)
from planetaire.ops.fix import fix_font
from planetaire.ops.merge import merge_glyphs
from planetaire.ops.rename import rename_font
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


def build_planetaire_mono(
    source_dir: Path,
    output_dir: Path,
    variant: str | None = None,
) -> list[Path]:
    """
    Build Planetaire Mono font family.

    For each variant: load Hack as base, merge B612 letter glyphs,
    rename to "Planetaire Mono", apply fixes, validate, and save.

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

    variants_to_build = (
        VARIANTS if variant is None else [v for v in VARIANTS if v["name"] == variant]
    )

    for v in variants_to_build:
        name = v["name"]
        hack_file = v["hack_file"]
        b612_file = v["b612_file"]
        subfamily = v["subfamily"]
        weight = v["weight"]

        log.info("Building Planetaire Mono %s", name)

        hack_path = source_dir / "hack" / hack_file
        b612_path = source_dir / "b612" / b612_file

        if not hack_path.exists():
            log.warning("Skipping %s: Hack source not found at %s", name, hack_path)
            continue
        if not b612_path.exists():
            log.warning("Skipping %s: B612 source not found at %s", name, b612_path)
            continue

        base = TTFont(hack_path)
        donor = TTFont(b612_path)

        # Merge B612 letter glyphs into Hack base
        merged = merge_glyphs(
            base,
            donor,
            PLANETAIRE_LETTER_RANGES,
            copy_gsub_features=PLANETAIRE_GSUB_FEATURES,
        )

        # Rename to Planetaire Mono
        renamed = rename_font(
            merged,
            family="Planetaire Mono",
            subfamily=subfamily,
            weight=weight,
            version=font_version,
        )

        # Add dotted zero (circle default + rect alternate via ss01/zero)
        dotted = add_dotted_zero(renamed)

        # Apply post-processing fixes
        fixed = fix_font(dotted)

        # Validate
        issues = validate_font(fixed, expected_weight=weight)
        for issue in issues:
            log.warning("Validation %s: %s", issue.severity, issue.message)

        # Save
        output_filename = f"PlanetaireMono-{name}.ttf"
        output_path = output_dir / output_filename
        with atomic_output_file(str(output_path)) as tmp:
            fixed.save(tmp)

        log.info("Wrote %s", output_path)
        outputs.append(output_path)

    return outputs
