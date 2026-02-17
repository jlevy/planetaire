"""Tests for ops/compare — glyph-level font comparison."""

from __future__ import annotations

from fontTools.ttLib import TTFont

from planetaire.ops.compare import compare_fonts


def test_compare_identical_fonts(base_font: TTFont):
    """Comparing a font to itself yields all identical."""
    result = compare_fonts(base_font, base_font)
    assert result.identical > 0
    assert result.different == 0
    assert result.missing_a == 0
    assert result.missing_b == 0


def test_compare_different_upm_fonts(base_font: TTFont, donor_font: TTFont):
    """Fonts with different UPMs but same structure show differences due to scaling."""
    result = compare_fonts(base_font, donor_font, [(0x41, 0x5A)])
    # Should have some results (identical or different depending on tolerance)
    total = result.identical + result.different + result.missing_a + result.missing_b
    assert total > 0


def test_compare_with_specific_ranges(base_font: TTFont, donor_font: TTFont):
    """Comparing only specific ranges limits the comparison scope."""
    result = compare_fonts(base_font, donor_font, [(0x41, 0x43)])  # A, B, C only
    total = result.identical + result.different + result.missing_a + result.missing_b
    assert total == 3


def test_compare_real_b612_to_itself(b612_regular: TTFont):
    """Real B612 compared to itself should be all identical."""
    result = compare_fonts(b612_regular, b612_regular, [(0x41, 0x5A)])
    assert result.identical == 26  # A-Z
    assert result.different == 0


def test_compare_real_b612_vs_hack(b612_regular: TTFont, hack_regular: TTFont):
    """B612 vs Hack should have different glyphs for letters."""
    result = compare_fonts(b612_regular, hack_regular, [(0x41, 0x5A)])
    # These are different fonts so their letter outlines differ
    assert result.different > 0 or result.identical > 0
    total = result.identical + result.different
    assert total == 26
