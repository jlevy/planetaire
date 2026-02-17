"""Tests for dotted zero insertion with OpenType alternates."""

from __future__ import annotations

import copy
from pathlib import Path

import pytest
from fontTools.ttLib import TTFont

from planetaire.ops.zero import add_dotted_zero

FONTS_SOURCE = Path(__file__).parent.parent.parent / "fonts" / "source"


@pytest.fixture
def b612_regular() -> TTFont:
    path = FONTS_SOURCE / "b612" / "B612Mono-Regular.ttf"
    if not path.exists():
        pytest.skip("B612 source font not available")
    return TTFont(path)


@pytest.fixture
def hack_regular() -> TTFont:
    """Hack font with full GSUB table (for testing feature wiring)."""
    path = FONTS_SOURCE / "hack" / "HackNerdFont-Regular.ttf"
    if not path.exists():
        pytest.skip("Hack source font not available")
    return TTFont(path)


@pytest.fixture
def merged_font(hack_regular: TTFont, b612_regular: TTFont) -> TTFont:
    """A merged font with B612 digits and Hack GSUB (mimics pipeline output)."""
    from planetaire.config import PLANETAIRE_LETTER_RANGES
    from planetaire.ops.merge import merge_glyphs

    return merge_glyphs(hack_regular, b612_regular, PLANETAIRE_LETTER_RANGES)


def _zero_glyph(font: TTFont):
    """Get the zero glyph from a font."""
    cmap = font.getBestCmap()
    assert cmap is not None
    return font["glyf"][cmap[0x30]]


def _dot_contour_info(glyph):
    """Return (num_points, num_oncurve) for the third contour (the dot)."""
    dot_start = glyph.endPtsOfContours[1] + 1
    dot_end = glyph.endPtsOfContours[2]
    npts = dot_end - dot_start + 1
    oncurve = sum(1 for j in range(dot_start, dot_end + 1) if glyph.flags[j] == 1)
    return npts, oncurve


class TestDottedZeroBasics:
    """Verify dot insertion on the B612 zero glyph."""

    def test_original_b612_zero_has_no_dot(self, b612_regular: TTFont):
        """Original polarsys B612 zero has exactly 2 contours (no dot)."""
        g = _zero_glyph(b612_regular)
        assert g.numberOfContours == 2

    def test_add_dotted_zero_adds_third_contour(self, b612_regular: TTFont):
        """After add_dotted_zero, zero has 3 contours."""
        font = copy.deepcopy(b612_regular)
        add_dotted_zero(font)
        g = _zero_glyph(font)
        assert g.numberOfContours == 3

    def test_default_dot_is_circle(self, b612_regular: TTFont):
        """The default zero dot should be a 12-point circle."""
        font = copy.deepcopy(b612_regular)
        add_dotted_zero(font)
        g = _zero_glyph(font)
        npts, oncurve = _dot_contour_info(g)
        assert npts == 12, f"Circle dot should have 12 points, got {npts}"
        assert oncurve == 4, f"Circle dot should have 4 on-curve points, got {oncurve}"

    def test_dot_is_centered_in_inner_counter(self, b612_regular: TTFont):
        """The dot should be approximately centered in the zero's inner counter."""
        font = copy.deepcopy(b612_regular)
        add_dotted_zero(font)
        g = _zero_glyph(font)

        # Inner counter (contour 1)
        inner_start = g.endPtsOfContours[0] + 1
        inner_end = g.endPtsOfContours[1]
        inner_xs = [g.coordinates[i][0] for i in range(inner_start, inner_end + 1)]
        inner_ys = [g.coordinates[i][1] for i in range(inner_start, inner_end + 1)]
        inner_cx = (min(inner_xs) + max(inner_xs)) / 2
        inner_cy = (min(inner_ys) + max(inner_ys)) / 2

        # Dot (contour 2)
        dot_start = g.endPtsOfContours[1] + 1
        dot_end = g.endPtsOfContours[2]
        dot_xs = [g.coordinates[i][0] for i in range(dot_start, dot_end + 1)]
        dot_ys = [g.coordinates[i][1] for i in range(dot_start, dot_end + 1)]
        dot_cx = (min(dot_xs) + max(dot_xs)) / 2
        dot_cy = (min(dot_ys) + max(dot_ys)) / 2

        assert abs(dot_cx - inner_cx) < 5
        assert abs(dot_cy - inner_cy) < 5

    def test_no_op_when_already_dotted(self, b612_regular: TTFont):
        """Applying add_dotted_zero twice should not add a second dot."""
        font = copy.deepcopy(b612_regular)
        add_dotted_zero(font)
        assert _zero_glyph(font).numberOfContours == 3

        add_dotted_zero(font)
        assert _zero_glyph(font).numberOfContours == 3


