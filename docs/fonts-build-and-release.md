# Building and Releasing the Fonts

This guide covers the font-specific workflow.
For generic Python/uv setup see [development.md](development.md); for PyPI publishing of
the *tooling* see [publishing.md](publishing.md); for the full asset-regeneration
reference (hero image, specimen, terminal demo, external tools) see
[build-assets.runbook.md](build-assets.runbook.md).

> **What ships where:** the **fonts** are published as GitHub Release assets; the **PyPI
> package** is the build tooling only.

## Prerequisites

- **uv** + Python 3.12+ (`uv sync --all-extras`).
- **FontForge** — *optional*. Only needed to regenerate the intermediate Medium and
  ExtraBold weights from the base weights.
  The generated weights are vendored under `fonts/source/`, so a normal build does not
  need FontForge.
- **Typst** — *optional*. Only needed to compile the PDF specimen
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
| **Planetaire Mono Text** (web/regular) | `planetaire build text` | `PlanetaireMonoText-*.{ttf,woff2,woff}` + `planetaire-mono-text.css` |

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

1. **Merge** — copy B612 letter/digit/Greek/Cyrillic outlines into the Hack base,
   normalizing UPM 2048 → 2000. Donor TrueType hinting is stripped so B612 letters
   render with grayscale AA (Hack’s glyphs keep their native hinting).
2. **Rename** — set family/subfamily/PostScript names, weight class, and the version
   (name IDs 3/5 + `head.fontRevision`) from the canonical package version.
3. **Dotted zero** — add the center-dot zero (`ss01`/`zero` alternates).
4. **Fix** — DSIG, `fsType=0`, GASP.
5. **Validate** — glyph coverage, weight, and italic/bold style-linking.

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

The fonts are released by `.github/workflows/release-fonts.yml` when a GitHub Release is
published (tag like `v0.1.0`). It builds both families and uploads:

- `PlanetaireMono-Extended.tar.xz` / `.zip` — full TTFs
- `PlanetaireMono-Text.tar.xz` / `.zip` — Text TTF + WOFF2 + WOFF + `@font-face` CSS
- `SHA256SUMS` — checksums for every archive

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
