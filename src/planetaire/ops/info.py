"""Font metadata inspection using fontTools."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from fontTools.ttLib import TTFont

# GSUB lookup type names (OpenType spec).
_GSUB_LOOKUP_TYPES: dict[int, str] = {
    1: "Single",
    2: "Multiple",
    3: "Alternate",
    4: "Ligature",
    5: "Context",
    6: "ChainingContext",
    7: "Extension",
    8: "ReverseChaining",
}


@dataclass
class FeatureDetail:
    """Detailed info about a single GSUB feature."""

    tag: str
    lookup_indices: list[int]
    lookups: list[LookupDetail] = field(default_factory=list)


@dataclass
class LookupDetail:
    """Info about a single GSUB lookup."""

    index: int
    lookup_type: int
    lookup_type_name: str
    subtable_count: int
    substitutions: dict[str, str] = field(default_factory=dict)


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
    gsub_feature_details: list[FeatureDetail] = field(default_factory=list)


def _inspect_gsub_lookup(gsub_table: object, index: int) -> LookupDetail | None:
    """Inspect a single GSUB lookup by index, returning detail or None if out of range."""
    lookup_list = gsub_table.LookupList  # type: ignore[union-attr]
    if index >= len(lookup_list.Lookup):
        return None

    lookup = lookup_list.Lookup[index]
    lt = lookup.LookupType
    type_name = _GSUB_LOOKUP_TYPES.get(lt, f"Unknown({lt})")

    # Resolve Extension lookups to their actual type.
    actual_type = lt
    if lt == 7 and lookup.SubTable:
        ext = lookup.SubTable[0]
        actual_type = ext.ExtSubTable.LookupType if hasattr(ext, "ExtSubTable") else lt
        type_name = f"Extension → {_GSUB_LOOKUP_TYPES.get(actual_type, f'Unknown({actual_type})')}"

    # Extract substitution mappings for simple types.
    subs: dict[str, str] = {}
    for subtable in lookup.SubTable:
        st = subtable
        if lt == 7 and hasattr(st, "ExtSubTable"):
            st = st.ExtSubTable
        if hasattr(st, "mapping"):
            subs.update(st.mapping)

    return LookupDetail(
        index=index,
        lookup_type=lt,
        lookup_type_name=type_name,
        subtable_count=len(lookup.SubTable),
        substitutions=subs,
    )


def inspect_font(path: Path, *, feature_details: bool = False) -> FontInfo:
    """Read font metadata. Pure read, no modifications.

    Args:
        path: Path to font file.
        feature_details: If True, include detailed GSUB feature/lookup inspection.
    """
    font = TTFont(path)
    name_table = font["name"]

    def _get_name(name_id: int) -> str:
        record = name_table.getName(name_id, 3, 1, 0x0409)
        if record is None:
            record = name_table.getName(name_id, 1, 0, 0)
        return str(record) if record else ""

    # GSUB features
    gsub_features: list[str] = []
    gsub_feature_details: list[FeatureDetail] = []
    if "GSUB" in font:
        gsub = font["GSUB"]
        if gsub.table.FeatureList:
            seen: set[str] = set()
            for rec in gsub.table.FeatureList.FeatureRecord:
                tag = rec.FeatureTag
                if tag not in seen:
                    gsub_features.append(tag)
                    seen.add(tag)

                if feature_details:
                    indices = list(rec.Feature.LookupListIndex)
                    lookups: list[LookupDetail] = []
                    for idx in indices:
                        detail = _inspect_gsub_lookup(gsub.table, idx)
                        if detail is not None:
                            lookups.append(detail)
                        else:
                            lookups.append(
                                LookupDetail(
                                    index=idx,
                                    lookup_type=-1,
                                    lookup_type_name=f"DANGLING (index {idx} out of range)",
                                    subtable_count=0,
                                )
                            )
                    gsub_feature_details.append(
                        FeatureDetail(tag=tag, lookup_indices=indices, lookups=lookups)
                    )

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
        gsub_feature_details=gsub_feature_details,
    )
