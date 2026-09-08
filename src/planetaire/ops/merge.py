"""
Binary glyph merging by unicode range.

Copies glyph outlines from a donor font into a base font for specified
unicode ranges, handling UPM normalization and cmap updates.

Also derives the OS/2 fields that *measure* the resulting outlines
(`derive_os2_metrics`), which a glyph merge necessarily invalidates.
"""

from __future__ import annotations

import copy
import logging

from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont

from planetaire.unicode_ranges import codepoints_in_ranges

log = logging.getLogger(__name__)

# Reference glyphs for the OpenType definitions of the two OS/2 height fields:
# sxHeight is the top of lowercase "x", sCapHeight the top of uppercase "H".
X_HEIGHT_CHAR = "x"
CAP_HEIGHT_CHAR = "H"


def merge_glyphs(
    base: TTFont,
    donor: TTFont,
    ranges: list[tuple[int, int]],
    *,
    copy_gsub_features: list[str] | None = None,
    normalize_upm: bool = True,
    strip_donor_hinting: bool = True,
) -> TTFont:
    """
    Copy glyphs from donor into base for specified unicode ranges.

    1. If UPMs differ and normalize_upm is True, scale base glyphs to match
       donor's UPM.
    2. For each codepoint in ranges, copy the glyph outline and metrics
       from donor to base.
    3. Optionally merge GSUB feature lookups from donor.

    When ``strip_donor_hinting`` is set (default), TrueType instructions on the
    copied donor glyphs are removed. The base font's global hinting program
    (``prep``/``fpgm``/``cvt``) belongs to the base; running the donor's
    instructions against it would be incorrect, so the donor letters ship
    unhinted (rendered with grayscale antialiasing) while the base's own glyphs
    keep their native, matching hinting.
    """
    from fontTools.ttLib.tables import ttProgram

    result = copy.deepcopy(base)

    donor_upm = donor["head"].unitsPerEm
    base_upm = result["head"].unitsPerEm

    if normalize_upm and base_upm != donor_upm:
        scale_font_upm(result, donor_upm)

    target_cps = codepoints_in_ranges(ranges)
    donor_cmap = donor.getBestCmap() or {}
    result_cmap_table = result["cmap"]

    glyf_base = result["glyf"]
    glyf_donor = donor["glyf"]
    hmtx_base = result["hmtx"]
    hmtx_donor = donor["hmtx"]
    glyph_order = result.getGlyphOrder()

    copied = 0
    for cp in sorted(target_cps):
        if cp not in donor_cmap:
            continue

        donor_glyph_name = donor_cmap[cp]
        # Reuse the donor's glyph name in the result. If the base already has a
        # glyph with this name, its outline/metrics/cmap are overwritten below.
        # This is intentional: e.g. the base "A" is replaced by the donor's "A".
        target_name = donor_glyph_name
        if target_name not in glyph_order:
            glyph_order.append(target_name)

        # Copy glyph outline
        if donor_glyph_name in glyf_donor:
            copied_glyph = copy.deepcopy(glyf_donor[donor_glyph_name])
            if strip_donor_hinting and hasattr(copied_glyph, "program"):
                copied_glyph.program = ttProgram.Program()
                copied_glyph.program.fromBytecode(b"")
            glyf_base[target_name] = copied_glyph

        # Copy metrics
        if donor_glyph_name in hmtx_donor.metrics:
            hmtx_base.metrics[target_name] = hmtx_donor.metrics[donor_glyph_name]

        # Update cmap to point to the new glyph
        for subtable in result_cmap_table.tables:
            if hasattr(subtable, "cmap"):
                subtable.cmap[cp] = target_name

        copied += 1

    result.setGlyphOrder(glyph_order)
    log.info("Copied %d glyphs from donor for %d target codepoints", copied, len(target_cps))

    if copy_gsub_features:
        _merge_gsub_features(result, donor, copy_gsub_features)

    return result


