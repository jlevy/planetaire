"""Font metadata inspection using fontTools."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from fontTools.ttLib import TTFont


@dataclass
class FontInfo:
    """Structured font metadata."""

    family: str
    subfamily: str
    full_name: str
    version: str
    postscript_name: str
    glyph_count: int
    upm: int
    weight_class: int
    is_italic: bool
    os2_metrics: dict[str, int] = field(default_factory=dict)
    gsub_features: list[str] = field(default_factory=list)


def inspect_font(path: Path) -> FontInfo:
    """Read font metadata. Pure read, no modifications."""
    font = TTFont(path)
    name_table = font["name"]

    def _get_name(name_id: int) -> str:
        record = name_table.getName(name_id, 3, 1, 0x0409)
        if record is None:
            record = name_table.getName(name_id, 1, 0, 0)
        return str(record) if record else ""

    # GSUB features
    gsub_features: list[str] = []
    if "GSUB" in font:
        gsub = font["GSUB"]
        if gsub.table.FeatureList:
            seen: set[str] = set()
            for rec in gsub.table.FeatureList.FeatureRecord:
                tag = rec.FeatureTag
                if tag not in seen:
                    gsub_features.append(tag)
                    seen.add(tag)

    # OS/2 metrics
    os2_metrics: dict[str, int] = {}
    if "OS/2" in font:
        os2 = font["OS/2"]
        os2_metrics = {
            "ascender": os2.sTypoAscender,
            "descender": os2.sTypoDescender,
            "line_gap": os2.sTypoLineGap,
            "x_height": getattr(os2, "sxHeight", 0),
            "cap_height": getattr(os2, "sCapHeight", 0),
        }

    is_italic = False
    if "head" in font:
        is_italic = bool(font["head"].macStyle & 0x2)

    weight_class = font["OS/2"].usWeightClass if "OS/2" in font else 0

    return FontInfo(
        family=_get_name(1),
        subfamily=_get_name(2),
        full_name=_get_name(4),
        version=_get_name(5),
        postscript_name=_get_name(6),
        glyph_count=len(font.getGlyphOrder()),
        upm=font["head"].unitsPerEm,
        weight_class=weight_class,
        is_italic=is_italic,
        os2_metrics=os2_metrics,
        gsub_features=gsub_features,
    )
