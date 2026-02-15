"""Tests for ops/rename — font family name and metadata updates."""

from __future__ import annotations

from fontTools.ttLib import TTFont

from planetaire.ops.rename import rename_font


def test_rename_updates_family(base_font: TTFont):
    result = rename_font(base_font, family="Planetaire Mono")

    name_table = result["name"]
    family = str(name_table.getName(1, 3, 1, 0x0409))
    assert family == "Planetaire Mono"


def test_rename_updates_postscript_name(base_font: TTFont):
    result = rename_font(base_font, family="Planetaire Mono", subfamily="Bold")

    ps_name = str(result["name"].getName(6, 3, 1, 0x0409))
    assert ps_name == "PlanetaireMono-Bold"


def test_rename_updates_full_name(base_font: TTFont):
    result = rename_font(base_font, family="Planetaire Mono", subfamily="Bold")

    full = str(result["name"].getName(4, 3, 1, 0x0409))
    assert full == "Planetaire Mono Bold"


def test_rename_sets_weight(base_font: TTFont):
    result = rename_font(base_font, family="Test", weight=700)
    assert result["OS/2"].usWeightClass == 700


def test_rename_preserves_subfamily_if_not_specified(base_font: TTFont):
    result = rename_font(base_font, family="NewFamily")

    sub = str(result["name"].getName(2, 3, 1, 0x0409))
    assert sub == "Regular"
