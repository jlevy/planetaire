"""Tests for ops/merge — binary glyph merging by unicode range."""

from __future__ import annotations

from fontTools.ttLib import TTFont

from planetaire.ops.merge import merge_glyphs


def test_merge_copies_glyphs_for_range(base_font: TTFont, donor_font: TTFont):
    """Glyphs in the merge range come from the donor."""
    # Merge A-Z from donor into base
    result = merge_glyphs(base_font, donor_font, [(0x41, 0x5A)])

    cmap = result.getBestCmap()
    assert cmap is not None
    # A should be present
    assert 0x41 in cmap


def test_merge_preserves_base_glyphs_outside_range(base_font: TTFont, donor_font: TTFont):
    """Glyphs outside the merge range stay from the base."""
    # Merge only A-Z; digits 0-9 should remain from base
    result = merge_glyphs(base_font, donor_font, [(0x41, 0x5A)])

    cmap = result.getBestCmap()
    assert cmap is not None
    # Digits should still be present
    assert 0x30 in cmap


def test_merge_handles_upm_normalization(base_font: TTFont, donor_font: TTFont):
    """When UPMs differ, base is scaled to match donor."""
    # base is UPM=1000, donor is UPM=2000
    result = merge_glyphs(base_font, donor_font, [(0x41, 0x5A)])
    assert result["head"].unitsPerEm == 2000


def test_merge_without_upm_normalization(base_font: TTFont, donor_font: TTFont):
    """When normalize_upm is False, UPM is preserved."""
    result = merge_glyphs(base_font, donor_font, [(0x41, 0x5A)], normalize_upm=False)
    assert result["head"].unitsPerEm == 1000


def test_merge_real_fonts(b612_regular: TTFont, hack_regular: TTFont):
    """Merge B612 letters into Hack base with real fonts."""
    result = merge_glyphs(
        hack_regular,
        b612_regular,
        [(0x41, 0x5A), (0x61, 0x7A)],  # A-Z, a-z
    )

    cmap = result.getBestCmap()
    assert cmap is not None
    # All ASCII letters should be present
    for cp in range(0x41, 0x5B):
        assert cp in cmap
    for cp in range(0x61, 0x7B):
        assert cp in cmap

    # UPM should be normalized to B612's 2000
    assert result["head"].unitsPerEm == 2000
