"""Tests for ops/monospace — single-advance-width invariant + normalization."""

from __future__ import annotations

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont

from planetaire.ops.monospace import (
    cell_width,
    check_monospace,
    normalize_monospace,
    set_fixed_pitch_flags,
)


def _font_with_wide_glyph(codepoint: int, *, cell: int = 600, ink: int = 800) -> TTFont:
    """A monospace font (advance=cell) plus one over-wide glyph at ``codepoint``.

    The over-wide glyph carries a wider-than-cell advance so normalize_monospace
    touches it; its ink (``ink`` units, centered) exceeds the cell so we can see
    whether normalization condenses it (tiling) or lets it overhang (text).
    """
    # A handful of plain cell-width filler glyphs establish the cell, plus the
    # one wide glyph under test.
    filler = {0x41 + i: f"uni{0x41 + i:04X}" for i in range(6)}
    wide_name = f"uni{codepoint:04X}"
    glyph_names = [".notdef", *filler.values(), wide_name]
    cmap = {cp: name for cp, name in filler.items()}
    cmap[codepoint] = wide_name

    fb = FontBuilder(1000, isTTF=True)
    fb.setupGlyphOrder(glyph_names)
    fb.setupCharacterMap(cmap)

    glyphs = {}
    for gname in glyph_names:
        pen = TTGlyphPen(None)
        if gname == wide_name:
            x0, x1 = 0, ink  # wide rectangle, will be recentered/condensed
        else:
            x0, x1 = 100, 500
        pen.moveTo((x0, 0))
        pen.lineTo((x0, 700))
        pen.lineTo((x1, 700))
        pen.lineTo((x1, 0))
        pen.closePath()
        glyphs[gname] = pen.glyph()
    fb.setupGlyf(glyphs)

    metrics = {g: (cell, 0) for g in glyph_names}
    metrics[wide_name] = (cell + 200, 0)  # off the cell grid -> normalized
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=800, descent=-200)
    fb.setupNameTable({"familyName": "WideTest", "styleName": "Regular"})
    fb.setupOS2(sTypoAscender=800, sTypoDescender=-200, usWeightClass=400)
    fb.setupPost()
    fb.setupHead(unitsPerEm=1000)
    return fb.font


def test_check_detects_nonuniform(base_font: TTFont):
    hmtx = base_font["hmtx"]
    names = [n for n in base_font.getGlyphOrder() if n != ".notdef"]
    hmtx[names[0]] = (800, hmtx[names[0]][1])  # widen one glyph
    hmtx[names[1]] = (500, hmtx[names[1]][1])  # narrow another

    report = check_monospace(base_font)
    assert report.cell_width == 600  # the unchanged majority
    assert not report.is_monospace
    offending = {n for n, _ in report.nonuniform}
    assert names[0] in offending and names[1] in offending


def test_normalize_makes_uniform(base_font: TTFont):
    hmtx = base_font["hmtx"]
    names = [n for n in base_font.getGlyphOrder() if n != ".notdef"]
    hmtx[names[0]] = (800, hmtx[names[0]][1])
    hmtx[names[1]] = (500, hmtx[names[1]][1])

    stats = normalize_monospace(base_font)
    assert stats["cell"] == 600
    report = check_monospace(base_font)
    assert report.is_monospace
    assert all(hmtx[n][0] == 600 for n in base_font.getGlyphOrder())


def test_cell_glyphs_left_untouched(base_font: TTFont):
    """Glyphs already at the cell width keep their exact outline (byte-identical)."""
    glyf = base_font["glyf"]
    names = [n for n in base_font.getGlyphOrder() if n != ".notdef"]
    base_font["hmtx"][names[0]] = (800, base_font["hmtx"][names[0]][1])  # force a normalize pass

    untouched = names[5]  # stays at cell width (600)
    before = glyf[untouched].compile(glyf)
    normalize_monospace(base_font)
    after = base_font["glyf"][untouched].compile(base_font["glyf"])
    assert before == after


def test_recenters_without_distorting_height(base_font: TTFont):
    """A widened glyph is recentered to the cell; vertical extent is unchanged."""
    glyf = base_font["glyf"]
    name = next(n for n in base_font.getGlyphOrder() if n != ".notdef")
    glyf[name].recalcBounds(glyf)
    y_before = (glyf[name].yMin, glyf[name].yMax)
    base_font["hmtx"][name] = (760, base_font["hmtx"][name][1])  # ~1.27x cell -> snaps to 1

    normalize_monospace(base_font)
    g = base_font["glyf"][name]
    g.recalcBounds(base_font["glyf"])
    assert base_font["hmtx"][name][0] == 600
    assert (g.yMin, g.yMax) == y_before  # x-only transform
    assert g.xMin >= 0 and g.xMax <= 600  # fits the cell


def test_zero_width_marks_preserved(base_font: TTFont):
    name = next(n for n in base_font.getGlyphOrder() if n != ".notdef")
    base_font["hmtx"][name] = (0, base_font["hmtx"][name][1])
    normalize_monospace(base_font)
    assert base_font["hmtx"][name][0] == 0  # marks stay zero-width


def test_cell_width_is_the_mode(base_font: TTFont):
    assert cell_width(base_font) == 600


def test_set_fixed_pitch_flags(base_font: TTFont):
    set_fixed_pitch_flags(base_font)
    assert base_font["post"].isFixedPitch == 1
    assert base_font["OS/2"].panose.bProportion == 9


def test_wide_letter_overhangs_instead_of_condensing():
    """An over-wide LETTER keeps its ink width and is recentered (allowed to overhang).

    Regression for plt-3h7p: horizontally condensing wide letters (italic m/x/y)
    thinned their strokes unevenly. Letters must keep full ink width; only their
    advance is pinned to the cell.
    """
    font = _font_with_wide_glyph(0x6D, cell=600, ink=800)  # 'm', a text codepoint
    stats = normalize_monospace(font)
    assert stats["condensed"] == 0  # letters are never condensed
    glyf = font["glyf"]
    g = glyf["uni006D"]
    g.recalcBounds(glyf)
    assert font["hmtx"]["uni006D"][0] == 600  # advance pinned to cell (monospace)
    assert g.xMax - g.xMin == 800  # ink width preserved (no thinning)
    # Recentered: overhang is symmetric about the cell.
    left_over = -g.xMin
    right_over = g.xMax - 600
    assert abs(left_over - right_over) <= 2
    assert left_over > 0  # it does overhang


def test_wide_tiling_glyph_is_condensed_to_fit():
    """An over-wide TILING glyph (box-drawing) is condensed so ink stays in the cell.

    Box-drawing/block/Powerline glyphs tile seamlessly with neighbours, so their
    ink must not overhang. They keep the strict scale-to-fit behavior.
    """
    font = _font_with_wide_glyph(0x2500, cell=600, ink=800)  # box-drawing light horizontal
    stats = normalize_monospace(font)
    assert stats["condensed"] == 1  # tiling glyph condensed
    glyf = font["glyf"]
    g = glyf["uni2500"]
    g.recalcBounds(glyf)
    assert font["hmtx"]["uni2500"][0] == 600
    # Ink fits inside the cell (with the small condense margin on each side).
    assert g.xMin >= 0 and g.xMax <= 600
    assert g.xMax - g.xMin < 800  # was scaled down
