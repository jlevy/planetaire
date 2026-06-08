"""Font family name and metadata updates."""

from __future__ import annotations

from fontTools.ttLib import TTFont

# Combined copyright notice for Planetaire Mono, crediting all upstream sources.
# Copyright holders and years sourced from:
#   - LICENSE (top-level): Planetaire/Joshua Levy 2026, B612 2012, Hack/Source Foundry 2018,
#     Bitstream 2003, Nerd Fonts/Ryan L McIntyre 2014
#   - fonts/source/licenses/B612-OFL.txt: "Copyright 2012 The B612 Project Authors"
#   - fonts/source/licenses/Hack-LICENSE.md: "Copyright (c) 2018 Source Foundry Authors" /
#     "Copyright (c) 2003 by Bitstream, Inc."
#   - fonts/source/licenses/NerdFonts-LICENSE: "Copyright (c) 2014 Ryan L McIntyre"
COPYRIGHT_NOTICE = (
    "Copyright 2026 Joshua Levy (https://github.com/jlevy/planetaire). "
    "Portions copyright 2012 The B612 Project Authors (https://github.com/polarsys/b612). "
    "Portions copyright 2018 Source Foundry Authors / 2003 Bitstream, Inc. "
    "(https://github.com/source-foundry/Hack). "
    "Portions copyright 2014 Ryan L McIntyre (https://github.com/ryanoasis/nerd-fonts)."
)

# License description for the combined font distribution (nameID 13).
# Planetaire Mono is distributed under OFL-1.1 as the umbrella license for the combined work.
# Constituent upstream licenses: B612 (OFL-1.1 + EPL-2.0), Hack (MIT + Bitstream Vera),
# Nerd Fonts patches (MIT + OFL-1.1 for glyph fonts).
LICENSE_DESCRIPTION = (
    "This Font Software is licensed under the SIL Open Font License, Version 1.1 "
    "(https://openfontlicense.org). "
    "Constituent upstream licenses: "
    "B612 Mono: SIL OFL-1.1 and Eclipse Public License 2.0; "
    "Hack: MIT License and Bitstream Vera License; "
    "Nerd Fonts patches: MIT License (tooling) and SIL OFL-1.1 (glyph fonts). "
    "Full license texts are included with this distribution."
)

# License URL (nameID 14).
LICENSE_URL = "https://openfontlicense.org"


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

    Updates name table IDs 0 (copyright), 1 (family), 2 (subfamily), 4 (full name),
    6 (PostScript name), 13 (license description), 14 (license URL),
    16 (typographic family), 17 (typographic subfamily).
    Sets OS/2.usWeightClass if `weight` is provided.
    """
    name_table = font["name"]
    sub = subfamily or _get_name(name_table, 2) or "Regular"
    ps_family = family.replace(" ", "")
    ps_name = f"{ps_family}-{sub.replace(' ', '')}"
    full = f"{family} {sub}" if sub != "Regular" else family

    # Copyright, license description, and license URL.
    license_names: dict[int, str] = {
        0: COPYRIGHT_NOTICE,
        13: LICENSE_DESCRIPTION,
        14: LICENSE_URL,
    }
    for name_id, value in license_names.items():
        _set_name(name_table, name_id, value)

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
        if "head" in font:
            from planetaire.version import to_font_revision

            font["head"].fontRevision = to_font_revision(version)

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
