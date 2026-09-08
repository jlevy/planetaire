#!/usr/bin/env python3
"""Gate the committed public web fonts against a rebuild from this commit's sources.

`fonts/web/` is what jsDelivr serves and `site/fonts/` is the Pages-local copy; both
are committed binaries, so nothing but this check keeps them honest about the sources
beside them. The build is byte-reproducible (`head.modified` is pinned in
`ops/subset.py`), so "matches a rebuild" is a byte comparison, not a tolerance.

The version is the one moving part. Every face stamps it into name ID 5 and
`head.fontRevision`, so the comparison is only well defined once both sides agree on
which version this commit builds: the latest release tag reachable from HEAD. That is
resolved here, explicitly, and a version that did not come from a tag is an error
rather than a confusing byte diff (plt-0204).

Usage:
    uv run python devtools/check_web_fonts.py                 # CI and release gate
    uv run python devtools/check_web_fonts.py --version 0.2.0 # stamp an explicit version
    uv run python devtools/check_web_fonts.py --write         # rebuild and refresh both dirs
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
import tempfile
from pathlib import Path
from typing import NoReturn

from planetaire.config import text_web_font_file_names
from planetaire.recipes.planetaire_mono import build_text
from planetaire.version import VersionSource, resolve_version

REPO_ROOT = Path(__file__).resolve().parent.parent
FONTS_SOURCE = REPO_ROOT / "fonts/source"
# Both committed copies of the same files: what jsDelivr serves, and the copy the
# static site loads locally. `scripts/release.py` syncs them together, so they are
# gated together.
WEB_FONT_DIRS = [REPO_ROOT / "fonts/web", REPO_ROOT / "site/fonts"]

REMEDIATION = """\
Refresh both committed copies from a rebuild, then commit them:
  uv run python devtools/check_web_fonts.py --write
  git add fonts/web site/fonts

At release time `make release VERSION=X.Y.Z` does this as part of preparing the
release, stamping the version being released."""


def fail(msg: str) -> NoReturn:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def resolve_build_version(explicit: str | None, *, allow_untagged: bool) -> str:
    """Resolve the version the rebuild must stamp, and say where it came from."""
    if explicit:
        print(f"Rebuilding at version {explicit} (given explicitly)", flush=True)
        return explicit

    resolved = resolve_version()
    if resolved.source is not VersionSource.git_tag and not allow_untagged:
        fail(
            f"resolved version {resolved.version} came from {resolved.origin}, not a git "
            "tag, so a rebuild would not stamp the version the committed web fonts "
            "carry. Fetch tags (actions/checkout needs fetch-depth: 0), or pass "
            "--version, or --allow-untagged if you really mean to compare against an "
            "untagged build."
        )
    print(f"Rebuilding at version {resolved.version} (from {resolved.origin})", flush=True)
    return resolved.version


def strays(target_dir: Path, expected: tuple[str, ...]) -> list[Path]:
    """Files in a committed web-font directory that are not part of the published set."""
    return sorted(
        path
        for path in target_dir.iterdir()
        if path.name not in expected and not path.name.startswith(".")
    )


def compare_dir(target_dir: Path, built_dir: Path, expected: tuple[str, ...]) -> list[str]:
    """Compare one committed web-font directory against the rebuild, byte for byte."""
    rel = target_dir.relative_to(REPO_ROOT)
    problems: list[str] = []

    if not target_dir.is_dir():
        return [f"{rel}/ does not exist"]

    for name in expected:
        committed = target_dir / name
        rebuilt = built_dir / name
        if not rebuilt.exists():
            problems.append(f"{rel}/{name}: the rebuild did not produce this file")
        elif not committed.exists():
            problems.append(f"{rel}/{name}: missing from the committed directory")
        elif not filecmp.cmp(committed, rebuilt, shallow=False):
            problems.append(
                f"{rel}/{name}: differs from the rebuild "
                f"({committed.stat().st_size} vs {rebuilt.stat().st_size} bytes)"
            )

    for stray in strays(target_dir, expected):
        problems.append(f"{rel}/{stray.name}: not part of the published web-font set")

    if not problems:
        print(f"  {rel}/: {len(expected)} file(s) match the rebuild")
    return problems


def write_dir(target_dir: Path, built_dir: Path, expected: tuple[str, ...]) -> None:
    """Refresh one committed web-font directory from the rebuild."""
    rel = target_dir.relative_to(REPO_ROOT)
    target_dir.mkdir(parents=True, exist_ok=True)
    for stray in strays(target_dir, expected):
        print(f"  {rel}/{stray.name}: removing (not part of the published web-font set)")
        stray.unlink()
    for name in expected:
        rebuilt = built_dir / name
        if not rebuilt.exists():
            fail(f"the rebuild did not produce {name}")
        shutil.copy2(rebuilt, target_dir / name)
    print(f"  {rel}/: refreshed {len(expected)} file(s)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--version",
        help="Version to stamp into the rebuild (default: the canonical git-tag version)",
    )
    parser.add_argument(
        "--allow-untagged",
        action="store_true",
        help="Compare even when no release tag is reachable (the rebuild stamps a fallback)",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Refresh both committed directories from the rebuild instead of checking them",
    )
    args = parser.parse_args(argv)

    version = resolve_build_version(args.version, allow_untagged=args.allow_untagged)
    expected = text_web_font_file_names()

    with tempfile.TemporaryDirectory() as tmpdir:
        build_text(FONTS_SOURCE, Path(tmpdir), version=version)
        if args.write:
            for target_dir in WEB_FONT_DIRS:
                write_dir(target_dir, Path(tmpdir), expected)
            print("Refreshed the committed web fonts. Review and commit them.")
            return 0
        problems = [
            problem
            for target_dir in WEB_FONT_DIRS
            for problem in compare_dir(target_dir, Path(tmpdir), expected)
        ]

    if problems:
        print()
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        print(f"\n{REMEDIATION}", file=sys.stderr)
        return 1

    print("The committed web fonts match a rebuild from this commit's sources.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
