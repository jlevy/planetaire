# Feature: Finalize and Publish Planetaire Mono

**Date:** 2026-06-05 (last updated 2026-06-05)

**Author:** jlevy (with engineering review by Claude Code)

**Status:** Implemented

## Progress (2026-06-05)

**All beads complete.** Phase 1: doc/metadata fixes (`plt-1k7s`, `plt-apwa`); unified
versioning and specimen injection (`plt-g5ht`); style-linking validation (`plt-b9na`);
the **Text** family with WOFF2/WOFF and `@font-face` (`plt-py0f`); font CI job
(`plt-17qf`); dual-family release packaging (`plt-2epl`); checksum-verified
`build download` (`plt-jecp`); composite audit and guard (`plt-gqdz`); single hinting
policy, strip donor hinting (`plt-d6t8`); ExtraBold investigation (`plt-qj8x`); golden
manifest gzipped and completed and source-vendoring decision (`plt-3fxa`).

Phase 2: generated HTML specimen (`plt-x4bn`); static site generator (`plt-0d2l`);
build/release docs and web-install (`plt-ke43`); README hero rendered from Typst
(`plt-7b9q`); PDF specimen polished, version and build-date and Text page (`plt-7pcj`);
VHS terminal demo (`plt-wgvi`). Asset-regeneration is documented in
[`build-assets.runbook.md`](../../../build-assets.runbook.md).

**Deferred (noted, not blocking):** regenerating the illustrative mock terminal listing
in the PDF from live output (cosmetic).

## Overview

Bring Planetaire Mono from an early-stage build pipeline to a polished, published font
family. This plan operationalizes the findings in
[`docs/engineering-review.md`](../../../engineering-review.md): fix font-metadata and
packaging correctness, split the family into a lightweight **Text** build and a full
**Extended** build, give the actual font artifacts real CI coverage, correct
documentation drift, and systematize presentation (README imagery, PDF specimen, a
generated HTML specimen, a terminal-output demo, and static site pages).

