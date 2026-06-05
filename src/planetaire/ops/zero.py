"""
Add a center dot to the zero glyph for disambiguation from uppercase O.

Creates two glyph variants packaged as OpenType alternates:
  - Default zero: circle dot (smooth Bezier ellipse).
  - ss01 alternate: rectangle dot.

The alternates are accessible via:
  - OpenType ``ss01`` feature (Stylistic Set 1: "Rectangle Zero")
  - OpenType ``zero`` feature (Slashed Zero — wired to the same alternate)

Applications activate these via:
  - Typst: ``#set text(stylistic-set: 1)`` or ``slashed-zero: true``
  - VS Code: ``"editor.fontLigatures": "'ss01'"``
  - Kitty: ``font_features PlanetaireMonoExtended-Regular +ss01``
  - WezTerm: ``harfbuzz_features = { "ss01=1" }``
"""

from __future__ import annotations

import copy
import logging
import math

from fontTools.ttLib import TTFont
from fontTools.ttLib.tables import otTables

log = logging.getLogger(__name__)

# Dot dimensions at 2000 UPM.
_DOT_WIDTH = 221
_DOT_HEIGHT = 348
_REFERENCE_UPM = 2000

# Name for the alternate glyph.
_ALTERNATE_GLYPH_NAME = "zero.ss01"


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

    Uses the standard 12-point approximation: 4 on-curve points at the
    cardinal positions and 8 off-curve control points (2 per arc segment).
    The off-curve factor (tan(pi/8) ~ 0.4142) gives a good circle
    approximation with quadratic splines.
    """
    k = math.tan(math.pi / 8)
    kw = round(half_w * k)
    kh = round(half_h * k)

    coords = [
        (cx, cy + half_h),  # top (on-curve)
        (cx + kw, cy + half_h),  # top-right (off-curve)
        (cx + half_w, cy + kh),  # right-top (off-curve)
        (cx + half_w, cy),  # right (on-curve)
        (cx + half_w, cy - kh),  # right-bottom (off-curve)
        (cx + kw, cy - half_h),  # bottom-right (off-curve)
        (cx, cy - half_h),  # bottom (on-curve)
        (cx - kw, cy - half_h),  # bottom-left (off-curve)
        (cx - half_w, cy - kh),  # left-bottom (off-curve)
        (cx - half_w, cy),  # left (on-curve)
        (cx - half_w, cy + kh),  # left-top (off-curve)
        (cx - kw, cy + half_h),  # top-left (off-curve)
    ]
    # on, off, off, on, off, off, on, off, off, on, off, off
    flags = [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0]
    return coords, flags


def _compute_dot_params(font: TTFont, glyph):
    """Compute the center and half-dimensions for the dot."""
    inner_start = glyph.endPtsOfContours[0] + 1
    inner_end = glyph.endPtsOfContours[1]
    inner_xs = [glyph.coordinates[i][0] for i in range(inner_start, inner_end + 1)]
    inner_ys = [glyph.coordinates[i][1] for i in range(inner_start, inner_end + 1)]
    cx = (min(inner_xs) + max(inner_xs)) // 2
    cy = (min(inner_ys) + max(inner_ys)) // 2

    upm = font["head"].unitsPerEm
    scale = upm / _REFERENCE_UPM
    half_w = round(_DOT_WIDTH * scale / 2)
    half_h = round(_DOT_HEIGHT * scale / 2)
    return cx, cy, half_w, half_h


def _append_dot_contour(glyph, coords, flags):
    """Append a dot contour to an existing glyph."""
    existing_coords = list(glyph.coordinates)
    existing_flags = list(glyph.flags)
    existing_ends = list(glyph.endPtsOfContours)

    new_start = existing_ends[-1] + 1
    existing_coords.extend(coords)
    existing_flags.extend(flags)
    existing_ends.append(new_start + len(coords) - 1)

    glyph.coordinates = type(glyph.coordinates)(existing_coords)
    glyph.flags = type(glyph.flags)(existing_flags)
    glyph.endPtsOfContours = existing_ends
    glyph.numberOfContours = len(existing_ends)


def _add_alternate_glyph(font: TTFont, zero_name: str, cx, cy, half_w, half_h):
    """Create the alternate zero glyph (zero.ss01) with a rectangle dot.

    Copies the original 2-contour zero and adds the rectangle dot contour.
    Returns the alternate glyph name.
    """
    glyf = font["glyf"]
    original = glyf[zero_name]

    # Deep-copy the original glyph (before the circle dot was added).
    # We need the raw 2-contour zero. If it already has 3 contours (circle
    # was already added), we take just the first 2 contours.
    alt = copy.deepcopy(original)

    if alt.numberOfContours > 2:
        # Strip back to 2 contours (the oval without any dot).
        end_of_contour_1 = alt.endPtsOfContours[1]
        alt.coordinates = type(alt.coordinates)(list(alt.coordinates)[: end_of_contour_1 + 1])
        alt.flags = type(alt.flags)(list(alt.flags)[: end_of_contour_1 + 1])
        alt.endPtsOfContours = alt.endPtsOfContours[:2]
        alt.numberOfContours = 2

    # Add rectangle dot to the alternate.
    rect_coords, rect_flags = _rect_contour(cx, cy, half_w, half_h)
    _append_dot_contour(alt, rect_coords, rect_flags)

    # Insert the alternate glyph into the font.
    glyf[_ALTERNATE_GLYPH_NAME] = alt

    # Add to glyph order (after the original zero).
    glyph_order = font.getGlyphOrder()
    if _ALTERNATE_GLYPH_NAME not in glyph_order:
        zero_idx = glyph_order.index(zero_name)
        glyph_order.insert(zero_idx + 1, _ALTERNATE_GLYPH_NAME)
        font.setGlyphOrder(glyph_order)

    # Copy metrics from the original zero.
    if "hmtx" in font:
        font["hmtx"][_ALTERNATE_GLYPH_NAME] = font["hmtx"][zero_name]

    log.info("Created alternate glyph '%s' with rectangle dot", _ALTERNATE_GLYPH_NAME)
    return _ALTERNATE_GLYPH_NAME


def _add_gsub_features(font: TTFont, zero_name: str, alt_name: str):
    """Add ss01 and zero GSUB features mapping zero -> zero.ss01.

    Surgically appends to the existing GSUB table without disturbing
    existing features (aalt, frac, subs, sups, etc.).
    """
    gsub = font["GSUB"].table

    # Build SingleSubst lookup: zero -> zero.ss01
    single_subst = otTables.SingleSubst()
    single_subst.mapping = {zero_name: alt_name}

    lookup = otTables.Lookup()
    lookup.LookupType = 1  # Single Substitution
    lookup.LookupFlag = 0
    lookup.SubTable = [single_subst]
    lookup.SubTableCount = 1

    lookup_index = len(gsub.LookupList.Lookup)
    gsub.LookupList.Lookup.append(lookup)

    # Create feature records for ss01 and zero, sharing the same lookup.
    new_feature_indices = []
    for tag in ("ss01", "zero"):
        frec = otTables.FeatureRecord()
        frec.FeatureTag = tag
        frec.Feature = otTables.Feature()
        frec.Feature.FeatureParams = None
        frec.Feature.LookupListIndex = [lookup_index]
        frec.Feature.LookupCount = 1
        gsub.FeatureList.FeatureRecord.append(frec)
        new_feature_indices.append(len(gsub.FeatureList.FeatureRecord) - 1)

    # Wire the new features into all script/language records.
    for srec in gsub.ScriptList.ScriptRecord:
        if srec.Script.DefaultLangSys:
            srec.Script.DefaultLangSys.FeatureIndex.extend(new_feature_indices)
        for lr in srec.Script.LangSysRecord:
            if lr.LangSys:
                lr.LangSys.FeatureIndex.extend(new_feature_indices)

    log.info(
        "Added GSUB features ss01 and zero (lookup %d): %s -> %s",
        lookup_index,
        zero_name,
        alt_name,
    )


def add_dotted_zero(font: TTFont) -> TTFont:
    """Add circle-dot zero (default) and rect-dot zero (ss01 alternate).

    This is the main entry point. It:
    1. Adds a circle dot to the default zero glyph.
    2. Creates an alternate glyph ``zero.ss01`` with a rectangle dot.
    3. Adds GSUB ``ss01`` and ``zero`` features for the alternate.

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

    # Compute dot placement parameters from the undotted zero.
    cx, cy, half_w, half_h = _compute_dot_params(font, glyph)

    # 1. Create the alternate glyph FIRST (before modifying the original),
    #    so it gets a clean copy of the 2-contour zero.
    alt_name = _add_alternate_glyph(font, zero_name, cx, cy, half_w, half_h)

    # 2. Add circle dot to the default zero.
    circle_coords, circle_flags = _circle_contour(cx, cy, half_w, half_h)
    _append_dot_contour(glyph, circle_coords, circle_flags)
    log.info(
        "Added circle center dot to zero glyph '%s' at (%d,%d) size %dx%d",
        zero_name,
        cx - half_w,
        cy - half_h,
        half_w * 2,
        half_h * 2,
    )

    # 3. Add GSUB features.
    if "GSUB" in font:
        _add_gsub_features(font, zero_name, alt_name)

    return font
