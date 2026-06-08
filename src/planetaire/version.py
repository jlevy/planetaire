"""Canonical version resolution for both the Python package and the fonts.

A single source of truth is threaded into font name tables, `head.fontRevision`,
and the specimen, so the package, the binaries, and the specimen never disagree.

The version comes from the latest git tag when building inside the repo, so a
dev/editable checkout always reflects the current release (e.g. tag ``v0.1.2`` ->
``"0.1.2"``, and a future ``v0.1.3`` tag updates everything with no other change).
Outside a git checkout (an installed package) it falls back to the baked package
metadata, which uv-dynamic-versioning sets from the same git tag at build time.
"""

from __future__ import annotations

import re
import subprocess
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version
from pathlib import Path

_FALLBACK_VERSION = "0.0.0"


def _git_tag_version() -> str | None:
    """Release version from the latest git tag (e.g. "0.1.2"), or None.

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
    match = re.match(r"v?(\d+(?:\.\d+){0,2})", result.stdout.strip())
    return match.group(1) if match else None


def get_version() -> str:
    """Return the canonical release version (e.g. "0.1.2").

    Prefers the latest git tag (so dev/editable builds reflect the current release
    even when the installed metadata is stale), then the installed package
    metadata, then "0.0.0".
    """
    git_version = _git_tag_version()
    if git_version:
        return git_version
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
