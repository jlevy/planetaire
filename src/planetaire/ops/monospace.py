"""
Monospace invariants: check and enforce a single advance width.

Planetaire Mono merges B612 letters (designed on a 1300-unit cell at UPM 2000)
into the Hack Nerd Font base (1204-unit cell after UPM normalization). On its
own the merge copies each source's advance verbatim, so the result is *not*
monospace: letters end up 1300 wide while punctuation, symbols, box-drawing,
powerline, and icons stay 1204. FontForge emboldening makes it worse, inflating
the Medium/ExtraBold letters to 1360-1420 and non-uniformly (e.g. m wider than
A).

`check_monospace` reports any deviation from a single cell width (the core
monospace invariant) plus glyphs whose ink would bleed past the cell.
`normalize_monospace` enforces the invariant: it pins every non-zero-width
glyph whose advance differs from the cell to the cell width, recentering its
ink and -- only when the ink would otherwise overflow -- condensing it just
enough to avoid a bleed/clip. Glyphs already at the cell width (the Hack base,
including the width-critical box-drawing and powerline glyphs) are left exactly
as-is. Zero-width glyphs (combining marks) are also left alone.
"""

from __future__ import annotations

import logging
from collections import Counter
from dataclasses import dataclass, field

from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont

log = logging.getLogger(__name__)

# Minimum side bearing (font units) to keep when condensing an overflowing
# glyph, so ink never sits exactly on -- or past -- the cell edge.
_CONDENSE_MARGIN = 12

# Unicode ranges of "text / coding" glyphs that must sit cleanly inside the
# cell. Box-drawing, block elements, powerline, Braille, and Private-Use icons
# are intentionally cell-filling (they tile, so ink on/over the edge is correct)
# and are excluded from the ink-bleed check.
_TEXT_RANGES = (
    (0x0021, 0x007E),  # ASCII printable
    (0x00A0, 0x017F),  # Latin-1 + Latin Extended-A
    (0x0180, 0x024F),  # Latin Extended-B
    (0x0250, 0x02AF),  # IPA Extensions
    (0x0300, 0x036F),  # Combining marks (checked for completeness)
    (0x0370, 0x03FF),  # Greek
    (0x0400, 0x04FF),  # Cyrillic
    (0x1E00, 0x1EFF),  # Latin Extended Additional
)


def _is_text_codepoint(cp: int) -> bool:
    return any(lo <= cp <= hi for lo, hi in _TEXT_RANGES)


@dataclass
class MonospaceReport:
    """Result of checking the single-advance-width invariant."""

    cell_width: int
    total: int = 0
    zero_width: int = 0
    # (glyph_name, advance) for every non-zero glyph whose advance != cell_width
    nonuniform: list[tuple[str, int]] = field(default_factory=list)
    # (glyph_name, advance, xMin, xMax) for glyphs whose ink exceeds [0, cell]
    bleed: list[tuple[str, int, int, int]] = field(default_factory=list)

    @property
    def is_monospace(self) -> bool:
        return not self.nonuniform

    def summary(self) -> str:
        lines = [
            f"cell width: {self.cell_width}",
            f"glyphs: {self.total} ({self.zero_width} zero-width / marks)",
            f"non-uniform advances: {len(self.nonuniform)}",
            f"ink bleeding past cell: {len(self.bleed)}",
        ]
        if self.nonuniform:
            widths = Counter(aw for _, aw in self.nonuniform)
            lines.append(f"  offending widths: {dict(sorted(widths.items()))}")
        return "\n".join(lines)


def cell_width(font: TTFont) -> int:
    """The canonical cell width: the most common non-zero advance width."""
    hmtx = font["hmtx"]
    widths = Counter(aw for aw, _ in (hmtx[g] for g in font.getGlyphOrder()) if aw > 0)
    if not widths:
        raise ValueError("font has no positive advance widths")
    return widths.most_common(1)[0][0]


