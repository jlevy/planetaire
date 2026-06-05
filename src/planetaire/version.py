"""Canonical version resolution for both the Python package and the fonts.

A single source of truth (the installed package version, derived from the git tag
via uv-dynamic-versioning) is threaded into font name tables, `head.fontRevision`,
and the specimen, so the package, the binaries, and the specimen never disagree.
"""

from __future__ import annotations

import re
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version

_FALLBACK_VERSION = "0.0.0"


def get_version() -> str:
    """Return the canonical package version (e.g. "1.2.3" or "0.1.dev4+g1a2b3c").

    Falls back to "0.0.0" when the package metadata is unavailable (e.g. running
    from a source tree that has not been installed).
    """
    try:
        return _pkg_version("planetaire")
    except PackageNotFoundError:
        return _FALLBACK_VERSION


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
