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
    1. Build the fonts locally with `--version X.Y.Z` stamped explicitly, because the
       web fonts built here are committed: without it they would carry whatever the
       latest existing tag says, which is the *previous* release (plt-0204).
    2. Refresh the committed public web fonts in fonts/web/ and the static-site copy in
       site/fonts/, check they stamp X.Y.Z, then validate the public copy, so the
       release gates exactly the bytes it is about to commit.
    3. Rebuild the committed specimen PDF with `--version X.Y.Z` stamped explicitly.
    4. Re-pin every release-controlled jsDelivr CDN link in README.md and site/ to
       `planetaire@vX.Y.Z` (a plain search/replace from the previous ref — no template
       vars — which also busts the CDN cache, since `@vX.Y.Z` is a URL jsDelivr has
       never served).
    5. Leave those changes in the working tree and print the diff. STOP for review.

  finalize X.Y.Z
    6. Commit the web fonts + PDF + release-controlled CDN pins as `release: vX.Y.Z` and
       tag that commit `vX.Y.Z`.
    7. With the tag now in place, rebuild the web fonts the way CI will and compare them
       byte for byte against what step 6 just committed. This is the same check as the
       `fonts` job's, run before the release is pushable rather than after.

After finalize the specimen PDF and public web fonts served by
`cdn.jsdelivr.net/gh/jlevy/planetaire@vX.Y.Z/` are byte-for-byte the committed files in
the tag, and the fonts CI builds from the same tag also reports X.Y.Z. Everything agrees
by construction, not by timing.

Neither step pushes; finalize prints the push commands. See docs/fonts-build-and-release.md.

Usage:
    uv run python scripts/release.py prepare 0.1.4              # build + refresh + re-pin
    uv run python scripts/release.py prepare 0.1.4 --no-build   # reuse fonts/output
    uv run python scripts/release.py finalize 0.1.4            # commit + tag the reviewed changes
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import NoReturn

from fontTools.ttLib import TTFont

from planetaire.config import text_web_font_file_names
from planetaire.version import to_font_revision

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
SPECIMEN_PDF = REPO_ROOT / "docs/specimen/planetaire-mono-specimen.pdf"
FONT_OUTPUT = REPO_ROOT / "fonts/output"
PUBLIC_WEB_FONTS = REPO_ROOT / "fonts/web"
SITE_FONTS = REPO_ROOT / "site/fonts"
# Files with production jsDelivr refs that must move together at release time. Keep
# examples/placeholders out of these files or avoid writing them as full jsDelivr URLs.
CDN_PINNED_PATHS = [
    "README.md",
    "site/index.html",
    "site/compare.html",
    "site/compare-fonts.js",
]
# Paths the release commit is allowed to touch, relative to the repo root.
RELEASE_PATHS = [
    "README.md",
    "docs/specimen/planetaire-mono-specimen.pdf",
    "site/index.html",
    "site/compare.html",
    "site/compare-fonts.js",
    "fonts/web",
    "site/fonts",
]

# Matches the ref segment of any jsDelivr CDN link into this repo, e.g. `planetaire@main`
# or `planetaire@v0.1.3`. The second group is whatever ref the link is currently pinned to
# (the previous release, or `main`); we rewrite just that. This is a plain search/replace
# that matches the last release and swaps in the new tag — no template variables — and
# because `@vX.Y.Z` is a URL jsDelivr has never cached, re-pinning busts the CDN cache.
CDN_LINK_RE = re.compile(r"(cdn\.jsdelivr\.net/gh/jlevy/planetaire@)([^/\s)\"']+)")

VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")


