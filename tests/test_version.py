"""Tests for version resolution and font-version conversion."""

from __future__ import annotations

import pytest

from planetaire.version import (
    VersionSource,
    get_version,
    resolve_version,
    to_font_revision,
    to_font_version,
)


def test_get_version_returns_nonempty():
    assert get_version()


def test_resolve_version_reports_its_origin():
    """Callers gate on where a version came from, not only on what it is.

    CI's web-font rebuild has to stamp the release version; a silent fall back to
    package metadata or "0.0.0" would turn a missing tag into an unexplained byte
    diff, so the source is part of the result (plt-0204).
    """
    resolved = resolve_version()
    assert resolved.version == get_version()
    assert resolved.source in set(VersionSource)
    assert resolved.origin
    if resolved.source is VersionSource.git_tag:
        assert resolved.origin.startswith("git tag ")
        assert resolved.version in resolved.origin


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