class TestAlternateGlyph:
    """Tests for the zero.ss01 alternate glyph."""

    def test_alternate_glyph_exists(self, b612_regular: TTFont):
        """After add_dotted_zero, zero.ss01 should exist in the font."""
        font = copy.deepcopy(b612_regular)
        add_dotted_zero(font)
        assert "zero.ss01" in font["glyf"]
        assert "zero.ss01" in font.getGlyphOrder()

    def test_alternate_has_rectangle_dot(self, b612_regular: TTFont):
        """The alternate glyph should have a 4-point rectangle dot."""
        font = copy.deepcopy(b612_regular)
        add_dotted_zero(font)
        alt = font["glyf"]["zero.ss01"]
        assert alt.numberOfContours == 3
        npts, oncurve = _dot_contour_info(alt)
        assert npts == 4, f"Rect dot should have 4 points, got {npts}"
        assert oncurve == 4, "All rect dot points should be on-curve"

    def test_alternate_metrics_match_default(self, b612_regular: TTFont):
        """The alternate should have the same horizontal metrics as the default."""
        font = copy.deepcopy(b612_regular)
        # Need hmtx table for this test
        if "hmtx" not in font:
            pytest.skip("Font has no hmtx table")
        add_dotted_zero(font)
        cmap = font.getBestCmap()
        assert cmap is not None
        zero_name = cmap[0x30]
        assert font["hmtx"][zero_name] == font["hmtx"]["zero.ss01"]

    def test_default_and_alternate_have_different_dots(self, b612_regular: TTFont):
        """Default (circle) and alternate (rect) should have different dot contours."""
        font = copy.deepcopy(b612_regular)
        add_dotted_zero(font)

        default = _zero_glyph(font)
        alt = font["glyf"]["zero.ss01"]

        default_npts, _ = _dot_contour_info(default)
        alt_npts, _ = _dot_contour_info(alt)

        assert default_npts == 12  # circle
        assert alt_npts == 4  # rectangle

    def test_first_two_contours_match(self, b612_regular: TTFont):
        """The oval contours (0, 1) should be identical between default and alternate."""
        font = copy.deepcopy(b612_regular)
        add_dotted_zero(font)

        default = _zero_glyph(font)
        alt = font["glyf"]["zero.ss01"]

        # Both should share the first two contours
        end_of_contour_1 = default.endPtsOfContours[1]
        for i in range(end_of_contour_1 + 1):
            assert default.coordinates[i] == alt.coordinates[i]
            assert default.flags[i] == alt.flags[i]


class TestGSUBFeatures:
    """Tests for GSUB ss01 and zero feature wiring."""

    def test_gsub_features_added_with_gsub_table(self, merged_font: TTFont):
        """When font has GSUB, ss01 and zero features should be added."""
        add_dotted_zero(merged_font)
        gsub = merged_font["GSUB"].table
        tags = [fr.FeatureTag for fr in gsub.FeatureList.FeatureRecord]
        assert "ss01" in tags
        assert "zero" in tags

    def test_gsub_features_share_lookup(self, merged_font: TTFont):
        """ss01 and zero should share the same lookup index."""
        add_dotted_zero(merged_font)
        gsub = merged_font["GSUB"].table

        ss01_lookups = None
        zero_lookups = None
        for fr in gsub.FeatureList.FeatureRecord:
            if fr.FeatureTag == "ss01":
                ss01_lookups = fr.Feature.LookupListIndex
            elif fr.FeatureTag == "zero":
                zero_lookups = fr.Feature.LookupListIndex

        assert ss01_lookups is not None
        assert zero_lookups is not None
        assert ss01_lookups == zero_lookups

    def test_gsub_lookup_maps_zero_to_alternate(self, merged_font: TTFont):
        """The shared lookup should map zero -> zero.ss01."""
        add_dotted_zero(merged_font)
        gsub = merged_font["GSUB"].table

        # Find the ss01 lookup index
        lookup_idx = None
        for fr in gsub.FeatureList.FeatureRecord:
            if fr.FeatureTag == "ss01":
                lookup_idx = fr.Feature.LookupListIndex[0]
                break
        assert lookup_idx is not None

        lookup = gsub.LookupList.Lookup[lookup_idx]
        assert lookup.LookupType == 1  # SingleSubst
        assert lookup.SubTable[0].mapping == {"zero": "zero.ss01"}

    def test_features_wired_to_dflt_script(self, merged_font: TTFont):
        """ss01 and zero should be registered in the DFLT script."""
        add_dotted_zero(merged_font)
        gsub = merged_font["GSUB"].table

        # Get feature indices for ss01 and zero
        feature_indices = set()
        for i, fr in enumerate(gsub.FeatureList.FeatureRecord):
            if fr.FeatureTag in ("ss01", "zero"):
                feature_indices.add(i)

        # Check DFLT script has them
        for srec in gsub.ScriptList.ScriptRecord:
            if srec.ScriptTag == "DFLT":
                assert feature_indices.issubset(set(srec.Script.DefaultLangSys.FeatureIndex)), (
                    "ss01/zero features not wired to DFLT script"
                )
                break
        else:
            pytest.fail("No DFLT script found")

    def test_no_gsub_features_without_gsub_table(self, b612_regular: TTFont):
        """When font has no GSUB table, should still add dots without error."""
        font = copy.deepcopy(b612_regular)
        if "GSUB" in font:
            del font["GSUB"]
        add_dotted_zero(font)
        # Default zero should still get a circle dot
        g = _zero_glyph(font)
        assert g.numberOfContours == 3
        # Alternate should still exist
        assert "zero.ss01" in font["glyf"]
