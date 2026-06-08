"""QA: the specimen PDF must use the right fonts and the right symbols.

Two regressions are guarded here:

1. Font fallback (plt-uuag). Typst's built-in font for `raw` (code) elements is
   DejaVu Sans Mono, so any code block or inline code span that does not explicitly
   set the Planetaire font silently falls back to DejaVu. We assert every embedded
   font is a Planetaire Mono face.

2. Prime-for-apostrophe. Typst's smart quotes turn a straight `'` *after a digit*
   into a PRIME (U+2032) -- the thin mark meant for 6' feet / 6" inches. So in prose
   like "B612's" the possessive reads as a prime, not an apostrophe. The specimen
   disables smart quotes document-wide and authors quotes literally (oriented in
   prose, straight ASCII in code), but this test is the backstop: the specimen uses
   no real primes, so the rendered text must contain zero U+2032 (and zero U+2033).
"""

from __future__ import annotations

import re
import shutil
import subprocess
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


# U+2032 PRIME and U+2033 DOUBLE PRIME -- the marks Typst's smart quotes substitute
# for a straight ' / " after a digit. The specimen uses no feet/inch measurements,
# so any occurrence means an apostrophe (e.g. "B612's") was mis-set as a prime.
_PRIME_CHARS = {"′": "U+2032 PRIME", "″": "U+2033 DOUBLE PRIME"}


@pytest.mark.skipif(shutil.which("typst") is None, reason="typst not installed")
@pytest.mark.skipif(shutil.which("pdftotext") is None, reason="pdftotext not installed")
def test_specimen_has_no_prime_for_apostrophe(tmp_path: Path) -> None:
    if not FONT_DIR.exists() or not list(FONT_DIR.glob("PlanetaireMono*.ttf")):
        pytest.skip("fonts not built; run `planetaire build planetaire-mono` first")

    out = tmp_path / "specimen.pdf"
    build_specimen(source=SPECIMEN_SOURCE, output=out, font_dir=FONT_DIR)

    text = subprocess.run(
        ["pdftotext", str(out), "-"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    ).stdout

    found = sorted({name for ch, name in _PRIME_CHARS.items() if ch in text})
    assert not found, (
        f"specimen renders {found} -- a possessive apostrophe after a digit was "
        f"turned into a prime by Typst smart quotes. Keep smart quotes disabled and "
        f"write the apostrophe as a literal oriented ’ (U+2019) in the source."
    )