def scale_font_upm(font: TTFont, target_upm: int) -> None:
    """
    Scale all glyph coordinates and metrics in `font` to match `target_upm`.

    This modifies the font in place.
    """
    current_upm = font["head"].unitsPerEm
    if current_upm == target_upm:
        return

    scale = target_upm / current_upm
    log.info("Scaling font UPM from %d to %d (factor %.6f)", current_upm, target_upm, scale)

    # Scale glyph outlines
    glyf = font["glyf"]
    for glyph_name in font.getGlyphOrder():
        if glyph_name not in glyf:
            continue
        glyph = glyf[glyph_name]
        if glyph.numberOfContours > 0:
            # Simple glyph: scale coordinates
            coords = glyph.coordinates
            for i in range(len(coords)):
                x, y = coords[i]
                coords[i] = (round(x * scale), round(y * scale))
        elif glyph.isComposite():
            # Composite glyph: scale component offsets
            for comp in glyph.components:
                if hasattr(comp, "x") and hasattr(comp, "y"):
                    comp.x = round(comp.x * scale)
                    comp.y = round(comp.y * scale)
        # Scale bounding box
        if hasattr(glyph, "xMin"):
            glyph.xMin = round(glyph.xMin * scale)
            glyph.yMin = round(glyph.yMin * scale)
            glyph.xMax = round(glyph.xMax * scale)
            glyph.yMax = round(glyph.yMax * scale)

    # Scale advance widths and LSB
    hmtx = font["hmtx"]
    for glyph_name in hmtx.metrics:
        width, lsb = hmtx.metrics[glyph_name]
        hmtx.metrics[glyph_name] = (round(width * scale), round(lsb * scale))

    # Scale vertical metrics. Every OS/2 field carrying a font-unit measurement
    # has to move with the UPM: leaving any of them behind puts a 2048-unit
    # number in a 2000-unit font, which is how xAvgCharWidth and the usWin pair
    # came to overstate this family's cell and clipping box by 2.4%.
    if "OS/2" in font:
        os2 = font["OS/2"]
        os2.sTypoAscender = round(os2.sTypoAscender * scale)
        os2.sTypoDescender = round(os2.sTypoDescender * scale)
        os2.sTypoLineGap = round(os2.sTypoLineGap * scale)
        os2.xAvgCharWidth = round(os2.xAvgCharWidth * scale)
        os2.usWinAscent = round(os2.usWinAscent * scale)
        os2.usWinDescent = round(os2.usWinDescent * scale)
        if hasattr(os2, "sxHeight"):
            os2.sxHeight = round(os2.sxHeight * scale)
        if hasattr(os2, "sCapHeight"):
            os2.sCapHeight = round(os2.sCapHeight * scale)

    if "hhea" in font:
        hhea = font["hhea"]
        hhea.ascent = round(hhea.ascent * scale)
        hhea.descent = round(hhea.descent * scale)
        hhea.lineGap = round(hhea.lineGap * scale)

    # Update head table UPM
    font["head"].unitsPerEm = target_upm


def glyph_ink_top(font: TTFont, char: str) -> int | None:
    """Top of the drawn ink for `char`, in font units, or None if it draws nothing.

    Uses a pen over the glyph set so composites and the merged donor outlines are
    measured the same way a renderer sees them, rather than trusting a stored
    bounding box that an earlier step may have left stale.
    """
    name = (font.getBestCmap() or {}).get(ord(char))
    if name is None:
        return None
    glyph_set = font.getGlyphSet()
    pen = BoundsPen(glyph_set)
    glyph_set[name].draw(pen)
    # BoundsPen leaves `bounds` as None for a glyph that draws nothing (a space,
    # say). Tested for truth rather than `is None` because the annotation claims a
    # tuple that is always present, and a real bounds tuple is never empty.
    bounds = pen.bounds
    if not bounds:
        return None
    return round(bounds[3])


def font_ink_extent(font: TTFont) -> tuple[int, int] | None:
    """(lowest, highest) drawn y across every glyph, in font units.

    None when the font draws nothing. Bounds are recalculated rather than read,
    for the same reason as `glyph_ink_top`.
    """
    if "glyf" not in font:
        return None
    glyf = font["glyf"]
    lowest: int | None = None
    highest: int | None = None
    for name in font.getGlyphOrder():
        glyph = glyf[name]
        if glyph.numberOfContours == 0:
            continue  # no contours, so no ink (space and friends)
        glyph.recalcBounds(glyf)
        lowest = glyph.yMin if lowest is None else min(lowest, glyph.yMin)
        highest = glyph.yMax if highest is None else max(highest, glyph.yMax)
    if lowest is None or highest is None:
        return None
    return lowest, highest