def run(
    cmd: list[str], *, capture: bool = False, check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Run a command at the repo root, echoing it."""
    print(f"  $ {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=REPO_ROOT, text=True, capture_output=capture, check=check)


def uv_run(
    cmd: list[str], *, capture: bool = False, check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Run a project command through uv without touching the lockfile.

    `--frozen` is not a performance tweak: a plain `uv run` re-resolves and can rewrite
    uv.lock mid-release, which leaves the release with an unrelated dirty file in a
    working tree the script is checking for cleanliness.
    """
    return run(["uv", "run", "--frozen", *cmd], capture=capture, check=check)


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


def cdn_refs_by_path() -> dict[str, list[str]]:
    """Return current jsDelivr refs in release-controlled files."""
    refs: dict[str, list[str]] = {}
    for rel in CDN_PINNED_PATHS:
        path = REPO_ROOT / rel
        matches = CDN_LINK_RE.findall(path.read_text())
        if matches:
            refs[rel] = sorted({ref for _, ref in matches})
    return refs


def rewrite_cdn_links(tag: str) -> int:
    """Re-pin release-controlled jsDelivr CDN links to `planetaire@<tag>`. Returns count."""
    total = 0
    before = cdn_refs_by_path()
    if not before:
        fail(
            "could not find any jsDelivr CDN link "
            f"(cdn.jsdelivr.net/gh/jlevy/planetaire@...) in {', '.join(CDN_PINNED_PATHS)}"
        )

    for rel in CDN_PINNED_PATHS:
        path = REPO_ROOT / rel
        text = path.read_text()
        matches = CDN_LINK_RE.findall(text)
        if not matches:
            continue
        total += len(matches)
        refs = sorted({ref for _, ref in matches})
        if refs == [tag]:
            print(f"  {rel}: {len(matches)} CDN link(s) already pinned to {tag}")
            continue
        previous = ", ".join(f"@{ref}" for ref in refs)
        print(f"  {rel}: re-pinning {len(matches)} CDN link(s): {previous} -> @{tag}")
        path.write_text(CDN_LINK_RE.sub(rf"\g<1>{tag}", text))
    return total


def sync_web_font_dir(target_dir: Path) -> int:
    """Copy the built Text web fonts into target_dir and remove everything else.

    The file set is enumerated (`text_web_font_file_names`), not globbed. fonts/output
    is a working directory that also collects the `--split` subset slices and the
    italic companion stylesheet from other builds, and a `PlanetaireMonoText-*.woff2`
    glob sweeps whatever happens to be sitting there into the published directories —
    which is how 21 stale split files were published from a dirty fonts/output (plt-pu35).
    """
    names = text_web_font_file_names()
    missing = [name for name in names if not (FONT_OUTPUT / name).exists()]
    if missing:
        fail(
            f"fonts/output is missing {len(missing)} of the {len(names)} published web "
            f"font file(s) ({', '.join(missing[:4])}...). Run the font build first, or "
            "drop --no-build."
        )

    target_dir.mkdir(parents=True, exist_ok=True)
    for stale in sorted(target_dir.iterdir()):
        if stale.name not in names and not stale.name.startswith("."):
            print(f"  {target_dir.relative_to(REPO_ROOT)}/{stale.name}: removing (not published)")
            stale.unlink()
    for name in names:
        shutil.copy2(FONT_OUTPUT / name, target_dir / name)
    rel = target_dir.relative_to(REPO_ROOT)
    print(f"  {rel}/: refreshed {len(names)} Text web font file(s)")
    return len(names)


def sync_web_fonts() -> None:
    """Refresh both the public CDN copy and the Pages-local copy."""
    public_count = sync_web_font_dir(PUBLIC_WEB_FONTS)
    site_count = sync_web_font_dir(SITE_FONTS)
    if public_count != site_count:
        fail("fonts/web and site/fonts refreshed different file counts")


def verify_web_font_version(version: str) -> None:
    """Check that every synced web font stamps `version`, before anything is committed.

    The build takes the version from the latest git tag unless it is told otherwise,
    and at release time that tag is the *previous* release. Stamping is now explicit,
    so this is the assertion that it stayed explicit — and it is the check that catches
    a `--no-build` run reusing a fonts/output built at some other version (plt-0204).
    """
    expected_name = f"Version {version}"
    expected_revision = to_font_revision(version)
    problems: list[str] = []
    for target_dir in (PUBLIC_WEB_FONTS, SITE_FONTS):
        for name in text_web_font_file_names():
            path = target_dir / name
            if path.suffix != ".woff2":
                continue
            font = TTFont(path)
            stamped = font["name"].getDebugName(5)
            revision = round(font["head"].fontRevision, 3)
            rel = path.relative_to(REPO_ROOT)
            if stamped != expected_name:
                problems.append(f"{rel}: name ID 5 is {stamped!r}, expected {expected_name!r}")
            if revision != expected_revision:
                problems.append(
                    f"{rel}: head.fontRevision is {revision}, expected {expected_revision}"
                )
    if problems:
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        fail(
            f"the synced web fonts do not stamp {version}. Rebuild them with the version "
            f"being released: `uv run planetaire build text --version {version}`."
        )
    print(f"  fonts/web and site/fonts both stamp Version {version}")


def validate_public_web_fonts() -> None:
    """Validate exactly the web fonts the release just synced.

    `sync_web_fonts` is the last thing that touches what jsDelivr will serve, so the
    gate belongs here rather than on the build output alone: the release must validate
    the bytes it is about to commit.
    """
    paths = sorted(PUBLIC_WEB_FONTS.glob("*.woff2"))
    if not paths:
        fail("no WOFF2 files in fonts/web to validate; the web font sync did not produce any")
    rels = [str(path.relative_to(REPO_ROOT)) for path in paths]
    uv_run(["planetaire", "validate", *rels])


def format_repinned_sources() -> None:
    """Re-run the site formatter so the re-pin leaves canonically formatted files.

    `rewrite_cdn_links` is a raw search/replace, so shortening a ref (e.g. a 40-char
    commit SHA -> `@vX.Y.Z`) can leave a line that Biome would wrap differently. Without
    this, the release commit lands JS/CSS that the `site:check:format` CI gate rejects
    (this exact case broke CI on the v0.1.5 release commit). `npm run site:format` is
    idempotent on already-formatted files, so it only touches what the re-pin changed.
    """
    run(["npm", "run", "site:format"])


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
        uv_run(["planetaire", "build", "download"])
        # `--version` for the same reason the specimen gets one: these binaries are
        # committed, and the tag they must name does not exist until finalize.
        uv_run(["planetaire", "build", "planetaire-mono", "--version", version])
        uv_run(["planetaire", "build", "text", "--version", version])

    print("\nRefresh web fonts:")
    sync_web_fonts()

    print("\nCheck the web fonts stamp this release:")
    verify_web_font_version(version)

    print("\nValidate public web fonts:")
    validate_public_web_fonts()

    print("\nBuild specimen:")
    uv_run(["planetaire", "build", "specimen", "--version", version])

    print("\nRe-pin CDN links:")
    rewrite_cdn_links(tag)

    print("\nFormat re-pinned sources:")
    format_repinned_sources()

    if not out(["git", "status", "--porcelain", "--", *RELEASE_PATHS]):
        fail("nothing changed — the web fonts, PDF, and CDN pins already match this version")

    print(f"\nPrepared {tag}. Review the changes below, then finalize.\n")
    run(["git", "--no-pager", "diff", "--stat", "--", *RELEASE_PATHS])
    print()
    run(["git", "--no-pager", "diff", "--", *CDN_PINNED_PATHS])
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
    # Guard against a stray version: the PDF must stamp this tag and all production CDN
    # links must point at it, so a finalize for the wrong version cannot slip through.
    current_refs = sorted({ref for refs in cdn_refs_by_path().values() for ref in refs})
    if current_refs != [tag]:
        fail(
            f"release-controlled CDN links are not all pinned to {tag} "
            f"(found: {', '.join('@' + ref for ref in current_refs) or 'none'}). "
            f"Re-run `make release VERSION={version}` so the prepared changes match the "
            "version you are finalizing."
        )

    print("\nCommit and tag:")
    run(["git", "commit", "-m", f"release: {tag}", "--", *RELEASE_PATHS])
    run(["git", "tag", "-a", tag, "-m", tag])

    if args.skip_rebuild_check:
        print("\nSkipping the rebuild check (--skip-rebuild-check).")
    else:
        # Only now does the tag exist, so only now can this be asked the way CI asks
        # it: rebuild from the tagged commit's sources and compare byte for byte. Run
        # here rather than only in CI so a mismatched release is caught before it is
        # pushed, which is what the v0.2.0 release needed (plt-0204).
        print("\nCheck the committed web fonts match a rebuild at the tag:")
        uv_run(["python", "devtools/check_web_fonts.py"])

    print("\nDone. Push to publish (this script does not push):")
    print("  git push origin main")
    print(f"  git push origin {tag}        # fires release-fonts.yml")
    print("  # In a Claude Code web session the git proxy rejects tag pushes; instead:")
    print(f"  # gh api repos/jlevy/planetaire/git/refs -f ref=refs/tags/{tag} \\")
    print(f'  #   -f sha="$(git rev-parse {tag}^{{commit}})"')


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="step", required=True)

    p = sub.add_parser("prepare", help="Build + refresh web fonts + re-pin CDN links")
    p.add_argument("version", help="Release version, e.g. 0.1.4 (no leading v)")
    p.add_argument(
        "--no-build", action="store_true", help="Reuse fonts/output instead of rebuilding"
    )
    p.set_defaults(func=cmd_prepare)

    f = sub.add_parser("finalize", help="Commit + tag the prepared (reviewed) changes")
    f.add_argument("version", help="Release version, e.g. 0.1.4 (no leading v)")
    f.add_argument(
        "--skip-rebuild-check",
        action="store_true",
        help="Skip the post-tag rebuild comparison (CI runs it too; this only saves time)",
    )
    f.set_defaults(func=cmd_finalize)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
