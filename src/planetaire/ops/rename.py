"""Font family name and metadata updates."""

from __future__ import annotations

from fontTools.ttLib import TTFont


def rename_font(
    font: TTFont,
    *,
    family: str,
    subfamily: str | None = None,
    weight: int | None = None,
    version: str | None = None,
) -> TTFont:
    """
    Update font family name and related metadata.

    Updates name table IDs 1 (family), 2 (subfamily), 4 (full name),
    6 (PostScript name), 16 (typographic family), 17 (typographic subfamily).
    Sets OS/2.usWeightClass if `weight` is provided.
    """
    name_table = font["name"]
    sub = subfamily or _get_name(name_table, 2) or "Regular"
    ps_family = family.replace(" ", "")
    ps_name = f"{ps_family}-{sub.replace(' ', '')}"
    full = f"{family} {sub}" if sub != "Regular" else family

    _set_name(name_table, 1, family)
    _set_name(name_table, 2, sub)
    _set_name(name_table, 4, full)
    _set_name(name_table, 6, ps_name)
    _set_name(name_table, 16, family)
    _set_name(name_table, 17, sub)

    # Unique ID (name ID 3)
    ver = version or _get_name(name_table, 5) or "1.0"
    _set_name(name_table, 3, f"{ver};{ps_name}")

    if version:
        _set_name(name_table, 5, f"Version {version}")

    if weight is not None and "OS/2" in font:
        font["OS/2"].usWeightClass = weight

    return font


def _get_name(name_table: object, name_id: int) -> str:
    record = name_table.getName(name_id, 3, 1, 0x0409)  # pyright: ignore
    if record is None:
        record = name_table.getName(name_id, 1, 0, 0)  # pyright: ignore
    return str(record) if record else ""


def _set_name(name_table: object, name_id: int, value: str) -> None:
    name_table.setName(value, name_id, 3, 1, 0x0409)  # pyright: ignore
    name_table.setName(value, name_id, 1, 0, 0)  # pyright: ignore