Work is tracked under epic **`plt-toa7`** ("Polish Planetaire Mono to published-release
quality"), with every bead linked to this spec.

## Goals

- Ship two clearly-branded families from one pipeline:
  - **Planetaire Mono Text:** clean, standard-Unicode coverage for websites and regular
    use: letters, punctuation, Greek/Cyrillic, plus box-drawing, block elements, and
    geometric shapes (used in markdown tables, TUI output, and ASCII art, e.g. Claude
    Code’s graphics). Drops only the **thousands of Nerd Font PUA icons** and Powerline.
    Measured: **~1,376 glyphs, ~53 KB WOFF2/weight** vs ~984 KB for the full build,
    roughly **18× smaller**. Web-ready (WOFF2/WOFF) with a generated `@font-face`
    stylesheet.
  - **Planetaire Mono Extended:** the full build with Nerd Font icons and all the
    terminal/coding glyphs (the current output, renamed). “Extended” leaves room to grow
    beyond Nerd Font additions later.
- Make font metadata correct and self-consistent: a single version source threaded
  through name tables, `head.fontRevision`, and the specimen.
- Give the font artifacts real CI: build → validate → regression-verify on every change,
  not just at release.
- Fix documentation drift (variant counts, Jinja artifact) and placeholder package
  metadata.
- Systematize presentation so the README image, PDF specimen, and HTML specimen share
  one reproducible rendering story; add a clean terminal-output demo (static SVG +
  animated) and develop static site pages (local dev; deployment deferred).
- Reduce repo weight (13 MB golden manifest, ~35 MB vendored TTFs).

## Non-Goals

- Designing new letterforms from scratch (we continue to compose B612 and Hack).
- Deploying the static site to a host. This plan develops the **pages**; hosting (GitHub
  Pages vs separate repo/domain) is deferred per owner direction.
- Variable-font output or OpenType features beyond what sources provide and the existing
  dotted-zero (`ss01`/`zero`).

## Background

See [`docs/engineering-review.md`](../../../engineering-review.md) (2026-06-05) for the
full review. Key facts that shape this plan:

- The full build is **12,138 glyphs / ~2.6–4.5 MB per TTF**; **~88% of glyphs are Nerd
  Font icons living in the PUA** (U+E000–F8FF and U+F0000+).
- Baseline (non-Nerd) Hack contributes only **~1,387 standard-Unicode glyphs**, which
  already include Box Drawing (128), Block Elements (32), Geometric Shapes (96), Arrows
  (109), Math Operators (177), and native Powerline (38, in PUA).
- Built fonts currently report **Hack’s** version string
  (`Version 3.003 … Nerd Fonts 3.3.0`); the specimen separately hardcodes `0.1.0`.
- CI (`ci.yml`) only lints and tests Python; it never builds or validates the fonts.
- The build is verified working: all 8 variants build, lint clean, 113 tests pass.

### Glyph-scope decision for the Text family

“Text” is for websites and regular reading, plus the line-drawing characters that modern
CLIs and docs actually render. The single big cut is the **~10,400 Nerd Font PUA
icons**; that is where essentially all the size lives. Box-drawing and friends are tiny
(~314 glyphs, ~8 KB WOFF2) and worth keeping:

| Block | In **Text** | In **Extended** | Notes |
| --- | :---: | :---: | --- |
| Basic Latin, Latin-1, Latin Extended-A/B | yes | yes | Core letterforms (B612) |
| Latin Extended Additional, Latin Extended-C | yes | yes |  |
| Greek & Coptic, Cyrillic (+ Supplement) | yes | yes | Standard Unicode |
| General Punctuation, Currency, Super/Subscripts | yes | yes | Text typography |
| Letterlike, Number Forms | yes | yes | Small, text-useful |
| Arrows, Math Operators (common) | yes | yes | Useful in prose/docs |
| Box Drawing, Block Elements, Geometric Shapes | **yes** | yes | Tables, TUI, ASCII art (Claude Code, etc.) |
| Powerline (PUA) | no | yes | Terminal prompt segments |
| Nerd Font icons (PUA, ~10.4k) | no | yes | **The entire size difference** |

Measured on `PlanetaireMono-Regular` (pyftsubset, no hinting, layout kept):

| Build | Glyphs | TTF | WOFF2/weight |
| --- | ---: | ---: | ---: |
| Full (Extended) | 11,938 | 2,571 KB | 984 KB |
| Text (lean, no box-drawing) | 1,062 | 110 KB | 45 KB |
| **Text (with box-drawing/blocks/shapes)** | **1,376** | **131 KB** | **53 KB** |

So Text lands at **~53 KB/weight WOFF2 (~18× smaller)**; including box-drawing costs
only ~8 KB over the lean variant. **Decision: include box-drawing, block elements, and
geometric shapes in Text; exclude only Powerline and the Nerd PUA icons.**

## Design

### Approach

Extend the existing `ops/` and `recipes/` architecture rather than rework it. Add a
subsetting op and a “Text” recipe that runs after the main merge; keep “Extended” as the
current pipeline output, renamed. Drive everything from `make` targets and a CLI
subcommand so the artifacts are fully reproducible.

### Components

- **`ops/subset.py`** (new): thin wrapper over `fontTools.subset` taking a set of
  Unicode ranges; drops PUA/terminal blocks, prunes layout/GSUB to retained glyphs, and
  can emit TTF/WOFF/WOFF2.
- **`config.py`**: add `TEXT_SUBSET_RANGES` (and keep `PLANETAIRE_LETTER_RANGES`), plus
  family-name constants for `Planetaire Mono Text` / `Planetaire Mono Extended`.
- **`recipes/planetaire_mono.py`**: rename full-build family to “Planetaire Mono
  Extended”; add a `build_text(...)` path that subsets and renames to “Planetaire Mono
  Text” and writes WOFF2/WOFF/TTF.
- **`ops/rename.py`** / build: thread a real `version` (from git tag, same source as the
  Python package) into name IDs 3 and 5 and `head.fontRevision`.
- **Versioning helper**: single function resolving the canonical version for both
  package and fonts; injected into the Typst specimen at compile time.
- **`ops/validate.py`**: add style-linking assertions (italic/bold bits map to
  subfamily; weight class matches expected).
- **Presentation generators**: a make/CLI target rendering the README specimen image
  from the same Typst source as the PDF; a generated `specimen.html` using the Text
  WOFF2 via `@font-face`; a scripted terminal-demo (VHS `.tape`) producing static SVG
  and animated output; `site/` pages assembled from these (no deploy).
- **CI**: a Linux job (FontForge and Typst) running build/validate/regression-verify.

### API Changes

- New CLI: `planetaire build text` (Text family) and a flag or separate target for web
  formats; `planetaire build planetaire-mono` continues to produce Extended.
- `release-fonts.yml` packages both families (Extended TTFs as today; Text TTF, WOFF2,
  WOFF, and `@font-face` CSS).
- Font family names change: current “Planetaire Mono” → “Planetaire Mono Extended”.
  README, terminal-config, and specimen update accordingly.

## Implementation Plan

Two phases. Phase 1 makes the fonts correct, split, validated, CI-covered, and
release-packaged (revise/finalize/test). Phase 2 prepares publication assets
(presentation/web). The full breakdown is tracked as beads under epic `plt-toa7`;
blocker dependencies are noted inline and enforced in tbd (`tbd ready` / `tbd blocked`).

### Phase 1: Correct, split, CI-cover, and package the fonts

- [ ] Unify font versioning from a single source → name IDs 3/5, `head.fontRevision`,
  and specimen injection (`plt-g5ht`).
- [ ] Add `ops/subset.py` and Text recipe; produce **Planetaire Mono Text** (subset) and
  rename full build to **Planetaire Mono Extended** (`plt-py0f`).
- [ ] Emit WOFF2, WOFF, and TTF for Text and a generated `@font-face` stylesheet
  (`plt-py0f`; needs a `brotli` dependency for WOFF2).
- [ ] Add CI job: build → validate → `regression verify` (FontForge and Typst, cached
  sources) (`plt-17qf`).
- [ ] Package **both** families in `release-fonts.yml` (Extended TTF archive; Text TTF,
  WOFF2, WOFF, and `@font-face` CSS) with SHA-256 checksums (`plt-2epl`; blocked by
  `plt-py0f`, `plt-g5ht`).
- [ ] Fix README Jinja `{{ }}` artifact; standardize variant count to 8; document the
  Text/Extended split and what ships where (`plt-1k7s`).
- [ ] De-boilerplate docs: add a font build/release guide and WOFF2/`@font-face`
  web-install instructions; refresh `development/installation/publishing.md`
  (`plt-ke43`; blocked by `plt-py0f`).
- [ ] Fix placeholder author/email; add project URLs (`plt-apwa`).
- [ ] Extend `validate` with style-linking assertions (`plt-b9na`).
- [ ] Audit composite/accented glyph component handling in `merge` (`plt-gqdz`).
- [ ] Decide and apply a single hinting policy for shipped fonts (`plt-d6t8`).
- [ ] Implement real `build download` with checksums, or relabel (`plt-jecp`).
- [ ] Shrink/relocate the 13 MB golden manifest; reconsider committed source TTFs
  (`plt-3fxa`).
- [ ] Investigate the ~4.5 MB ExtraBold weight; decide ExtraBold icon coverage in
  Extended (`plt-qj8x`).

### Phase 2: Publication and presentation assets

- [ ] Systematize the README home-page specimen image via the Typst render path
  (`plt-7b9q`).
- [ ] Polish the PDF specimen: version stamp, regenerate mock terminal data, add a
  Text/web page (`plt-7pcj`; blocked by `plt-g5ht`, `plt-py0f`).
- [ ] Generate a clean static **HTML specimen** loading the Text WOFF2 (`plt-x4bn`;
  blocked by `plt-py0f`).
- [ ] Clean terminal-output demo: static SVG (README) and animated (site) via VHS
  `.tape`, scripting real programs (e.g. Claude Code, `mark`) to show the font in live
  CLI use (`plt-wgvi`).
- [ ] Develop simple static **site pages** assembling the specimen, demo, and downloads;
  deployment deferred (`plt-0d2l`; blocked by `plt-7b9q`, `plt-x4bn`, `plt-wgvi`).

## Testing Strategy

- **Unit:** new `ops/subset.py` (correct glyph set retained, PUA dropped, layout pruned,
  format round-trips); versioning helper; extended `validate` assertions.
- **Recipe/e2e:** Text build produces expected glyph count and the named blocks;
  Extended build unchanged except family name and version; WOFF2/WOFF decode and report
  the right family/weight.
- **Regression:** regenerate golden manifest for both families and wire
  `regression verify` into CI so glyph drift fails the build.
- **Visual:** specimen (PDF and HTML) and README image build without error from one
  source; spot-check accented Latin/Greek/Cyrillic against B612.
- **Gate:** `make` (lint and test) plus the new font-CI job must pass before release.

## Rollout Plan

1. Land Phase 1; regenerate golden manifests; confirm font-CI green.
2. Land Phase 2 assets.
3. Tag a release; `release-fonts.yml` publishes both families (Extended archive as
   today; Text TTF, WOFF2, WOFF, and CSS) with checksums. Static-site deployment is a
   later, separate step.

## Implementation Notes

Decisions taken while implementing, recorded here so they can be revisited:

- **Family naming (done).** The two families are **`Planetaire Mono Extended`** (full,
  files `PlanetaireMonoExtended-*.ttf`) and **`Planetaire Mono Text`** (web subset,
  `PlanetaireMonoText-*`). The full family was renamed from the original
  `Planetaire Mono`; family names are `config` constants (`FAMILY_NAME`,
  `TEXT_FAMILY_NAME`) and output filenames derive from them. The specimen, hero, demo,
  terminal-config docs, and release workflow were all updated accordingly. ("Planetaire
  Mono" remains the *project* name.)
- **Text drops TrueType hinting.** `build_text` subsets with `drop_hinting=True`. This
  kept full Text WOFF2s in the 53-77 KB/weight range before split delivery, and avoids
  carrying Hack’s hinting, which is tuned for Hack outlines rather than the merged B612
  letterforms. The hinting policy for the *full* TTFs is still open under `plt-d6t8`.
- **Measured old single-file Text output (Regular):** 1,317 glyphs, about 53 KB WOFF2
  after web metadata trims, vs ~2.6 MB TTF / ~984 KB WOFF2 for the full build. Current
  release web output is the smaller split profile: Regular/Bold, Latin + Latin Extended,
  with optional Regular/Bold italics.

## Open Questions

- ~~Should Box Drawing / Block Elements be in Text?~~ **Resolved: yes**: they cost only
  ~8 KB WOFF2 and are used by markdown tables, TUIs, and ASCII art. Only Powerline and
  the Nerd PUA icons stay Extended-only.
- ~~Hard-rename the full family to `Planetaire Mono Extended`?~~ **Done:** full family
  and filenames renamed; specimen/hero/demo/docs/release updated.
- ~~Manifest slimming approach?~~ **Done:** gzipped in-repo (~2 MB).

## References

- [`docs/engineering-review.md`](../../../engineering-review.md): full review
  (2026-06-05)
- [`docs/specs/font-pipeline-plan.md`](../../../specs/font-pipeline-plan.md): original
  pipeline plan
- [`docs/specs/font-customization-notes.md`](../../../specs/font-customization-notes.md):
  design evaluations
- Epic `plt-toa7` and its children (this spec’s beads)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
