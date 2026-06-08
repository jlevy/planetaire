# Building and Releasing the Fonts

This guide covers the font-specific workflow. For generic Python/uv setup see
[development.md](development.md); for PyPI publishing of the *tooling* see
[publishing.md](publishing.md); for the full asset-regeneration reference (hero image,
specimen, terminal demo, external tools) see
[build-assets.runbook.md](build-assets.runbook.md).

> **What ships where:** the **fonts** are published as GitHub Release assets; the **PyPI
> package** is the build tooling only.

## Prerequisites

- **uv** and Python 3.12+ (`uv sync --all-extras`).
- **FontForge:** *optional*. Only needed to regenerate the intermediate Medium and
  ExtraBold weights from the base weights. The generated weights are vendored under
  `fonts/source/`, so a normal build does not need FontForge.
- **Typst:** *optional*. Only needed to compile the PDF specimen
  (`planetaire build specimen`).

WOFF2/WOFF output needs `brotli`/`zopfli`, pulled in automatically via
`fonttools[woff]`.

## Source fonts

The B612 and Hack Nerd Font sources are vendored under `fonts/source/{b612,hack}` and
recorded in `fonts/source/SHA256SUMS`. Verify their integrity with:

```shell
uv run planetaire build download   # locate + checksum-verify sources
```

(Network fetching from upstream is not yet implemented; the command verifies the
vendored copies.)

## The two families

| Family | Command | Output |
| --- | --- | --- |
| **Planetaire Mono Extended** (full) | `planetaire build planetaire-mono` | `PlanetaireMonoExtended-*.ttf` (all Nerd Font icons) |
| **Planetaire Mono Text** (web/regular) | `planetaire build text` | `PlanetaireMonoText-*.{ttf,woff2,woff}` and `planetaire-mono-text.css` |

Text is the full build subset to standard-Unicode text glyphs (letters, punctuation,
box-drawing, block elements, geometric shapes), dropping the Private-Use Nerd Font icons
and Powerline, and shipped unhinted for the web (~55 KB WOFF2/weight).

## Build

```shell
make fonts        # download(verify) -> build Extended -> build Text -> validate
# or individually:
uv run planetaire build planetaire-mono
uv run planetaire build text
uv run planetaire validate fonts/output/PlanetaireMonoExtended-*.ttf
uv run planetaire validate fonts/output/PlanetaireMonoText-*.ttf
```

Outputs land in `fonts/output/` (gitignored).

### Pipeline (per variant)

1. **Merge:** copy B612 letter/digit/Greek/Cyrillic outlines into the Hack base,
   normalizing UPM 2048 → 2000. Donor TrueType hinting is stripped so B612 letters
   render with grayscale AA (Hack’s glyphs keep their native hinting).
2. **Rename:** set family/subfamily/PostScript names, weight class, and the version
   (name IDs 3/5 and `head.fontRevision`) from the canonical package version.
3. **Dotted zero:** add the center-dot zero (`ss01`/`zero` alternates).
4. **Fix:** DSIG, `fsType=0`, GASP.
5. **Validate:** glyph coverage, weight, and italic/bold style-linking.

## Regression checks

Per-glyph hashes are stored (gzipped) in `fonts/golden/manifest.json.gz`.

```shell
uv run planetaire regression verify     # fail on outline drift
uv run planetaire regression generate   # regenerate after an intended change
```

CI runs `build → validate → regression verify` on every push (the `fonts` job in
`ci.yml`).

## Specimens

```shell
make specimen        # PDF (needs Typst); version is injected automatically
make html-specimen   # static specimen.html using the Text web fonts
```

## Releasing

Releases are tag-driven. Pushing a version tag (`vX.Y.Z`) is the only trigger and the
single source of truth for the version, which `uv-dynamic-versioning` derives from the
tag and threads into the font name tables, `head.fontRevision`, and the specimen.

### 1. Write the release notes

Add a notes file at `docs/release/notes/<tag>.md` (for example
`docs/release/notes/v0.1.3.md`). `release-fonts.yml` reads it verbatim as the GitHub
Release body; if no file exists for the tag it falls back to GitHub's auto-generated
notes. Match the previous releases: a short product intro, a **Which package?** section,
then **## What's Changed** and a **Full Changelog** compare link (see the
[Release Notes Format](publishing.md#release-notes-format) in publishing.md, and the
existing files under `docs/release/notes/` for examples).

Commit the notes file (and any other changes) to `main` **before** tagging, so the
tagged commit contains the notes the workflow reads.

### 2. Cut the tag

Tag the `main` commit that carries the notes file. Prefer `gh` (the GitHub API): it works
everywhere, including Claude Code web sessions where the git proxy rejects tag pushes
(`git push <tag>` returns HTTP 403).

```shell
# Lightweight tag on the current main; fires release-fonts.yml.
gh api repos/jlevy/planetaire/git/refs \
  -f ref=refs/tags/v0.1.3 \
  -f sha="$(git rev-parse origin/main)"
```

From a local checkout with tag-push access you can push the tag with git instead
(annotated is fine — the workflow only needs the tag to exist on the remote):

```shell
git tag -a v0.1.3 -m "v0.1.3" && git push origin v0.1.3
```

> **`gh` in web sessions:** managing releases needs `gh auth login` with the `repo` and
> `workflow` scopes — the `workflow` scope is what lets the tag-creation event trigger
> `release-fonts.yml` (events from a bare `GITHUB_TOKEN` would not). In web sessions the
> git remote points at a local proxy, so pass `-R jlevy/planetaire` to `gh run` / `gh
> release` subcommands that otherwise infer the repo from the remote.

Either way the tag fires `.github/workflows/release-fonts.yml`, which builds both
families, creates the GitHub Release for the tag, and uploads the archives:

- `PlanetaireMono-Extended.tar.xz` / `.zip`: the full family (TTF + WOFF2 + `@font-face`
  CSS, all Nerd Font icons), with the README and license texts
- `PlanetaireMono-Text.tar.xz` / `.zip`: the Text subset (TTF + WOFF2 + `@font-face`
  CSS), with the README and license texts
- `SHA256SUMS`: checksums for every archive

It keys off the tag push directly rather than chaining off the `release: published`
event, because the Release is created with the workflow's `GITHUB_TOKEN` and events
raised by that token do not trigger further workflows. To rebuild and re-upload assets
(or refresh the notes) for an existing tag, run `release-fonts.yml` manually from the
Actions tab and pass the tag.

`.github/workflows/publish.yml` (PyPI) is **manual-only** for now: the tag does **not**
publish to PyPI. Pilot releases ship as GitHub Release assets only; run `publish.yml`
from the Actions tab once trusted publishing is configured for the project.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
