# Building and Releasing the Fonts

This guide covers the font-specific workflow.
For generic Python/uv setup see [development.md](development.md); for PyPI publishing of
the *tooling* see [publishing.md](publishing.md); for the full asset-regeneration
reference (hero image, specimen, terminal demo, external tools) see
[build-assets.runbook.md](build-assets.runbook.md).

> **What ships where:** the **fonts** are published as GitHub Release assets; the **PyPI
> package** is the build tooling only.

## Prerequisites

- **uv** and Python 3.12+ (`uv sync --all-extras`).
- **FontForge:** *optional*. Only needed to regenerate the intermediate Medium and
  ExtraBold weights from the base weights.
  The generated weights are vendored under `fonts/source/`, so a normal build does not
  need FontForge.
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
| **Planetaire Mono Text** (local text TTFs) | `planetaire build text --formats ttf` | `PlanetaireMonoText-*.ttf` |
| **Planetaire Mono Text** (slim web) | `planetaire build text --split --italics` | `PlanetaireMonoText-{Regular,Bold}{,Italic}-{latin,latin-ext,greek,cyrillic,cyrillic-ext}.woff2`, `planetaire-mono-text.css`, and `planetaire-mono-text-italics.css` |

Text is the full build subset to standard-Unicode text glyphs (letters, punctuation,
box-drawing, block elements, geometric shapes), dropping the Private-Use Nerd Font icons
and Powerline. The release archive keeps that full Text coverage in `ttf/`, but the
`web/` folder uses a Google Fonts-style split: Regular/Bold upright as the base CSS,
Latin, Latin Extended, Greek, Cyrillic, and Cyrillic Extended WOFF2 files, plus an
optional Regular/Bold italic companion CSS. Browsers fetch only the unicode ranges and
styles a page actually uses, so adding Greek/Cyrillic support does not increase the font
payload for Latin-only pages. The generated CSS also includes a local metric-matched
fallback face and a
`--planetaire-mono-text-font-stack` custom property for stable line height during
`font-display: swap`.

Additional named split subsets can be requested with `--subsets`, using the subset names
defined in `src/planetaire/config.py`. `greek-ext` is defined for parity with the Google
Fonts model, but the current Text font has no encoded Greek Extended (`U+1F00-1FFF`)
coverage, so the build warns and skips that file.

## Build

```shell
make fonts        # download(verify) -> build Extended -> build Text -> validate
# or individually:
uv run planetaire build planetaire-mono
uv run planetaire build text --formats ttf
uv run planetaire build text --split --italics
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

Releases are tag-driven.
The version tag (`vX.Y.Z`) is the single source of truth for the version:
`uv-dynamic-versioning` derives the package and font version from it, and
`planetaire.version.get_version()` threads the same value into the font name tables,
`head.fontRevision`, and the specimen.

Two artifacts must agree with the tag *and* live inside the tagged commit:

- **The specimen PDF** (`docs/specimen/planetaire-mono-specimen.pdf`) stamps
  `Version X.Y.Z` on its cover and is served over the jsDelivr CDN.
- **The README CDN link** is pinned to the tag —
  `cdn.jsdelivr.net/gh/jlevy/planetaire@vX.Y.Z/...` — so it is immutable, served
  instantly, and always resolves to the PDF that stamps that same version.
  (Versioned jsDelivr refs are cached for a year; an `@main` link would lag up to ~12h
  and could disagree with the PDF’s stamped version.)

This is a chicken-and-egg: the version comes *from* the tag, but the PDF content and the
README link must be *in* the tagged commit.
`scripts/release.py` resolves it by stamping the version explicitly, so **always cut
releases with `make release`** rather than tagging by hand.
Doing it by hand leaves the committed PDF and CDN link pointing at a stale version.

> **Download links are deliberately not pinned.** The `releases/latest/download/...`
> URLs in the README and the generated site resolve `latest` server-side, and the
> release archive names are unversioned, so those URLs stay stable across releases and
> never need updating — only the CDN specimen link is version-pinned.

### 1. Write the release notes

Add a notes file at `docs/release/notes/<tag>.md` (for example
`docs/release/notes/v0.1.4.md`). Copy
[`docs/release/notes/TEMPLATE.md`](release/notes/TEMPLATE.md), fill in the
release-specific changes, and replace the compare link with the previous and new tags.
`release-fonts.yml` reads this file verbatim as the GitHub Release body and now fails if
the file is missing; do not rely on GitHub’s auto-generated notes for font releases.

The release page is the downloads page, so every notes file should keep the context from
the template:

- product intro and links to the [repo](https://github.com/jlevy/planetaire),
  [README](https://github.com/jlevy/planetaire#readme),
  [download/install instructions](https://github.com/jlevy/planetaire#download), and
  [web-font usage](https://github.com/jlevy/planetaire#use-on-the-web)
- **Which package?** guidance for Extended vs. Text
- archive contents (`ttf/`, `web/`, `README.txt`, `LICENSE`, `licenses/`)
- checksum guidance for `SHA256SUMS`
- **## What’s Changed** sections and a **Full Changelog** compare link

Commit the notes file to `main` **before** running the release script, so the tagged
commit contains the notes the workflow reads. The release files (`README.md` and the
specimen PDF) must have no other uncommitted changes, so the review diff shows only what
the release introduces. `make release` and `make release-finalize` both refuse to run if
the curated notes file is missing or has uncommitted changes.

### 2. Prepare the release and review it

```shell
make release VERSION=0.1.4        # or: uv run python scripts/release.py prepare 0.1.4
```

This builds the fonts, rebuilds the specimen PDF stamped `Version 0.1.4`, and re-pins
every README jsDelivr CDN link to `planetaire@v0.1.4` (a plain search/replace from the
previous ref — no template variables — which also busts the CDN cache, since `@v0.1.4`
is a URL jsDelivr has never served).
It then **stops and prints the diff** — nothing is committed yet.
It refuses to run off `main`, when the tag already exists, or when the release files
have unrelated uncommitted changes.
Use `--no-build` to reuse an existing `fonts/output`.

Review the printed diff: confirm both README CDN links now point at `@v0.1.4` and the
specimen PDF was rebuilt.
To discard and start over, run the `git checkout` the script prints.

### 3. Finalize the release

```shell
make release-finalize VERSION=0.1.4   # or: uv run python scripts/release.py finalize 0.1.4
```

This commits the PDF + README as `release: v0.1.4` and creates the annotated tag
`v0.1.4` on that commit.
It re-checks that you are on `main`, the tag is free, and the README is actually pinned
to `v0.1.4`, then commits only those two files.
It does **not** push — so nothing publishes as a side effect.

### 4. Push the commit and tag

Pushing the tag is the trigger; push the release commit first so the tag’s commit exists
on `main`. Prefer `gh` (the GitHub API): it works everywhere, including Claude Code web
sessions where the git proxy rejects tag pushes (`git push <tag>` returns HTTP 403).

```shell
git push origin main
gh api repos/jlevy/planetaire/git/refs \
  -f ref=refs/tags/v0.1.4 \
  -f sha="$(git rev-parse v0.1.4^{commit})"   # fires release-fonts.yml