def check_monospace(
    font: TTFont, target: int | None = None, *, bleed_tolerance: int = 40
) -> MonospaceReport:
    """Check the single-advance-width invariant and ink-within-cell.

    Args:
        font: the font to inspect.
        target: expected cell width; defaults to the most common advance.
        bleed_tolerance: ink may extend this many units past the cell before it
            is reported (absorbs italic slant and minor symbol overshoot).
    """
    cell = target if target is not None else cell_width(font)
    hmtx = font["hmtx"]
    glyf = font["glyf"]
    # Map glyph name -> codepoint so the ink-bleed check can be scoped to text
    # glyphs. Cell-filling box-drawing/powerline/icons are excluded by design;
    # combining marks (0x300-0x36F) legitimately extend outside the cell.
    text_glyphs = {
        name
        for cp, name in (font.getBestCmap() or {}).items()
        if _is_text_codepoint(cp) and not (0x0300 <= cp <= 0x036F)
    }
    report = MonospaceReport(cell_width=cell)
    for name in font.getGlyphOrder():
        report.total += 1
        adv = hmtx[name][0]
        if adv == 0:
            report.zero_width += 1
            continue
        if adv % cell != 0:
            # Advances must be the cell or an exact integer multiple (a font may
            # carry intentional double-width glyphs, e.g. Roman numerals).
            report.nonuniform.append((name, adv))
        if name in text_glyphs:
            g = glyf[name]
            if g.numberOfContours != 0:
                g.recalcBounds(glyf)
                if g.xMin < -bleed_tolerance or g.xMax > cell + bleed_tolerance:
                    report.bleed.append((name, adv, g.xMin, g.xMax))
    return report


def _ink_bounds(glyf, name: str) -> tuple[int, int] | None:
    g = glyf[name]
    if g.numberOfContours == 0:
        return None
    g.recalcBounds(glyf)
    return g.xMin, g.xMax


def normalize_monospace(
    font: TTFont,
    target: int | None = None,
    *,
    fit_overflow: bool = True,
) -> dict[str, int]:
    """Force every non-zero glyph to a single cell width.

    Only glyphs whose advance differs from the cell are touched; glyphs already
    at the cell width (the Hack base, box-drawing, powerline, icons) are left
    untouched. Touched glyphs are recentered in the cell; if their ink would
    overflow, they are condensed horizontally just enough to fit.

    Donor (B612) letters are merged unhinted, so rebuilding their outlines via a
    transform pen is lossless. Returns stats: {"normalized", "condensed"}.
    """
    cell = target if target is not None else cell_width(font)
    hmtx = font["hmtx"]
    glyf = font["glyf"]
    glyphset = font.getGlyphSet()
    normalized = 0
    condensed = 0

    for name in font.getGlyphOrder():
        adv, _ = hmtx[name]
        if adv == 0 or adv % cell == 0:
            continue  # marks and glyphs already on the cell grid: leave as-is

        # Snap to the nearest whole number of cells (1 for almost everything;
        # 2 preserves intentional double-width glyphs such as Roman numerals).
        cells = max(1, round(adv / cell))
        width = cells * cell
        max_ink = width - 2 * _CONDENSE_MARGIN

        bounds = _ink_bounds(glyf, name)
        if bounds is None:
            hmtx[name] = (width, 0)  # empty glyph (e.g. space): just set advance
            normalized += 1
            continue

        xmin, xmax = bounds
        ink = xmax - xmin
        # Center the ink in the cell; condense only glyphs whose own ink is
        # wider than the cell (minus margins) so nothing is trimmed.
        sx = 1.0
        if fit_overflow and ink > max_ink:
            sx = max_ink / ink
            condensed += 1
        new_ink = ink * sx
        target_xmin = (width - new_ink) / 2
        transform = (sx, 0.0, 0.0, 1.0, target_xmin - sx * xmin, 0.0)

        # Decompose composites so the transform reaches their outlines, then
        # rebuild as simple contours (donor letters are unhinted -> lossless).
        rec = DecomposingRecordingPen(glyphset)
        glyphset[name].draw(rec)
        pen = TTGlyphPen(None)
        rec.replay(TransformPen(pen, transform))
        new_glyph = pen.glyph()
        glyf[name] = new_glyph
        new_glyph.recalcBounds(glyf)
        hmtx[name] = (width, new_glyph.xMin)
        normalized += 1

    log.info(
        "normalize_monospace: cell=%d normalized=%d condensed=%d",
        cell,
        normalized,
        condensed,
    )
    return {"cell": cell, "normalized": normalized, "condensed": condensed}


def set_fixed_pitch_flags(font: TTFont) -> None:
    """Declare the font monospaced (only valid once advances are uniform)."""
    if "post" in font:
        font["post"].isFixedPitch = 1
    if "OS/2" in font:
        panose = font["OS/2"].panose
        # Latin Text family; proportion = 9 (Monospaced).
        if getattr(panose, "bFamilyType", 0) in (0, 2):
            panose.bFamilyType = 2
            panose.bProportion = 9
