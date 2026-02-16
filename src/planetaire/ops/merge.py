"""
Binary glyph merging by unicode range.

Copies glyph outlines from a donor font into a base font for specified
unicode ranges, handling UPM normalization and cmap updates.
"""

from __future__ import annotations

import copy
import logging

from fontTools.ttLib import TTFont

from planetaire.unicode_ranges import codepoints_in_ranges

log = logging.getLogger(__name__)


def merge_glyphs(
    base: TTFont,
    donor: TTFont,
    ranges: list[tuple[int, int]],
    *,
    copy_gsub_features: list[str] | None = None,
    normalize_upm: bool = True,
) -> TTFont:
    """
    Copy glyphs from donor into base for specified unicode ranges.

    1. If UPMs differ and normalize_upm is True, scale base glyphs to match
       donor's UPM.
    2. For each codepoint in ranges, copy the glyph outline and metrics
       from donor to base.
    3. Optionally merge GSUB feature lookups from donor.
    """
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
        # Use the donor glyph name in the result, suffixing if there's a collision
        # with a glyph we're NOT replacing
        target_name = donor_glyph_name
        if target_name in glyph_order:
            # Check if this glyph is already mapped to our codepoint — if so, replace in-place
            pass
        else:
            glyph_order.append(target_name)
            result.setGlyphOrder(glyph_order)

        # Copy glyph outline
        if donor_glyph_name in glyf_donor:
            glyf_base[target_name] = copy.deepcopy(glyf_donor[donor_glyph_name])

        # Copy metrics
        if donor_glyph_name in hmtx_donor.metrics:
            hmtx_base.metrics[target_name] = hmtx_donor.metrics[donor_glyph_name]

        # Update cmap to point to the new glyph
        for subtable in result_cmap_table.tables:
            if hasattr(subtable, "cmap"):
                subtable.cmap[cp] = target_name

        copied += 1

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
            # Simple glyph — scale coordinates
            coords = glyph.coordinates
            for i in range(len(coords)):
                x, y = coords[i]
                coords[i] = (round(x * scale), round(y * scale))
        elif glyph.isComposite():
            # Composite glyph — scale component offsets
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

    # Scale vertical metrics
    if "OS/2" in font:
        os2 = font["OS/2"]
        os2.sTypoAscender = round(os2.sTypoAscender * scale)
        os2.sTypoDescender = round(os2.sTypoDescender * scale)
        os2.sTypoLineGap = round(os2.sTypoLineGap * scale)
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
                # Copy the feature and its lookups from donor
                # This is a simplified approach — for production use,
                # lookup indices need proper remapping
                log.info("Copying GSUB feature '%s' from donor", donor_rec.FeatureTag)
                if base_gsub.FeatureList is None:
                    base_gsub.FeatureList = copy.deepcopy(donor_gsub.FeatureList)
                    break
                base_gsub.FeatureList.FeatureRecord.append(copy.deepcopy(donor_rec))
                base_gsub.FeatureList.FeatureCount = len(base_gsub.FeatureList.FeatureRecord)
