"""
Full Planetaire Mono build pipeline.

Composes ops/ functions to produce all Planetaire Mono font variants
from B612 and Hack source fonts.
"""

from __future__ import annotations

import logging
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

log = logging.getLogger(__name__)


def build_planetaire_mono(
    source_dir: Path,
    output_dir: Path,
    variant: str | None = None,
) -> list[Path]:
    """
    Build Planetaire Mono font family.

    For each variant: load Hack as base, merge B612 letter glyphs,
    rename to "Planetaire Mono", apply fixes, validate, and save.

    Returns list of output font paths.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
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
        )

        # Apply post-processing fixes
        fixed = fix_font(renamed)

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
