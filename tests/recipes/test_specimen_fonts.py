"""QA: the specimen PDF must embed only Planetaire fonts (no Typst fallback).

Typst's built-in font for `raw` (code) elements is DejaVu Sans Mono, so any code
block or inline code span that does not explicitly set the Planetaire font
silently falls back to DejaVu. This test renders the specimen and asserts every
embedded font is a Planetaire Mono face, catching any regression where a glyph,
code block, or inline span escapes the font (plt-uuag).
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

import pytest

from planetaire.recipes.specimen import SPECIMEN_SOURCE, build_specimen

FONT_DIR = Path("fonts/output")

# Matches e.g. "/BaseFont /ABCDEF+PlanetaireMonoExtended-Regular"; the 6-char
# "ABCDEF+" subset tag is optional.
_BASEFONT_RE = re.compile(rb"/BaseFont\s*/([A-Za-z0-9.+_-]+)")


def _embedded_fonts(pdf: Path) -> set[str]:
    """Return the set of embedded base-font names (subset tags stripped)."""
    names: set[str] = set()
    for match in _BASEFONT_RE.finditer(pdf.read_bytes()):
        name = match.group(1).decode("latin-1")
        if "+" in name:  # drop the "ABCDEF+" subset prefix
            name = name.split("+", 1)[1]
        names.add(name)
    return names


@pytest.mark.skipif(shutil.which("typst") is None, reason="typst not installed")
def test_specimen_embeds_only_planetaire_fonts(tmp_path: Path) -> None:
    if not FONT_DIR.exists() or not list(FONT_DIR.glob("PlanetaireMono*.ttf")):
        pytest.skip("fonts not built; run `planetaire build planetaire-mono` first")

    out = tmp_path / "specimen.pdf"
    build_specimen(source=SPECIMEN_SOURCE, output=out, font_dir=FONT_DIR)

    fonts = _embedded_fonts(out)
    assert fonts, "no embedded fonts found in the specimen PDF"

    # Every face must be one of ours (PlanetaireMonoExtended / PlanetaireMonoText).
    # A stray family means Typst fell back -- most commonly DejaVu Sans Mono for a
    # code block that did not set the Planetaire font.
    stray = sorted(f for f in fonts if not f.startswith("PlanetaireMono"))
    assert not stray, (
        f"specimen PDF embeds non-Planetaire fonts (Typst fell back): {stray}. "
        f"All embedded fonts: {sorted(fonts)}"
    )
