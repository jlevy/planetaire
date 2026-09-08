"""Tests for ops/merge — binary glyph merging by unicode range."""

from __future__ import annotations

import pytest
from fontTools.ttLib import TTFont

from planetaire.ops.merge import (
    WinBox,
    apply_win_box,
    derive_os2_metrics,
    family_win_box,
    font_ink_extent,
    font_win_box,
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


def test_font_ink_extent_leaves_the_font_alone(b612_regular: TTFont, hack_regular: TTFont):
    """Measuring is read-only: the stored glyf bounding boxes are not rewritten.

    Regression for P26-R4. `validate` measures through this function, and a
    read-only inspection command must not rewrite the font it inspects.
    """
    merged = merge_glyphs(hack_regular, b612_regular, [(0x41, 0x5A), (0x61, 0x7A)])
    glyf = merged["glyf"]
    names = merged.getGlyphOrder()
    before = [(glyf[n].numberOfContours, getattr(glyf[n], "yMin", None)) for n in names]

    assert font_ink_extent(merged) is not None

    after = [(glyf[n].numberOfContours, getattr(glyf[n], "yMin", None)) for n in names]
    assert after == before


def test_font_win_box_is_the_faces_ink_floored_at_the_line_box(base_font: TTFont):
    """One face's box covers its ink and never sits inside the typographic line box."""
    box = font_win_box(base_font)
    assert box is not None
    extent = font_ink_extent(base_font)
    assert extent is not None
    lowest, highest = extent
    assert box.ascent >= highest
    assert box.descent >= -lowest
    assert box.ascent >= base_font["OS/2"].sTypoAscender
    assert box.descent >= -base_font["OS/2"].sTypoDescender


def test_family_win_box_encloses_every_face(make_font):
    """The family box is the max over the faces, not any one face's own extent.

    Regression for P26-R1: deriving per file gave one family's weights different
    `usWin` boxes, and so different default line spacing on the stacks that
    ignore USE_TYPO_METRICS.
    """
    short = make_font(family="Short", ink_top=700)
    tall = make_font(family="Tall", ink_top=1500)

    assert font_win_box(short) != font_win_box(tall)

    box = family_win_box([short, tall])
    assert box is not None
    assert box.ascent == 1500  # the tall face, not the short one
    assert box == family_win_box([tall, short])  # order does not matter


def test_apply_win_box_makes_a_subset_declare_its_familys_box(make_font):
    """A subset keeps the family box even though its own ink would allow less.

    The `usWin` pair is a clipping box: it only has to avoid cutting ink off, so
    shrinking it to a script subset's smaller ink buys nothing and costs the
    family its uniform line spacing.
    """
    face = make_font(family="Face", ink_top=1500)
    subset = make_font(family="Face", ink_top=700)  # one script's worth of ink
    box = family_win_box([face, subset])
    assert box is not None

    apply_win_box(subset, box)

    os2 = subset["OS/2"]
    assert (os2.usWinAscent, os2.usWinDescent) == (box.ascent, box.descent)
    assert os2.usWinAscent > 700  # roomier than this file's own ink, deliberately


def test_derive_os2_metrics_takes_a_family_box_but_measures_the_rest_per_face(make_font):
    """`win_box` overrides only the clipping box; the height fields stay per face."""
    face = make_font(family="Face", ink_top=900)
    family_box = WinBox(ascent=1800, descent=400)

    written = derive_os2_metrics(face, win_box=family_box)

    assert (written["usWinAscent"], written["usWinDescent"]) == (1800, 400)
    # Measured off this face's own outlines, not inherited from the family.
    assert written["sxHeight"] == glyph_ink_top(face, "x") == 900
    assert written["sCapHeight"] == glyph_ink_top(face, "H") == 900
