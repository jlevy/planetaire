"""
Add a center dot to the zero glyph for disambiguation from uppercase O.

Replicates the dotted zero from the carlosedp B612 fork: a small filled
rectangle centered in the zero's inner counter. The original polarsys B612
zero is an empty oval; this post-processing step adds the distinguishing dot.
"""

from __future__ import annotations

import logging

from fontTools.ttLib import TTFont

log = logging.getLogger(__name__)

# Dot dimensions at 2000 UPM, matching the carlosedp reference.
# The dot is a 221x348 rectangle centered in the inner counter.
_DOT_WIDTH = 221
_DOT_HEIGHT = 348
_REFERENCE_UPM = 2000


def add_dotted_zero(font: TTFont) -> TTFont:
    """
    Add a center dot contour to the zero glyph.

    Finds the zero glyph via cmap, calculates the center of its inner
    counter (contour 1), and appends a rectangular dot contour.

    If the zero already has 3+ contours (dot already present), this is
    a no-op.
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

    # Dot rectangle corners (clockwise from top-left).
    dot_coords = [
        (cx - half_w, cy + half_h),
        (cx + half_w, cy + half_h),
        (cx + half_w, cy - half_h),
        (cx - half_w, cy - half_h),
    ]

    # Append the dot contour to the existing glyph.
    from fontTools.pens.pointPen import PointToSegmentPen
    from fontTools.ttLib.tables._g_l_y_f import Glyph as TTGlyph

    existing_coords = list(glyph.coordinates)
    existing_flags = list(glyph.flags)
    existing_ends = list(glyph.endPtsOfContours)

    # Add dot points (all on-curve, flag=1).
    new_start = existing_ends[-1] + 1
    for coord in dot_coords:
        existing_coords.append(coord)
        existing_flags.append(1)
    existing_ends.append(new_start + len(dot_coords) - 1)

    glyph.coordinates = type(glyph.coordinates)(existing_coords)
    glyph.flags = type(glyph.flags)(existing_flags)
    glyph.endPtsOfContours = existing_ends
    glyph.numberOfContours = len(existing_ends)

    log.info(
        "Added center dot to zero glyph '%s' at (%d,%d) size %dx%d",
        zero_name,
        cx - half_w,
        cy - half_h,
        half_w * 2,
        half_h * 2,
    )

    return font
