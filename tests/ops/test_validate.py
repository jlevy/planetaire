"""Tests for ops/validate — font validation."""

from __future__ import annotations

from fontTools.ttLib import TTFont

from planetaire.ops.merge import glyph_ink_top
from planetaire.ops.validate import validate_font


def test_validate_clean_font(base_font: TTFont):
    """A well-formed font with no expectations passes validation."""
    issues = validate_font(base_font)
    assert not any(i.severity == "error" for i in issues)


def test_validate_detects_weight_mismatch(base_font: TTFont):
    issues = validate_font(base_font, expected_weight=700)
    errors = [i for i in issues if i.severity == "error" and i.category == "metrics"]
    assert len(errors) == 1
    assert "700" in errors[0].message


def test_validate_detects_missing_glyphs(base_font: TTFont):
    # Expect Greek range, which our minimal font doesn't have
    issues = validate_font(base_font, expected_ranges=[(0x0370, 0x03FF)])
    errors = [i for i in issues if i.severity == "error" and i.category == "glyph_coverage"]
    assert len(errors) == 1
    assert "Missing" in errors[0].message


def test_validate_passes_with_correct_ranges(base_font: TTFont):
    # Expect A-Z which our font does have
    issues = validate_font(base_font, expected_ranges=[(0x0041, 0x005A)])
    errors = [i for i in issues if i.severity == "error" and i.category == "glyph_coverage"]
    assert len(errors) == 0


def test_validate_real_b612(b612_regular: TTFont):
    """Real B612 font passes basic validation.

    expect_monospace=False: the raw donor carries intentional double-width
    glyphs (e.g. Roman numerals at 2x the cell) that are only normalized to the
    Planetaire cell during the build, not a property of the source itself.

    Metrics are excluded for a similar reason: B612 declares round design values
    (sxHeight 1100, sCapHeight 1500) about 20 units under where it actually draws
    `x` and `H`, and its xAvgCharWidth averages a proportional-width glyph set.
    Those are the designer's numbers for the source, not a claim the Planetaire
    build makes about its own output.
    """
    issues = validate_font(b612_regular, expect_monospace=False)
    errors = [i for i in issues if i.severity == "error" and i.category != "metrics"]
    assert len(errors) == 0


def _metrics_errors(font: TTFont) -> list[str]:
    return [
        i.message
        for i in validate_font(font, expect_monospace=False)
        if i.severity == "error" and i.category == "metrics"
    ]


def test_validate_accepts_metrics_matching_the_outlines(base_font: TTFont):
    """The fixture's OS/2 measurements describe its own glyphs, so nothing fires."""
    assert _metrics_errors(base_font) == []


def test_validate_detects_stale_x_height(base_font: TTFont):
    """An sxHeight that does not match the drawn `x` is an error.

    This is the plt-y36x defect in miniature: the merge left the base font's
    x-height in OS/2 after replacing the letterforms it measured.
    """
    drawn = glyph_ink_top(base_font, "x")
    assert drawn is not None
    base_font["OS/2"].sxHeight = drawn - 20

    messages = _metrics_errors(base_font)
    assert any("sxHeight" in m and str(drawn) in m for m in messages)


def test_validate_detects_stale_cap_height(base_font: TTFont):
    """A sCapHeight that does not match the drawn `H` is an error."""
    drawn = glyph_ink_top(base_font, "H")
    assert drawn is not None
    base_font["OS/2"].sCapHeight = drawn - 20

    messages = _metrics_errors(base_font)
    assert any("sCapHeight" in m and str(drawn) in m for m in messages)


def test_validate_allows_small_height_rounding(base_font: TTFont):
    """A couple of units of rounding is within tolerance and is not reported."""
    base_font["OS/2"].sxHeight -= 2
    base_font["OS/2"].sCapHeight += 2
    assert _metrics_errors(base_font) == []


def test_validate_detects_stale_avg_char_width(base_font: TTFont):
    """xAvgCharWidth must be the mean non-zero advance, not the base font's."""
    base_font["OS/2"].xAvgCharWidth += 33

    messages = _metrics_errors(base_font)
    assert any("xAvgCharWidth" in m for m in messages)


def test_validate_detects_clipping_win_metrics(base_font: TTFont):
    """usWin* smaller than the ink would clip glyphs on Windows."""
    base_font["OS/2"].usWinAscent = 10
    base_font["OS/2"].usWinDescent = 0

    messages = _metrics_errors(base_font)
    assert any("usWinAscent" in m and "clips" in m for m in messages)


def test_validate_allows_win_metrics_larger_than_ink(base_font: TTFont):
    """A win box roomier than the ink is fine — subsetting shrinks ink, not the box."""
    base_font["OS/2"].usWinAscent += 500
    base_font["OS/2"].usWinDescent += 500
    assert _metrics_errors(base_font) == []


def _set_subfamily(font: TTFont, name: str) -> None:
    font["name"].setName(name, 2, 3, 1, 0x0409)
    font["name"].setName(name, 2, 1, 0, 0)


def test_validate_style_linking_consistent_italic(base_font: TTFont):
    """Matching italic name + macStyle + fsSelection produces no style errors."""
    _set_subfamily(base_font, "Italic")
    base_font["head"].macStyle |= 0x02
    base_font["OS/2"].fsSelection = (base_font["OS/2"].fsSelection | 0x01) & ~0x40
    errors = [
        i
        for i in validate_font(base_font)
        if i.severity == "error" and i.category == "style_linking"
    ]
    assert errors == []


def test_validate_style_linking_detects_italic_bit_mismatch(base_font: TTFont):
    """Italic set in head but not OS/2 is flagged."""
    _set_subfamily(base_font, "Italic")
    base_font["head"].macStyle |= 0x02  # italic in head only
    errors = [
        i
        for i in validate_font(base_font)
        if i.severity == "error" and i.category == "style_linking"
    ]
    assert any("Italic flag mismatch" in i.message for i in errors)


def test_validate_style_linking_detects_name_vs_flag_mismatch(base_font: TTFont):
    """Subfamily 'Bold' without bold bits is flagged."""
    _set_subfamily(base_font, "Bold")
    errors = [
        i
        for i in validate_font(base_font)
        if i.severity == "error" and i.category == "style_linking"
    ]
    assert any("do not match subfamily" in i.message for i in errors)


def test_validate_style_linking_semibold_not_bold(base_font: TTFont):
    """'SemiBold' (600) contains the substring 'bold' but is not a bold face.

    Regression: the bold bit is correctly unset, so it must not be flagged as a
    name/flag mismatch (unlike a true 'Bold' face without the bit).
    """
    _set_subfamily(base_font, "SemiBold")
    errors = [
        i
        for i in validate_font(base_font)
        if i.severity == "error" and i.category == "style_linking"
    ]
    assert errors == []