```

From a local checkout with tag-push access you can push the tag with git instead (the
script already created the annotated tag):

```shell
git push origin v0.1.4
```

> **`gh` in web sessions:** managing releases needs `gh auth login` with the `repo` and
> `workflow` scopes — the `workflow` scope is what lets the tag-creation event trigger
> `release-fonts.yml` (events from a bare `GITHUB_TOKEN` would not).
> In web sessions the git remote points at a local proxy, so pass `-R jlevy/planetaire`
> to `gh run` / `gh release` subcommands that otherwise infer the repo from the remote.

Either way the tag fires `.github/workflows/release-fonts.yml`, which builds both
families, creates the GitHub Release for the tag, and uploads the archives:

- `PlanetaireMono-Extended.tar.xz` / `.zip`: the full family (TTF + WOFF2 + `@font-face`
  CSS, all Nerd Font icons), with the README and license texts
- `PlanetaireMono-Text.tar.xz` / `.zip`: the Text subset (TTF + WOFF2 + `@font-face`
  CSS), with the README and license texts
- `SHA256SUMS`: checksums for every archive

It keys off the tag push directly rather than chaining off the `release: published`
event, because the Release is created with the workflow’s `GITHUB_TOKEN` and events
raised by that token do not trigger further workflows.
To rebuild and re-upload assets (or refresh the notes) for an existing tag, run
`release-fonts.yml` manually from the Actions tab and pass the tag.

### 5. Verify the GitHub Release downloads page

After `release-fonts.yml` passes, open
`https://github.com/jlevy/planetaire/releases/tag/vX.Y.Z` and verify the page exactly as
a new user will see it:

- Title is `Planetaire Mono vX.Y.Z`.
- Body uses the curated `docs/release/notes/vX.Y.Z.md` text, including repo/README,
  install, web-font, package-choice, archive-content, checksum, and changelog links.
- Assets are present: `PlanetaireMono-Extended.tar.xz`, `PlanetaireMono-Extended.zip`,
  `PlanetaireMono-Text.tar.xz`, `PlanetaireMono-Text.zip`, and `SHA256SUMS`.
- `gh release view vX.Y.Z` and the web page both show the expected notes.
- `https://github.com/jlevy/planetaire/releases/latest` resolves to the new tag.

For a quick CLI check:

```shell
gh release view vX.Y.Z --repo jlevy/planetaire
gh release download vX.Y.Z --repo jlevy/planetaire --pattern SHA256SUMS --dir /tmp/planetaire-release-check
```

`.github/workflows/publish.yml` (PyPI) is **manual-only** for now: the tag does **not**
publish to PyPI. Pilot releases ship as GitHub Release assets only; run `publish.yml`
from the Actions tab once trusted publishing is configured for the project.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
