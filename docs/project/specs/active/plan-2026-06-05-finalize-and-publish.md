# Feature: Finalize & Publish Planetaire Mono

**Date:** 2026-06-05 (last updated 2026-06-05)

**Author:** jlevy (with engineering review by Claude Code)

**Status:** Draft

## Overview

Bring Planetaire Mono from an early-stage build pipeline to a polished, published
font family. This plan operationalizes the findings in
[`docs/engineering-review.md`](../../../engineering-review.md): fix font-metadata
and packaging correctness, split the family into a lightweight **Text** build and a
full **Extended** build, give the actual font artifacts real CI coverage, correct
documentation drift, and systematize presentation (README imagery, PDF specimen,
a generated HTML specimen, a terminal-output demo, and static site pages).

Work is tracked under epic **`plt-toa7`** ("Polish Planetaire Mono to
published-release quality"), with every bead linked to this spec.

## Goals

- Ship two clearly-branded families from one pipeline:
  - **Planetaire Mono Text** — clean, standard-Unicode coverage for websites and
    regular use: letters, punctuation, Greek/Cyrillic, plus box-drawing, block
    elements, and geometric shapes (used in markdown tables, TUI output, and ASCII
    art — e.g. Claude Code's graphics). Drops only the **thousands of Nerd Font PUA
    icons** and Powerline. Measured: **~1,376 glyphs, ~53 KB WOFF2/weight** vs
    ~984 KB for the full build — roughly **18× smaller**. Web-ready (WOFF2/WOFF)
    with a generated `@font-face` stylesheet.
  - **Planetaire Mono Extended** — the full build with Nerd Font icons and all the
    terminal/coding glyphs (the current output, renamed). "Extended" leaves room to
    grow beyond Nerd Font additions later.
- Make font metadata correct and self-consistent: a single version source threaded
  through name tables, `head.fontRevision`, and the specimen.
- Give the font artifacts real CI: build → validate → regression-verify on every
  change, not just at release.
- Fix documentation drift (variant counts, Jinja artifact) and placeholder package
  metadata.
- Systematize presentation so the README image, PDF specimen, and HTML specimen
  share one reproducible rendering story; add a clean terminal-output demo (static
  SVG + animated) and develop static site pages (local dev; deployment deferred).
- Reduce repo weight (13 MB golden manifest, ~35 MB vendored TTFs).

## Non-Goals

- Designing new letterforms from scratch (we continue to compose B612 + Hack).
- Deploying the static site to a host. This plan develops the **pages**; hosting
  (GitHub Pages vs separate repo/domain) is deferred per owner direction.
- Variable-font output or OpenType features beyond what sources provide + the
  existing dotted-zero (`ss01`/`zero`).

## Background

See [`docs/engineering-review.md`](../../../engineering-review.md) (2026-06-05) for
the full review. Key facts that shape this plan:

- The full build is **12,138 glyphs / ~2.6–4.5 MB per TTF**; **~88% of glyphs are
  Nerd Font icons living in the PUA** (U+E000–F8FF and U+F0000+).
- Baseline (non-Nerd) Hack contributes only **~1,387 standard-Unicode glyphs**,
  which already include Box Drawing (128), Block Elements (32), Geometric Shapes
  (96), Arrows (109), Math Operators (177), and native Powerline (38, in PUA).
- Built fonts currently report **Hack's** version string
  (`Version 3.003 … Nerd Fonts 3.3.0`); the specimen separately hardcodes `0.1.0`.
- CI (`ci.yml`) only lints + tests Python; it never builds or validates the fonts.
- The build is verified working: all 8 variants build, lint clean, 113 tests pass.

### Glyph-scope decision for the Text family

"Text" is for websites and regular reading, plus the line-drawing characters that
modern CLIs and docs actually render. The single big cut is the **~10,400 Nerd Font
PUA icons** — that is where essentially all the size lives. Box-drawing and friends
are tiny (~314 glyphs, ~8 KB WOFF2) and worth keeping:

| Block | In **Text** | In **Extended** | Notes |
|-------|:-----------:|:---------------:|-------|
| Basic Latin, Latin-1, Latin Extended-A/B | yes | yes | Core letterforms (B612) |
| Latin Extended Additional, Latin Extended-C | yes | yes | |
| Greek & Coptic, Cyrillic (+ Supplement) | yes | yes | Standard Unicode |
| General Punctuation, Currency, Super/Subscripts | yes | yes | Text typography |
| Letterlike, Number Forms | yes | yes | Small, text-useful |
| Arrows, Math Operators (common) | yes | yes | Useful in prose/docs |
| Box Drawing, Block Elements, Geometric Shapes | **yes** | yes | Tables, TUI, ASCII art (Claude Code, etc.) |
| Powerline (PUA) | no | yes | Terminal prompt segments |
| Nerd Font icons (PUA, ~10.4k) | no | yes | **The entire size difference** |

Measured on `PlanetaireMono-Regular` (pyftsubset, no hinting, layout kept):

| Build | Glyphs | TTF | WOFF2/weight |
|-------|------:|----:|-------------:|
| Full (Extended) | 11,938 | 2,571 KB | 984 KB |
| Text (lean, no box-drawing) | 1,062 | 110 KB | 45 KB |
| **Text (with box-drawing/blocks/shapes)** | **1,376** | **131 KB** | **53 KB** |

So Text lands at **~53 KB/weight WOFF2 (~18× smaller)**; including box-drawing costs
only ~8 KB over the lean variant. **Decision: include box-drawing, block elements, and
geometric shapes in Text; exclude only Powerline and the Nerd PUA icons.**

## Design

### Approach

Extend the existing `ops/` + `recipes/` architecture rather than rework it. Add a
subsetting op and a "Text" recipe that runs after the main merge; keep "Extended" as
the current pipeline output, renamed. Drive everything from `make` targets and a CLI
subcommand so the artifacts are fully reproducible.

### Components

- **`ops/subset.py`** (new) — thin wrapper over `fontTools.subset` taking a set of
  Unicode ranges; drops PUA/terminal blocks, prunes layout/GSUB to retained glyphs,
  and can emit TTF/WOFF/WOFF2.
- **`config.py`** — add `TEXT_SUBSET_RANGES` (and keep `PLANETAIRE_LETTER_RANGES`),
  plus family-name constants for `Planetaire Mono Text` / `Planetaire Mono Extended`.
- **`recipes/planetaire_mono.py`** — rename full-build family to "Planetaire Mono
  Extended"; add a `build_text(...)` path that subsets + renames to "Planetaire Mono
  Text" and writes WOFF2/WOFF/TTF.
- **`ops/rename.py`** / build — thread a real `version` (from git tag, same source as
  the Python package) into name IDs 3 & 5 and `head.fontRevision`.
- **Versioning helper** — single function resolving the canonical version for both
  package and fonts; injected into the Typst specimen at compile time.
- **`ops/validate.py`** — add style-linking assertions (italic/bold bits map to
  subfamily; weight class matches expected).
- **Presentation generators** — a make/CLI target rendering the README specimen image
  from the same Typst source as the PDF; a generated `specimen.html` using the Text
  WOFF2 via `@font-face`; a scripted terminal-demo (VHS `.tape`) producing static SVG
  + animated output; `site/` pages assembled from these (no deploy).
- **CI** — a Linux job (FontForge + Typst) running build/validate/regression-verify.

### API Changes

- New CLI: `planetaire build text` (Text family) and a flag or separate target for
  web formats; `planetaire build planetaire-mono` continues to produce Extended.
- `release-fonts.yml` packages both families (Extended TTFs as today; Text TTF + WOFF2
  + WOFF + `@font-face` CSS).
- Font family names change: current "Planetaire Mono" → "Planetaire Mono Extended".
  README, terminal-config, and specimen update accordingly.

## Implementation Plan

Two phases. Phase 1 makes the fonts correct, split, validated, and CI-covered
(revise/finalize/test). Phase 2 prepares publication assets (presentation/web).

### Phase 1: Correct, split, and CI-cover the fonts

- [ ] Unify font versioning from a single source → name IDs 3/5 + `head.fontRevision`
      + specimen injection (`plt-g5ht`).
- [ ] Add `ops/subset.py` + Text recipe; produce **Planetaire Mono Text** (subset)
      and rename full build to **Planetaire Mono Extended** (`plt-py0f`).
- [ ] Emit WOFF2 + WOFF + TTF for Text and a generated `@font-face` stylesheet
      (`plt-py0f`).
- [ ] Add CI job: build → validate → `regression verify` (FontForge + Typst, cached
      sources) (`plt-17qf`).
- [ ] Fix README Jinja `{{ }}` artifact; standardize variant count to 8; document the
      Text/Extended split and what ships where (`plt-1k7s`).
- [ ] Fix placeholder author/email; add project URLs (`plt-apwa`).
- [ ] Extend `validate` with style-linking assertions (`plt-b9na`).
- [ ] Audit composite/accented glyph component handling in `merge` (`plt-gqdz`).
- [ ] Decide & apply a single hinting policy for shipped fonts (`plt-d6t8`).
- [ ] Implement real `build download` with checksums, or relabel (`plt-jecp`).
- [ ] Shrink/relocate the 13 MB golden manifest; reconsider committed source TTFs
      (`plt-3fxa`).

### Phase 2: Publication & presentation assets

- [ ] Systematize the README home-page specimen image via the Typst render path
      (`plt-7b9q`).
- [ ] Polish the PDF specimen: version stamp, regenerate mock terminal data, add a
      Text/web page (`plt-7pcj`).
- [ ] Generate a clean static **HTML specimen** loading the Text WOFF2 (`plt-x4bn`).
- [ ] Clean terminal-output demo: static SVG (README) + animated (site) via VHS
      `.tape`, scripting real programs (e.g. Claude Code, `mark`) to show the font in
      live CLI use (`plt-wgvi`).
- [ ] Develop simple static **site pages** assembling the specimen + demo + downloads;
      deployment deferred (`plt-0d2l`).

## Testing Strategy

- **Unit:** new `ops/subset.py` (correct glyph set retained, PUA dropped, layout
  pruned, format round-trips); versioning helper; extended `validate` assertions.
- **Recipe/e2e:** Text build produces expected glyph count and the named blocks;
  Extended build unchanged except family name + version; WOFF2/WOFF decode and report
  the right family/weight.
- **Regression:** regenerate golden manifest for both families and wire
  `regression verify` into CI so glyph drift fails the build.
- **Visual:** specimen (PDF + HTML) and README image build without error from one
  source; spot-check accented Latin/Greek/Cyrillic against B612.
- **Gate:** `make` (lint + test) plus the new font-CI job must pass before release.

## Rollout Plan

1. Land Phase 1; regenerate golden manifests; confirm font-CI green.
2. Land Phase 2 assets.
3. Tag a release; `release-fonts.yml` publishes both families (Extended archive as
   today; Text TTF + WOFF2 + WOFF + CSS) with checksums. Static-site deployment is a
   later, separate step.

## Open Questions

- ~~Should Box Drawing / Block Elements be in Text?~~ **Resolved: yes** — they cost
  only ~8 KB WOFF2 and are used by markdown tables, TUIs, and ASCII art. Only Powerline
  and the Nerd PUA icons stay Extended-only.
- Renaming the current family to "Planetaire Mono Extended" changes the installed
  name; confirm that's acceptable for anyone already using "Planetaire Mono".
- Manifest slimming approach: compact/gzip in-repo vs CI fixture — pick during
  `plt-3fxa`.

## References

- [`docs/engineering-review.md`](../../../engineering-review.md) — full review (2026-06-05)
- [`docs/specs/font-pipeline-plan.md`](../../../specs/font-pipeline-plan.md) — original pipeline plan
- [`docs/specs/font-customization-notes.md`](../../../specs/font-customization-notes.md) — design evaluations
- Epic `plt-toa7` and its children (this spec's beads)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
