"""Tests for ops/monospace — single-advance-width invariant + normalization."""

from __future__ import annotations

from fontTools.ttLib import TTFont

from planetaire.ops.monospace import (
    cell_width,
    check_monospace,
    normalize_monospace,
    set_fixed_pitch_flags,
)


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
