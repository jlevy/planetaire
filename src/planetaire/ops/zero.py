"""
Add a center dot to the zero glyph for disambiguation from uppercase O.

Supports two dot shapes:
  - "rect": A filled rectangle (matching the carlosedp B612 fork).
  - "circle": A filled circle approximated with quadratic Bezier curves.

The original polarsys B612 zero is an empty oval; this post-processing
step adds the distinguishing dot.
"""

from __future__ import annotations

import logging
import math
from typing import Literal

from fontTools.ttLib import TTFont

log = logging.getLogger(__name__)

# Dot dimensions at 2000 UPM, matching the carlosedp reference.
_DOT_WIDTH = 221
_DOT_HEIGHT = 348
_REFERENCE_UPM = 2000

DotShape = Literal["rect", "circle"]


def _rect_contour(
    cx: int, cy: int, half_w: int, half_h: int
) -> tuple[list[tuple[int, int]], list[int]]:
    """Generate a rectangular dot contour (4 on-curve points)."""
    coords = [
        (cx - half_w, cy + half_h),
        (cx + half_w, cy + half_h),
        (cx + half_w, cy - half_h),
        (cx - half_w, cy - half_h),
    ]
    flags = [1, 1, 1, 1]  # All on-curve
    return coords, flags


def _circle_contour(
    cx: int, cy: int, half_w: int, half_h: int
) -> tuple[list[tuple[int, int]], list[int]]:
    """Generate a circular/elliptical dot using TrueType quadratic Bezier curves.

    Uses the standard 8-point approximation: 4 on-curve points at the
    cardinal positions and 4 off-curve control points at the diagonals.
    The off-curve factor (tan(pi/8) ≈ 0.4142) gives a good circle
    approximation with quadratic splines.
    """
    # For a TrueType circle: on-curve at N/S/E/W, off-curve at diagonals.
    # The control point distance is r * tan(pi/8) ≈ 0.4142 * r from the
    # on-curve point, which is the standard quadratic Bezier circle approx.
    k = math.tan(math.pi / 8)
    kw = round(half_w * k)
    kh = round(half_h * k)

    # 8 points: alternating on-curve (1) and off-curve (0), starting at top.
    coords = [
        (cx, cy + half_h),          # top (on-curve)
        (cx + kw, cy + half_h),     # top-right (off-curve)
        (cx + half_w, cy + kh),     # right-top (off-curve)
        (cx + half_w, cy),          # right (on-curve)
        (cx + half_w, cy - kh),     # right-bottom (off-curve)
        (cx + kw, cy - half_h),     # bottom-right (off-curve)
        (cx, cy - half_h),          # bottom (on-curve)
        (cx - kw, cy - half_h),     # bottom-left (off-curve)
        (cx - half_w, cy - kh),     # left-bottom (off-curve)
        (cx - half_w, cy),          # left (on-curve)
        (cx - half_w, cy + kh),     # left-top (off-curve)
        (cx - kw, cy + half_h),     # top-left (off-curve)
    ]
    # on, off, off, on, off, off, on, off, off, on, off, off
    flags = [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0]
    return coords, flags


def add_dotted_zero(font: TTFont, shape: DotShape = "rect") -> TTFont:
    """
    Add a center dot contour to the zero glyph.

    Finds the zero glyph via cmap, calculates the center of its inner
    counter (contour 1), and appends a dot contour of the specified shape.

    If the zero already has 3+ contours (dot already present), this is
    a no-op.

    Args:
        font: The font to modify.
        shape: Dot shape - "rect" for rectangle, "circle" for circle.
    """
    cmap = font.getBestCmap()
    if not cmap or 0x30 not in cmap:
        log.warning("No zero glyph found in cmap; skipping dotted zero")
        return font

    zero_name = cmap[0x30]
    glyf = font["glyf"]
    if zero_name not in glyf:
        log.warning("Zero glyph '%s' not in glyf table; skipping", zero_name)
        return font

    glyph = glyf[zero_name]

    if glyph.numberOfContours != 2:
        log.info(
            "Zero glyph '%s' has %d contours (expected 2); skipping dot insertion",
            zero_name,
            glyph.numberOfContours,
        )
        return font

    # Calculate center of inner counter (contour 1).
    inner_start = glyph.endPtsOfContours[0] + 1
    inner_end = glyph.endPtsOfContours[1]
    inner_xs = [glyph.coordinates[i][0] for i in range(inner_start, inner_end + 1)]
    inner_ys = [glyph.coordinates[i][1] for i in range(inner_start, inner_end + 1)]
    cx = (min(inner_xs) + max(inner_xs)) // 2
    cy = (min(inner_ys) + max(inner_ys)) // 2

    # Scale dot dimensions for the font's UPM.
    upm = font["head"].unitsPerEm
    scale = upm / _REFERENCE_UPM
    half_w = round(_DOT_WIDTH * scale / 2)
    half_h = round(_DOT_HEIGHT * scale / 2)

    # Generate dot contour based on shape.
    if shape == "circle":
        dot_coords, dot_flags = _circle_contour(cx, cy, half_w, half_h)
    else:
        dot_coords, dot_flags = _rect_contour(cx, cy, half_w, half_h)

    # Append the dot contour to the existing glyph.
    existing_coords = list(glyph.coordinates)
    existing_flags = list(glyph.flags)
    existing_ends = list(glyph.endPtsOfContours)

    new_start = existing_ends[-1] + 1
    for coord in dot_coords:
        existing_coords.append(coord)
    existing_flags.extend(dot_flags)
    existing_ends.append(new_start + len(dot_coords) - 1)

    glyph.coordinates = type(glyph.coordinates)(existing_coords)
    glyph.flags = type(glyph.flags)(existing_flags)
    glyph.endPtsOfContours = existing_ends
    glyph.numberOfContours = len(existing_ends)

    log.info(
        "Added %s center dot to zero glyph '%s' at (%d,%d) size %dx%d",
        shape,
        zero_name,
        cx - half_w,
        cy - half_h,
        half_w * 2,
        half_h * 2,
    )

    return font
