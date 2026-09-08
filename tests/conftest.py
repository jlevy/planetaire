"""Shared test fixtures — minimal fonts built with fontTools for fast tests."""

from __future__ import annotations

from pathlib import Path

import pytest
from fontTools.fontBuilder import FontBuilder
from fontTools.ttLib import TTFont

FONTS_SOURCE = Path(__file__).parent.parent / "fonts" / "source"

# The minimal fixture draws every glyph as this one rectangle, so it is also the
# ink top that OS/2's measured height fields have to agree with.
GLYPH_INK_TOP = 700
GLYPH_INK_LEFT = 100
GLYPH_INK_RIGHT = 500


def _make_minimal_font(
    *,
    family: str = "TestFont",
    upm: int = 1000,
    weight: int = 400,
    codepoints: dict[int, str] | None = None,
    advance_width: int = 600,
) -> TTFont:
    """
    Build a minimal TrueType font with simple rectangular glyphs.

    Each glyph is a simple rectangle so we can verify merging/comparison
    without needing real glyph outlines.
    """
    if codepoints is None:
        # Default: A-Z + a-z + 0-9
        codepoints = {}
        for cp in range(0x41, 0x5B):  # A-Z
            codepoints[cp] = chr(cp)
        for cp in range(0x61, 0x7B):  # a-z
            codepoints[cp] = chr(cp)
        for cp in range(0x30, 0x3A):  # 0-9
            codepoints[cp] = chr(cp)

    glyph_names = [".notdef"] + [f"uni{cp:04X}" for cp in sorted(codepoints.keys())]
    cmap = {cp: f"uni{cp:04X}" for cp in codepoints}

    fb = FontBuilder(upm, isTTF=True)
    fb.setupGlyphOrder(glyph_names)
    fb.setupCharacterMap(cmap)

    # Build glyph objects using TTGlyphPen
    from fontTools.pens.ttGlyphPen import TTGlyphPen

    glyphs = {}
    for gname in glyph_names:
        pen = TTGlyphPen(None)
        pen.moveTo((GLYPH_INK_LEFT, 0))
        pen.lineTo((GLYPH_INK_LEFT, GLYPH_INK_TOP))
        pen.lineTo((GLYPH_INK_RIGHT, GLYPH_INK_TOP))
        pen.lineTo((GLYPH_INK_RIGHT, 0))
        pen.closePath()
        glyphs[gname] = pen.glyph()

    fb.setupGlyf(glyphs)

    fb.setupHorizontalMetrics({gname: (advance_width, 100) for gname in glyph_names})
    fb.setupHorizontalHeader(ascent=800, descent=-200)
    fb.setupNameTable(
        {
            "familyName": family,
            "styleName": "Regular" if weight <= 400 else "Bold",
        }
    )
    # OS/2's measured fields describe the rectangle above, so the fixture is a
    # font whose table and outlines agree — the baseline the metrics checks want.
    fb.setupOS2(
        sTypoAscender=800,
        sTypoDescender=-200,
        usWeightClass=weight,
        sxHeight=GLYPH_INK_TOP,
        sCapHeight=GLYPH_INK_TOP,
        usWinAscent=800,
        usWinDescent=200,
        xAvgCharWidth=advance_width,
    )
    fb.setupPost()
    fb.setupHead(unitsPerEm=upm)

    return fb.font


@pytest.fixture
def base_font() -> TTFont:
    """A minimal base font (UPM=1000, weight=400)."""
    return _make_minimal_font(family="BaseFont", upm=1000, weight=400)


@pytest.fixture
def donor_font() -> TTFont:
    """A minimal donor font (UPM=2000, weight=400) with different glyphs."""
    return _make_minimal_font(family="DonorFont", upm=2000, weight=400, advance_width=1200)


@pytest.fixture
def b612_regular() -> TTFont:
    """Load real B612Mono-Regular if available."""
    path = FONTS_SOURCE / "b612" / "B612Mono-Regular.ttf"
    if not path.exists():
        pytest.skip("B612 source font not available")
    return TTFont(path)


@pytest.fixture
def hack_regular() -> TTFont:
    """Load real HackNerdFont-Regular if available."""
    path = FONTS_SOURCE / "hack" / "HackNerdFont-Regular.ttf"
    if not path.exists():
        pytest.skip("Hack source font not available")
    return TTFont(path)
