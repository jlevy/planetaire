"""Download and cache source fonts from upstream repositories.

B612 Mono: original polarsys/b612 from Airbus/Intactile DESIGN.
Hack Nerd Font: from ryanoasis/nerd-fonts releases.

The ExtraBold B612 variants are generated from Bold via FontForge
emboldening (see ops/embolden.py). Pre-generated files can be
placed in the source directory to skip this step.
"""

from __future__ import annotations

import logging
from pathlib import Path

log = logging.getLogger(__name__)


def download_sources(output_dir: Path) -> dict[str, Path]:
    """
    Download B612 Mono and Hack Nerd Font source fonts.

    Returns a dict mapping variant names to font file paths.
    Currently a stub: checks if fonts already exist in output_dir.
    """
    b612_dir = output_dir / "b612"
    hack_dir = output_dir / "hack"

    fonts: dict[str, Path] = {}

    # Check for existing B612 fonts (original polarsys B612 Mono)
    for variant in ("Regular", "Bold", "Italic", "BoldItalic", "ExtraBold", "ExtraBoldItalic"):
        path = b612_dir / f"B612Mono-{variant}.ttf"
        if path.exists():
            fonts[f"b612-{variant.lower()}"] = path
        else:
            log.warning("B612 font not found: %s", path)

    # Check for existing Hack fonts
    for variant in ("Regular", "Bold", "Italic", "BoldItalic", "ExtraBold", "ExtraBoldItalic"):
        path = hack_dir / f"HackNerdFont-{variant}.ttf"
        if path.exists():
            fonts[f"hack-{variant.lower()}"] = path
        else:
            log.warning("Hack font not found: %s", path)

    if not fonts:
        raise FileNotFoundError(
            f"No source fonts found in {output_dir}. "
            "Copy fonts to fonts/source/ or run the download step."
        )

    log.info("Found %d source font(s) in %s", len(fonts), output_dir)
    return fonts
