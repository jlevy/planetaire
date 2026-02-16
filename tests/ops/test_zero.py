"""Tests for dotted zero insertion."""

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


def _zero_glyph(font: TTFont):
    """Get the zero glyph from a font."""
    cmap = font.getBestCmap()
    return font["glyf"][cmap[0x30]]


class TestDottedZeroToggle:
    """TDD: verify dot is absent without processing and present after."""

    def test_original_b612_zero_has_no_dot(self, b612_regular: TTFont):
        """Original polarsys B612 zero has exactly 2 contours (no dot)."""
        g = _zero_glyph(b612_regular)
        assert g.numberOfContours == 2, (
            f"Original B612 zero should have 2 contours, got {g.numberOfContours}"
        )

    def test_add_dotted_zero_adds_third_contour(self, b612_regular: TTFont):
        """After add_dotted_zero, zero has 3 contours."""
        font = copy.deepcopy(b612_regular)
        add_dotted_zero(font)
        g = _zero_glyph(font)
        assert g.numberOfContours == 3, (
            f"Dotted zero should have 3 contours, got {g.numberOfContours}"
        )

    def test_dot_contour_is_4_point_rectangle(self, b612_regular: TTFont):
        """The rect dot contour should be 4 on-curve points."""
        font = copy.deepcopy(b612_regular)
        add_dotted_zero(font, shape="rect")
        g = _zero_glyph(font)

        dot_start = g.endPtsOfContours[1] + 1
        dot_end = g.endPtsOfContours[2]
        npts = dot_end - dot_start + 1
        assert npts == 4, f"Rect dot should have 4 points, got {npts}"

        for i in range(dot_start, dot_end + 1):
            assert g.flags[i] == 1, f"Point {i} should be on-curve"

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

        assert abs(dot_cx - inner_cx) < 5, (
            f"Dot center x ({dot_cx}) should be near inner counter center x ({inner_cx})"
        )
        assert abs(dot_cy - inner_cy) < 5, (
            f"Dot center y ({dot_cy}) should be near inner counter center y ({inner_cy})"
        )

    def test_no_op_when_already_dotted(self, b612_regular: TTFont):
        """Applying add_dotted_zero twice should not add a second dot."""
        font = copy.deepcopy(b612_regular)
        add_dotted_zero(font)
        assert _zero_glyph(font).numberOfContours == 3

        add_dotted_zero(font)
        assert _zero_glyph(font).numberOfContours == 3

    def test_without_dot_vs_with_dot_differ(self, b612_regular: TTFont):
        """The zero glyph should differ between dotted and undotted versions."""
        undotted = copy.deepcopy(b612_regular)
        dotted = copy.deepcopy(b612_regular)
        add_dotted_zero(dotted)

        g_undotted = _zero_glyph(undotted)
        g_dotted = _zero_glyph(dotted)

        assert g_undotted.numberOfContours == 2
        assert g_dotted.numberOfContours == 3

        # The first two contours should be identical
        for i in range(g_undotted.endPtsOfContours[1] + 1):
            assert g_undotted.coordinates[i] == g_dotted.coordinates[i]
            assert g_undotted.flags[i] == g_dotted.flags[i]


class TestCircleDot:
    """Tests for the circular dot shape."""

    def test_circle_dot_adds_third_contour(self, b612_regular: TTFont):
        """Circle dot should add a third contour."""
        font = copy.deepcopy(b612_regular)
        add_dotted_zero(font, shape="circle")
        g = _zero_glyph(font)
        assert g.numberOfContours == 3

    def test_circle_dot_has_12_points(self, b612_regular: TTFont):
        """Circle dot should have 12 points (4 on-curve + 8 off-curve)."""
        font = copy.deepcopy(b612_regular)
        add_dotted_zero(font, shape="circle")
        g = _zero_glyph(font)

        dot_start = g.endPtsOfContours[1] + 1
        dot_end = g.endPtsOfContours[2]
        npts = dot_end - dot_start + 1
        assert npts == 12, f"Circle dot should have 12 points, got {npts}"

        # Verify flag pattern: on, off, off, on, off, off, on, off, off, on, off, off
        expected_flags = [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0]
        actual_flags = [g.flags[i] for i in range(dot_start, dot_end + 1)]
        assert actual_flags == expected_flags, (
            f"Circle dot flags should be {expected_flags}, got {actual_flags}"
        )

    def test_circle_dot_is_centered(self, b612_regular: TTFont):
        """Circle dot should also be centered in the inner counter."""
        font = copy.deepcopy(b612_regular)
        add_dotted_zero(font, shape="circle")
        g = _zero_glyph(font)

        inner_start = g.endPtsOfContours[0] + 1
        inner_end = g.endPtsOfContours[1]
        inner_xs = [g.coordinates[i][0] for i in range(inner_start, inner_end + 1)]
        inner_ys = [g.coordinates[i][1] for i in range(inner_start, inner_end + 1)]
        inner_cx = (min(inner_xs) + max(inner_xs)) / 2
        inner_cy = (min(inner_ys) + max(inner_ys)) / 2

        dot_start = g.endPtsOfContours[1] + 1
        dot_end = g.endPtsOfContours[2]
        dot_xs = [g.coordinates[i][0] for i in range(dot_start, dot_end + 1)]
        dot_ys = [g.coordinates[i][1] for i in range(dot_start, dot_end + 1)]
        dot_cx = (min(dot_xs) + max(dot_xs)) / 2
        dot_cy = (min(dot_ys) + max(dot_ys)) / 2

        assert abs(dot_cx - inner_cx) < 5
        assert abs(dot_cy - inner_cy) < 5

    def test_rect_and_circle_produce_different_contours(self, b612_regular: TTFont):
        """Rect and circle dots should produce different contours."""
        rect_font = copy.deepcopy(b612_regular)
        circle_font = copy.deepcopy(b612_regular)
        add_dotted_zero(rect_font, shape="rect")
        add_dotted_zero(circle_font, shape="circle")

        g_rect = _zero_glyph(rect_font)
        g_circle = _zero_glyph(circle_font)

        # Both have 3 contours
        assert g_rect.numberOfContours == 3
        assert g_circle.numberOfContours == 3

        # But different number of points in the dot contour
        rect_npts = g_rect.endPtsOfContours[2] - g_rect.endPtsOfContours[1]
        circle_npts = g_circle.endPtsOfContours[2] - g_circle.endPtsOfContours[1]
        assert rect_npts == 4  # rectangle
        assert circle_npts == 12  # circle
