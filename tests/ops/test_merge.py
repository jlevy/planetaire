"""Tests for ops/merge — binary glyph merging by unicode range."""

from __future__ import annotations

import pytest
from fontTools.ttLib import TTFont

from planetaire.ops.merge import (
    derive_os2_metrics,
    font_ink_extent,
    glyph_ink_top,
    merge_glyphs,
)


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


def _has_instructions(font: TTFont, codepoint: int) -> bool:
    cmap = font.getBestCmap()
    assert cmap is not None
    glyph = font["glyf"][cmap[codepoint]]
    program = getattr(glyph, "program", None)
    return bool(program and program.bytecode)


def test_merge_strips_donor_hinting_by_default(b612_regular: TTFont, hack_regular: TTFont):
    """Copied donor glyphs lose their TrueType instructions (default policy)."""
    assert _has_instructions(b612_regular, 0x41)  # B612 'A' is hinted
    result = merge_glyphs(hack_regular, b612_regular, [(0x41, 0x5A)])
    assert not _has_instructions(result, 0x41)  # stripped in the merge


def test_merge_can_keep_donor_hinting(b612_regular: TTFont, hack_regular: TTFont):
    """Stripping can be disabled to preserve donor instructions."""
    result = merge_glyphs(hack_regular, b612_regular, [(0x41, 0x5A)], strip_donor_hinting=False)
    assert _has_instructions(result, 0x41)


def test_scale_upm_moves_every_measured_os2_field(base_font: TTFont, donor_font: TTFont):
    """UPM normalization scales the font-unit OS/2 fields, leaving none behind.

    Regression for plt-y36x: xAvgCharWidth and the usWin pair used to keep the
    base font's numbers, so a 2048-unit measurement stayed in a 2000-unit font.
    """
    before = base_font["OS/2"]
    expected = {
        "xAvgCharWidth": before.xAvgCharWidth,
        "usWinAscent": before.usWinAscent,
        "usWinDescent": before.usWinDescent,
    }
    scale = 2000 / 1000

    result = merge_glyphs(base_font, donor_font, [(0x41, 0x5A)])

    after = result["OS/2"]
    for field, value in expected.items():
        assert getattr(after, field) == round(value * scale), field


def test_derive_os2_metrics_measures_the_merged_outlines(
    b612_regular: TTFont, hack_regular: TTFont
):
    """After a merge, OS/2's heights describe the donor letters now drawn.

    The defect: Hack declares 0.547 em / 0.729 em, B612 draws 0.560 em / 0.760 em,
    and the merged font kept Hack's table.
    """
    merged = merge_glyphs(hack_regular, b612_regular, [(0x41, 0x5A), (0x61, 0x7A)])
    upm = merged["head"].unitsPerEm
    assert merged["OS/2"].sxHeight != glyph_ink_top(merged, "x")  # the defect

    derive_os2_metrics(merged)

    os2 = merged["OS/2"]
    assert os2.sxHeight == glyph_ink_top(merged, "x")
    assert os2.sCapHeight == glyph_ink_top(merged, "H")
    # B612's own proportions, not Hack's 0.547/0.729.
    assert os2.sxHeight / upm == pytest.approx(0.560, abs=0.002)
    assert os2.sCapHeight / upm == pytest.approx(0.760, abs=0.002)


def test_derive_os2_metrics_sets_avg_width_and_win_box(b612_regular: TTFont, hack_regular: TTFont):
    """xAvgCharWidth becomes the mean advance; usWin* covers all the ink."""
    merged = merge_glyphs(hack_regular, b612_regular, [(0x41, 0x5A)])

    derive_os2_metrics(merged)

    os2 = merged["OS/2"]
    advances = [aw for aw, _ in merged["hmtx"].metrics.values() if aw > 0]
    assert os2.xAvgCharWidth == round(sum(advances) / len(advances))

    extent = font_ink_extent(merged)
    assert extent is not None
    lowest, highest = extent
    assert os2.usWinAscent >= highest
    assert os2.usWinDescent >= -lowest
    # ...and never tighter than the line box it has to contain.
    assert os2.usWinAscent >= os2.sTypoAscender
    assert os2.usWinDescent >= -os2.sTypoDescender


def test_derive_os2_metrics_is_idempotent(base_font: TTFont):
    """Deriving twice writes the same values — it measures, it does not accumulate."""
    first = derive_os2_metrics(base_font)
    second = derive_os2_metrics(base_font)
    assert first == second
    assert first["sxHeight"] == glyph_ink_top(base_font, "x")