def derive_os2_metrics(font: TTFont) -> dict[str, int]:
    """Recompute the OS/2 fields that describe the font's own drawn outlines.

    A glyph merge invalidates every OS/2 field that is a *measurement* of the
    glyphs: the table still describes the base font's letters while the outlines
    are now the donor's. Planetaire hits this twice over, because the base and
    donor also disagree about UPM. Deriving the fields from the merged outlines
    makes them right by construction, whatever the sources are.

    Per the OpenType spec:

    - ``sxHeight``: the height of lowercase ``x`` — its ink top.
    - ``sCapHeight``: the height of uppercase ``H`` — its ink top.
    - ``xAvgCharWidth`` (OS/2 v3+): the arithmetic mean of the advance widths of
      all non-zero-width glyphs. Delegated to fontTools, which also implements
      the older weighted definition for v1/v2 tables.
    - ``usWinAscent``/``usWinDescent``: the box outside which Windows clips ink;
      the spec recommends ``head.yMax`` and ``-head.yMin`` so nothing is clipped.
      Held to at least the typographic ascender/descender so the clipping box can
      never be smaller than the line box.

    Line height is untouched: ``sTypo*`` and ``hhea`` are design values, not
    measurements, and every face here sets ``fsSelection`` USE_TYPO_METRICS, so
    modern text stacks lay out from ``sTypo*`` regardless of the usWin pair.

    Must run *after* every step that moves outlines or advances — for this
    pipeline, after `add_dotted_zero` and `normalize_monospace` — so it is the
    last metrics step in a build. Worth running again after subsetting, which
    removes ink and so can shrink the clipping box. Returns the fields it wrote,
    for logging and tests; fields whose reference glyph the subset dropped keep
    the value measured before it.
    """
    if "OS/2" not in font:
        return {}
    os2 = font["OS/2"]
    written: dict[str, int] = {}

    x_top = glyph_ink_top(font, X_HEIGHT_CHAR)
    if x_top is not None and hasattr(os2, "sxHeight"):
        os2.sxHeight = x_top
        written["sxHeight"] = x_top

    cap_top = glyph_ink_top(font, CAP_HEIGHT_CHAR)
    if cap_top is not None and hasattr(os2, "sCapHeight"):
        os2.sCapHeight = cap_top
        written["sCapHeight"] = cap_top

    os2.recalcAvgCharWidth(font)
    written["xAvgCharWidth"] = os2.xAvgCharWidth

    extent = font_ink_extent(font)
    if extent is not None:
        lowest, highest = extent
        os2.usWinAscent = max(highest, os2.sTypoAscender, 0)
        os2.usWinDescent = max(-lowest, -os2.sTypoDescender, 0)
        written["usWinAscent"] = os2.usWinAscent
        written["usWinDescent"] = os2.usWinDescent

    log.info("Derived OS/2 metrics from merged outlines: %s", written)
    return written


def _merge_gsub_features(base: TTFont, donor: TTFont, features: list[str]) -> None:
    """
    Merge specified GSUB feature lookups from donor into base.

    This is a simplified merge that copies entire feature records. For full
    correctness, lookup indices need to be remapped.
    """
    if "GSUB" not in donor:
        return

    donor_gsub = donor["GSUB"].table
    if not donor_gsub.FeatureList:
        return

    if "GSUB" not in base:
        # Copy the entire GSUB table from donor
        base["GSUB"] = copy.deepcopy(donor["GSUB"])
        return

    base_gsub = base["GSUB"].table

    # Find donor features we want to copy
    for donor_rec in donor_gsub.FeatureList.FeatureRecord:
        if donor_rec.FeatureTag in features:
            # Check if base already has this feature
            has_feature = False
            if base_gsub.FeatureList:
                for base_rec in base_gsub.FeatureList.FeatureRecord:
                    if base_rec.FeatureTag == donor_rec.FeatureTag:
                        has_feature = True
                        break

            if not has_feature:
                log.info("Copying GSUB feature '%s' from donor", donor_rec.FeatureTag)
                if base_gsub.FeatureList is None:
                    base_gsub.FeatureList = copy.deepcopy(donor_gsub.FeatureList)
                    break
                # Appending a donor feature record into an existing base GSUB would
                # leave its LookupListIndex values pointing at the donor's lookups,
                # producing a corrupt table. Proper lookup remapping is not yet
                # implemented, so fail loudly rather than ship a broken font.
                # (The Planetaire pipeline does not exercise this path:
                # PLANETAIRE_GSUB_FEATURES is empty.)
                raise NotImplementedError(
                    f"Merging GSUB feature '{donor_rec.FeatureTag}' into a font that "
                    "already has a GSUB table requires lookup-index remapping, which "
                    "is not implemented."
                )
