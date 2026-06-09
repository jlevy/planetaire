#!/usr/bin/env python3
"""Prepare a release for review, then finalize it (commit + tag).

Versioning is tag-driven: the git tag `vX.Y.Z` is the single source of truth that
`uv-dynamic-versioning` and `planetaire.version.get_version()` thread into the font
binaries and the specimen. That creates a chicken-and-egg for any artifact that must
live *inside* the tagged commit while also naming the version: the committed specimen
PDF stamps a version, and the README pins its jsDelivr CDN links to a tag. Both have to
match the tag, but the tag does not exist yet.

This script resolves it by making the version an explicit input, and splits the release
into two steps so there is always a review gate before anything is committed:

  prepare X.Y.Z
    0. Require committed curated notes at docs/release/notes/vX.Y.Z.md.
    1. Build the fonts locally (so Typst can render the specimen with the real glyphs;
       the version baked into these throwaway local binaries does not matter).
    2. Rebuild the committed specimen PDF with `--version X.Y.Z` stamped explicitly.
    3. Re-pin every README jsDelivr CDN link to `planetaire@vX.Y.Z` (a plain
       search/replace from the previous ref — no template vars — which also busts the
       CDN cache, since `@vX.Y.Z` is a URL jsDelivr has never served).
    4. Leave those changes in the working tree and print the diff. STOP for review.

  finalize X.Y.Z
    5. Commit the PDF + README as `release: vX.Y.Z` and tag that commit `vX.Y.Z`.

After finalize the specimen PDF served by `cdn.jsdelivr.net/gh/jlevy/planetaire@vX.Y.Z/`
is byte-for-byte the PDF that stamps `Version X.Y.Z`, and the fonts CI builds from the
same tag also report X.Y.Z. Everything agrees by construction, not by timing.

Neither step pushes; finalize prints the push commands. See docs/fonts-build-and-release.md.

Usage:
    uv run python scripts/release.py prepare 0.1.4              # build + re-pin, then review
    uv run python scripts/release.py prepare 0.1.4 --no-build   # reuse fonts/output
    uv run python scripts/release.py finalize 0.1.4            # commit + tag the reviewed changes
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import NoReturn

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
SPECIMEN_PDF = REPO_ROOT / "docs/specimen/planetaire-mono-specimen.pdf"
# Paths the release commit is allowed to touch, relative to the repo root.
RELEASE_PATHS = ["README.md", "docs/specimen/planetaire-mono-specimen.pdf"]

# Matches the ref segment of any jsDelivr CDN link into this repo, e.g. `planetaire@main`
# or `planetaire@v0.1.3`. The second group is whatever ref the link is currently pinned to
# (the previous release, or `main`); we rewrite just that. This is a plain search/replace
# that matches the last release and swaps in the new tag — no template variables — and
# because `@vX.Y.Z` is a URL jsDelivr has never cached, re-pinning busts the CDN cache.
CDN_LINK_RE = re.compile(r"(cdn\.jsdelivr\.net/gh/jlevy/planetaire@)([^/\s)\"']+)")

VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")


def run(cmd: list[str], *, capture: bool = False, check: bool = True) -> subprocess.CompletedProcess:
    """Run a command at the repo root, echoing it."""
    print(f"  $ {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=REPO_ROOT, text=True, capture_output=capture, check=check)


def out(cmd: list[str]) -> str:
    """Run a command and return its stripped stdout."""
    return run(cmd, capture=True).stdout.strip()


def fail(msg: str) -> NoReturn:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def normalize(raw: str) -> tuple[str, str]:
    """Return (version, tag) from a `0.1.4` or `v0.1.4` argument."""
    version = raw.lstrip("v")
    if not VERSION_RE.match(version):
        fail(f"version must look like X.Y.Z (got {raw!r})")
    return version, f"v{version}"


def require_main_and_tagfree(tag: str) -> None:
    """Hard guards shared by both steps: on main, and the tag does not exist yet."""
    branch = out(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    if branch != "main":
        fail(
            f"releases are cut from main; you are on {branch!r}. Merge to main and check it "
            "out first (see docs/fonts-build-and-release.md)."
        )
    if out(["git", "tag", "--list", tag]):
        fail(f"tag {tag} already exists; pick the next version or delete the tag")


def require_release_notes(tag: str) -> Path:
    """Require curated, committed release notes for the GitHub downloads page."""
    notes = REPO_ROOT / f"docs/release/notes/{tag}.md"
    rel = str(notes.relative_to(REPO_ROOT))
    if not notes.exists():
        fail(
            f"missing release notes at {rel}. Copy docs/release/notes/TEMPLATE.md, fill "
            "in the release-specific changes and compare link, then commit the notes "
            "before preparing the release."
        )
    if out(["git", "status", "--porcelain", "--", rel]):
        fail(
            f"{rel} has uncommitted changes. Commit the curated release notes before "
            "preparing the release so the tag contains exactly what GitHub publishes."
        )
    return notes


def rewrite_cdn_links(tag: str) -> int:
    """Re-pin every jsDelivr CDN link in the README to `planetaire@<tag>`. Returns count."""
    text = README.read_text()
    matches = CDN_LINK_RE.findall(text)
    if not matches:
        fail(
            "could not find any jsDelivr CDN link "
            "(cdn.jsdelivr.net/gh/jlevy/planetaire@...) in README.md"
        )
    refs = sorted({ref for _, ref in matches})
    if refs == [tag]:
        print(f"  README CDN links already pinned to {tag}")
        return len(matches)
    froms = ", ".join(f"@{ref}" for ref in refs)
    print(f"  re-pinning {len(matches)} README CDN link(s): {froms} -> @{tag}")
    README.write_text(CDN_LINK_RE.sub(rf"\g<1>{tag}", text))
    return len(matches)


def cmd_prepare(args: argparse.Namespace) -> None:
    version, tag = normalize(args.version)
    print(f"Preparing release {tag} for review.\n")

    print("Preflight:")
    require_main_and_tagfree(tag)
    require_release_notes(tag)
    if out(["git", "status", "--porcelain", "--", *RELEASE_PATHS]):
        fail(
            "the release files have uncommitted changes already. Commit or discard them so "
            "the review diff shows only what this release introduces."
        )

    print("\nBuild assets:")
    if args.no_build:
        if not (REPO_ROOT / "fonts/output").exists():
            fail("--no-build given but fonts/output does not exist; run a build first")
    else:
        run(["uv", "run", "planetaire", "build", "download"])
        run(["uv", "run", "planetaire", "build", "planetaire-mono"])
        run(["uv", "run", "planetaire", "build", "text"])
    run(["uv", "run", "planetaire", "build", "specimen", "--version", version])

    print("\nRe-pin README:")
    rewrite_cdn_links(tag)

    if not out(["git", "status", "--porcelain", "--", *RELEASE_PATHS]):
        fail("nothing changed — the PDF and README already match this version")

    print(f"\nPrepared {tag}. Review the changes below, then finalize.\n")
    run(["git", "--no-pager", "diff", "--stat", "--", *RELEASE_PATHS])
    print()
    run(["git", "--no-pager", "diff", "--", "README.md"])
    print(
        f"\nWhen the diff looks right:\n"
        f"  make release-finalize VERSION={version}\n"
        f"To discard and start over:\n"
        f"  git checkout -- {' '.join(RELEASE_PATHS)}"
    )


def cmd_finalize(args: argparse.Namespace) -> None:
    version, tag = normalize(args.version)
    print(f"Finalizing release {tag}.\n")

    print("Preflight:")
    require_main_and_tagfree(tag)
    require_release_notes(tag)
    if not out(["git", "status", "--porcelain", "--", *RELEASE_PATHS]):
        fail(f"no prepared release changes found — run `make release VERSION={version}` first")
    # Guard against a stray version: the PDF must stamp this tag and the README must point
    # at it, so a finalize for the wrong version cannot slip through.
    if f"planetaire@{tag}/" not in README.read_text():
        fail(
            f"README is not pinned to {tag}. Re-run `make release VERSION={version}` so the "
            "prepared changes match the version you are finalizing."
        )

    print("\nCommit and tag:")
    run(["git", "commit", "-m", f"release: {tag}", "--", *RELEASE_PATHS])
    run(["git", "tag", "-a", tag, "-m", tag])

    print("\nDone. Push to publish (this script does not push):")
    print("  git push origin main")
    print(f"  git push origin {tag}        # fires release-fonts.yml")
    print("  # In a Claude Code web session the git proxy rejects tag pushes; instead:")
    print(f"  # gh api repos/jlevy/planetaire/git/refs -f ref=refs/tags/{tag} \\")
    print(f"  #   -f sha=\"$(git rev-parse {tag}^{{commit}})\"")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="step", required=True)

    p = sub.add_parser("prepare", help="Build + re-pin the README, then stop for review")
    p.add_argument("version", help="Release version, e.g. 0.1.4 (no leading v)")
    p.add_argument("--no-build", action="store_true", help="Reuse fonts/output instead of rebuilding")
    p.set_defaults(func=cmd_prepare)

    f = sub.add_parser("finalize", help="Commit + tag the prepared (reviewed) changes")
    f.add_argument("version", help="Release version, e.g. 0.1.4 (no leading v)")
    f.set_defaults(func=cmd_finalize)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
