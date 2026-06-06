"""Tests for version resolution and font-version conversion."""

from __future__ import annotations

import pytest

from planetaire.version import get_version, to_font_revision, to_font_version


def test_get_version_returns_nonempty():
    assert get_version()


@pytest.mark.parametrize(
    ("pkg_version", "expected"),
    [
        ("1.2.3", "1.2.3"),
        ("0.1.dev4+g1a2b3c", "0.1.0"),
        ("2", "2.0.0"),
        ("1.4", "1.4.0"),
        ("garbage", "0.0.0"),
    ],
)
def test_to_font_version(pkg_version: str, expected: str):
    assert to_font_version(pkg_version) == expected


@pytest.mark.parametrize(
    ("pkg_version", "expected"),
    [
        ("1.2.3", 1.2),
        ("0.1.dev4", 0.1),
        ("2", 2.0),
        ("garbage", 0.0),
    ],
)
def test_to_font_revision(pkg_version: str, expected: float):
    assert to_font_revision(pkg_version) == expected
