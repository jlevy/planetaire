"""
E2E validation: verify Planetaire Mono glyphs match source fonts exactly.

B612 letter/digit ranges must match B612 source (donor).
Hack punctuation/symbol ranges must match Hack source (base after UPM scaling).
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from fontTools.ttLib import TTFont

from planetaire.config import PLANETAIRE_LETTER_RANGES
from planetaire.ops.compare import compare_fonts
from planetaire.recipes.planetaire_mono import build_planetaire_mono

FONTS_SOURCE = Path(__file__).parent.parent.parent / "fonts" / "source"

# Punctuation/symbol ranges that should come from Hack (the base)
HACK_RANGES = [
    (0x0021, 0x002F),  # ! " # $ % & ' ( ) * + , - . /
    (0x003A, 0x0040),  # : ; < = > ? @
    (0x005B, 0x0060),  # [ \ ] ^ _ `
    (0x007B, 0x007E),  # { | } ~
]


@pytest.fixture
def planetaire_regular() -> TTFont:
    """Build a fresh Planetaire Mono Regular for testing."""
    if not (FONTS_SOURCE / "b612").exists() or not (FONTS_SOURCE / "hack").exists():
        pytest.skip("Source fonts not available")

    with tempfile.TemporaryDirectory() as tmpdir:
        outputs = build_planetaire_mono(FONTS_SOURCE, Path(tmpdir), variant="Regular")
        assert len(outputs) == 1
        return TTFont(outputs[0])


def test_b612_letters_match_donor(planetaire_regular: TTFont):
    """Letter glyphs in Planetaire must be identical to B612 donor."""
    donor = TTFont(FONTS_SOURCE / "b612" / "B612MonoLigaNerdFont-Regular.ttf")
    result = compare_fonts(planetaire_regular, donor, PLANETAIRE_LETTER_RANGES)

    assert result.different == 0, (
        f"{result.different} letter glyph(s) differ from B612 donor: "
        + ", ".join(f"U+{d.codepoint:04X}" for d in result.diffs if d.status == "different")
    )
    assert result.identical > 0, "No letter glyphs found to compare"


def test_hack_punctuation_matches_base(planetaire_regular: TTFont):
    """Punctuation/symbol glyphs in Planetaire must match Hack base (after UPM scaling)."""
    base = TTFont(FONTS_SOURCE / "hack" / "HackNerdFont-Regular.ttf")
    result = compare_fonts(planetaire_regular, base, HACK_RANGES)

    assert result.different == 0, (
        f"{result.different} punctuation glyph(s) differ from Hack base: "
        + ", ".join(f"U+{d.codepoint:04X}" for d in result.diffs if d.status == "different")
    )
    assert result.identical > 0, "No punctuation glyphs found to compare"


def test_nerd_font_glyphs_present(planetaire_regular: TTFont):
    """Nerd Font glyphs from Hack must still be present in the merged font."""
    cmap = planetaire_regular.getBestCmap()
    assert cmap is not None

    # Powerline glyphs
    assert 0xE0A0 in cmap  # Branch
    assert 0xE0A1 in cmap  # Line number
    assert 0xE0A2 in cmap  # Padlock
    assert 0xE0B0 in cmap  # Right arrow

    # Seti-UI / Custom glyphs (Nerd Font private use area)
    assert 0xE5FA in cmap  # Common Nerd Font glyph


def test_b612_digits_match_donor(planetaire_regular: TTFont):
    """Digit glyphs must be identical to B612 (they're in the merge range)."""
    donor = TTFont(FONTS_SOURCE / "b612" / "B612MonoLigaNerdFont-Regular.ttf")
    result = compare_fonts(planetaire_regular, donor, [(0x0030, 0x0039)])

    assert result.different == 0
    assert result.identical == 10  # 0-9
