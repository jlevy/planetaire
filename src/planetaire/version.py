"""Canonical version resolution for both the Python package and the fonts.

A single source of truth is threaded into font name tables, `head.fontRevision`,
and the specimen, so the package, the binaries, and the specimen never disagree.

The version comes from the latest git tag when building inside the repo, so a
dev/editable checkout always reflects the current release (e.g. tag ``v0.1.2`` ->
``"0.1.2"``, and a future ``v0.1.3`` tag updates everything with no other change).
Outside a git checkout (an installed package) it falls back to the baked package
metadata, which uv-dynamic-versioning sets from the same git tag at build time.

Resolution reports *where* the version came from, not only what it is. A release
build runs before its own tag exists, so it must stamp the version explicitly
instead of resolving one (see `scripts/release.py`), and the gate that compares the
committed web fonts against a rebuild is only well defined when the rebuild's
version came from the tag rather than from a fallback (plt-0204).
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from enum import StrEnum
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version
from pathlib import Path

_FALLBACK_VERSION = "0.0.0"


class VersionSource(StrEnum):
    """Where a resolved version came from, in precedence order."""

    git_tag = "git-tag"
    package_metadata = "package-metadata"
    fallback = "fallback"


@dataclass(frozen=True)
class ResolvedVersion:
    """A canonical version and the origin it was resolved from."""

    version: str
    source: VersionSource
    origin: str
    """Human-readable origin, e.g. ``git tag v0.1.2``. For error messages and logs."""


def _latest_git_tag() -> str | None:
    """The latest git tag reachable from HEAD, or None.

    Returns None outside a git checkout (installed package) or when git is
    unavailable, so callers fall back to the baked package metadata.
    """
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True,
            text=True,
            check=False,
            cwd=Path(__file__).resolve().parent,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def _version_from_tag(tag: str) -> str | None:
    """Release version from a tag name (``v0.1.2`` -> ``"0.1.2"``), or None."""
    match = re.match(r"v?(\d+(?:\.\d+){0,2})", tag)
    return match.group(1) if match else None


def resolve_version() -> ResolvedVersion:
    """Resolve the canonical release version and report where it came from.

    Prefers the latest git tag (so dev/editable builds reflect the current release
    even when the installed metadata is stale), then the installed package
    metadata, then "0.0.0".
    """
    tag = _latest_git_tag()
    if tag is not None:
        tagged = _version_from_tag(tag)
        if tagged:
            return ResolvedVersion(tagged, VersionSource.git_tag, f"git tag {tag}")
    try:
        return ResolvedVersion(
            _pkg_version("planetaire"),
            VersionSource.package_metadata,
            "installed package metadata",
        )
    except PackageNotFoundError:
        return ResolvedVersion(
            _FALLBACK_VERSION,
            VersionSource.fallback,
            "fallback (no version tag reachable, no installed package metadata)",
        )


def get_version() -> str:
    """Return the canonical release version (e.g. "0.1.2")."""
    return resolve_version().version


def to_font_version(pkg_version: str) -> str:
    """Reduce a PEP 440 version to a clean numeric font version string.

    Font name ID 5 wants a stable, human-readable release number, not a dev/local
    suffix. We keep up to major.minor.patch from the leading release segment.

    >>> to_font_version("1.2.3")
    '1.2.3'
    >>> to_font_version("0.1.dev4+g1a2b3c")
    '0.1.0'
    >>> to_font_version("garbage")
    '0.0.0'
    """
    match = re.match(r"\d+(?:\.\d+)*", pkg_version)
    parts = match.group(0).split(".") if match else []
    while len(parts) < 3:
        parts.append("0")
    return ".".join(parts[:3])


def to_font_revision(pkg_version: str) -> float:
    """Convert a version to the OpenType `head.fontRevision` value (major.minor).

    fontRevision is a 16.16 fixed-point number conventionally set to major.minor.

    >>> to_font_revision("1.2.3")
    1.2
    >>> to_font_revision("0.1.dev4")
    0.1
    >>> to_font_revision("garbage")
    0.0
    """
    match = re.match(r"(\d+)(?:\.(\d+))?", pkg_version)
    if not match:
        return 0.0
    major = int(match.group(1))
    minor = int(match.group(2) or 0)
    return float(f"{major}.{minor}")
