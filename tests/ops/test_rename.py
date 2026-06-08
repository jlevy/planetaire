"""Tests for ops/rename — font family name and metadata updates."""

from __future__ import annotations

from pathlib import Path

import pytest
from fontTools.ttLib import TTFont

from planetaire.ops.rename import (
    COPYRIGHT_NOTICE,
    LICENSE_DESCRIPTION,
    LICENSE_URL,
    rename_font,
)

FONTS_SOURCE = Path(__file__).parent.parent.parent / "fonts" / "source"


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


def test_rename_sets_version_name_and_revision(base_font: TTFont):
    result = rename_font(base_font, family="Planetaire Mono", version="1.2.3")

    version_name = str(result["name"].getName(5, 3, 1, 0x0409))
    assert version_name == "Version 1.2.3"
    assert result["head"].fontRevision == 1.2


def test_rename_without_version_leaves_revision_untouched(base_font: TTFont):
    original_revision = base_font["head"].fontRevision
    result = rename_font(base_font, family="Planetaire Mono")
    assert result["head"].fontRevision == original_revision


# --- nameID 0/13/14 (copyright and license) tests ---


def test_rename_sets_copyright_on_minimal_font(base_font: TTFont):
    result = rename_font(base_font, family="Planetaire Mono")
    name_table = result["name"]
    copyright_val = str(name_table.getName(0, 3, 1, 0x0409))
    assert "Joshua Levy" in copyright_val
    assert "B612 Project Authors" in copyright_val
    assert "Source Foundry" in copyright_val
    assert "Ryan L McIntyre" in copyright_val


def test_rename_sets_license_description_on_minimal_font(base_font: TTFont):
    result = rename_font(base_font, family="Planetaire Mono")
    name_table = result["name"]
    license_val = str(name_table.getName(13, 3, 1, 0x0409))
    assert "OFL" in license_val
    assert "openfontlicense.org" in license_val
    assert "B612" in license_val
    assert "Hack" in license_val
    assert "Nerd Fonts" in license_val


def test_rename_sets_license_url_on_minimal_font(base_font: TTFont):
    result = rename_font(base_font, family="Planetaire Mono")
    name_table = result["name"]
    url_val = str(name_table.getName(14, 3, 1, 0x0409))
    assert "openfontlicense.org" in url_val


@pytest.fixture
def hack_regular_font() -> TTFont:
    path = FONTS_SOURCE / "hack" / "HackNerdFont-Regular.ttf"
    if not path.exists():
        pytest.skip("HackNerdFont-Regular.ttf not available")
    return TTFont(path)


def test_rename_sets_copyright_on_real_hack_font(hack_regular_font: TTFont):
    result = rename_font(hack_regular_font, family="Planetaire Mono")
    name_table = result["name"]
    copyright_val = str(name_table.getName(0, 3, 1, 0x0409))
    assert "Joshua Levy" in copyright_val
    assert "B612 Project Authors" in copyright_val
    assert "Source Foundry" in copyright_val
    assert "Ryan L McIntyre" in copyright_val


def test_rename_sets_license_description_on_real_hack_font(hack_regular_font: TTFont):
    result = rename_font(hack_regular_font, family="Planetaire Mono")
    name_table = result["name"]
    license_val = str(name_table.getName(13, 3, 1, 0x0409))
    assert "OFL" in license_val
    assert "openfontlicense.org" in license_val


def test_rename_sets_license_url_on_real_hack_font(hack_regular_font: TTFont):
    result = rename_font(hack_regular_font, family="Planetaire Mono")
    name_table = result["name"]
    url_val = str(name_table.getName(14, 3, 1, 0x0409))
    assert "openfontlicense.org" in url_val


def test_copyright_notice_constant_content():
    """Verify the constants themselves contain the required attribution strings."""
    assert "Joshua Levy" in COPYRIGHT_NOTICE
    assert "2026" in COPYRIGHT_NOTICE
    assert "B612 Project Authors" in COPYRIGHT_NOTICE
    assert "2012" in COPYRIGHT_NOTICE
    assert "Source Foundry Authors" in COPYRIGHT_NOTICE
    assert "2018" in COPYRIGHT_NOTICE
    assert "Bitstream" in COPYRIGHT_NOTICE
    assert "2003" in COPYRIGHT_NOTICE
    assert "Ryan L McIntyre" in COPYRIGHT_NOTICE
    assert "2014" in COPYRIGHT_NOTICE


def test_license_description_constant_content():
    assert "OFL" in LICENSE_DESCRIPTION
    assert "openfontlicense.org" in LICENSE_DESCRIPTION
    assert "B612" in LICENSE_DESCRIPTION
    assert "Hack" in LICENSE_DESCRIPTION
    assert "Nerd Fonts" in LICENSE_DESCRIPTION
    assert "MIT" in LICENSE_DESCRIPTION


def test_license_url_constant_content():
    assert "openfontlicense.org" in LICENSE_URL
