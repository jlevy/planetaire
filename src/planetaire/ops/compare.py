"""
Glyph-level font comparison.

Compares glyph outlines between two fonts using RecordingPen to serialize
outlines into canonical drawing operations, then compares sequences.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from fontTools.pens.recordingPen import RecordingPen
from fontTools.ttLib import TTFont


@dataclass
class GlyphDiff:
    """Comparison result for a single codepoint."""

    codepoint: int
    glyph_name_a: str
    glyph_name_b: str
    status: Literal["identical", "different", "missing_a", "missing_b"]
    diff_details: str | None = None


@dataclass
class CompareResult:
    """Summary of a font comparison."""

    identical: int = 0
    different: int = 0
    missing_a: int = 0
    missing_b: int = 0
    diffs: list[GlyphDiff] = field(default_factory=list)


def compare_fonts(
    font_a: TTFont,
    font_b: TTFont,
    ranges: list[tuple[int, int]] | None = None,
    *,
    tolerance: float = 0.5,
    normalize_upm: bool = True,
) -> CompareResult:
    """
    Compare glyph outlines between two fonts.

    Uses RecordingPen to serialize glyph outlines, then compares the
    recorded operations. Handles UPM differences by scaling coordinates
    before comparison.
    """
    cmap_a = font_a.getBestCmap() or {}
    cmap_b = font_b.getBestCmap() or {}

    upm_a = font_a["head"].unitsPerEm
    upm_b = font_b["head"].unitsPerEm
    scale_a = 1.0
    scale_b = 1.0
    if normalize_upm and upm_a != upm_b:
        # Normalize both to UPM=1000 for comparison
        scale_a = 1000.0 / upm_a
        scale_b = 1000.0 / upm_b

    # Determine codepoints to compare
    if ranges:
        from planetaire.unicode_ranges import codepoints_in_ranges

        codepoints = sorted(codepoints_in_ranges(ranges))
    else:
        codepoints = sorted(set(cmap_a.keys()) | set(cmap_b.keys()))

    result = CompareResult()
    for cp in codepoints:
        in_a = cp in cmap_a
        in_b = cp in cmap_b
        glyph_name_a = cmap_a.get(cp, "")
        glyph_name_b = cmap_b.get(cp, "")

        if not in_a and not in_b:
            continue
        if not in_a:
            result.missing_a += 1
            result.diffs.append(GlyphDiff(cp, "", glyph_name_b, "missing_a"))
            continue
        if not in_b:
            result.missing_b += 1
            result.diffs.append(GlyphDiff(cp, glyph_name_a, "", "missing_b"))
            continue

        # Record outlines from both fonts
        ops_a = _record_glyph(font_a, glyph_name_a)
        ops_b = _record_glyph(font_b, glyph_name_b)

        if _ops_equal(ops_a, ops_b, scale_a, scale_b, tolerance):
            result.identical += 1
        else:
            result.different += 1
            detail = _describe_diff(ops_a, ops_b)
            result.diffs.append(GlyphDiff(cp, glyph_name_a, glyph_name_b, "different", detail))

    return result


def _record_glyph(font: TTFont, glyph_name: str) -> list[tuple[str, tuple[object, ...]]]:
    """Record glyph drawing operations using RecordingPen."""
    pen = RecordingPen()
    try:
        glyph_set = font.getGlyphSet()
        glyph_set[glyph_name].draw(pen)
    except (KeyError, TypeError):
        return []
    return pen.value


def _scale_point(point: object, scale: float) -> object:
    """Scale a point tuple by a factor."""
    if isinstance(point, tuple) and len(point) == 2:
        x, y = point
        if isinstance(x, (int, float)) and isinstance(y, (int, float)):
            return (x * scale, y * scale)
    return point


def _ops_equal(
    ops_a: list[tuple[str, tuple[object, ...]]],
    ops_b: list[tuple[str, tuple[object, ...]]],
    scale_a: float,
    scale_b: float,
    tolerance: float,
) -> bool:
    """Compare two recorded glyph operation sequences with scaling and tolerance."""
    if len(ops_a) != len(ops_b):
        return False

    for (op_a, args_a), (op_b, args_b) in zip(ops_a, ops_b, strict=True):
        if op_a != op_b:
            return False
        if len(args_a) != len(args_b):
            return False
        for a, b in zip(args_a, args_b, strict=True):
            sa = _scale_point(a, scale_a)
            sb = _scale_point(b, scale_b)
            if isinstance(sa, tuple) and isinstance(sb, tuple):
                for va, vb in zip(sa, sb, strict=True):
                    if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
                        if abs(va - vb) > tolerance:
                            return False
            elif sa != sb:
                return False
    return True


def _describe_diff(
    ops_a: list[tuple[str, tuple[object, ...]]],
    ops_b: list[tuple[str, tuple[object, ...]]],
) -> str:
    """Generate a brief description of how two glyph outlines differ."""
    if len(ops_a) != len(ops_b):
        return f"operation count differs: {len(ops_a)} vs {len(ops_b)}"
    for i, ((op_a, _), (op_b, _)) in enumerate(zip(ops_a, ops_b, strict=True)):
        if op_a != op_b:
            return f"operation {i} differs: {op_a} vs {op_b}"
    return "coordinate differences"
