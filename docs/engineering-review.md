# Planetaire Mono — Senior Engineering & Design Review

**Date:** 2026-06-05 (last updated 2026-06-05) **Reviewer:** Engineering review pass
(Claude Code) **Companion plan:**
[`docs/project/specs/active/plan-2026-06-05-finalize-and-publish.md`](project/specs/active/plan-2026-06-05-finalize-and-publish.md)
**Scope:** Full repository — font design & build pipeline, packaging & distribution,
documentation, and presentation (PDF specimen, README imagery, proposed web/site
assets).

This is a holistic review of the project as it stands today.
It records what is working well, what should be fixed or improved, and a prioritized
backlog. The backlog items are tracked as beads (see the `plt-*` IDs referenced
throughout and the summary table at the end).

* * *

## 1. Executive Summary

Planetaire Mono is in **good shape for an early-stage project**. The core idea — merging
B612’s cockpit-grade legible letterforms onto Hack Nerd Font’s complete programming/icon
infrastructure — is well-executed and clearly documented.
The build pipeline is clean, the code is typed and linted, the test suite is real (113
tests, all passing), and the PDF specimen is already detailed.

The project is **not yet at “published, polished font” quality**, mostly in areas that
were never given a senior pass: **font metadata/versioning correctness**, **distribution
ergonomics** (no lightweight/web build, large committed binaries), **CI coverage of the
actual font artifacts** (CI only tests the Python, never the fonts), and **presentation
systematization** (README images are hand-coded PIL canvases; there is no web specimen
or live demo).

### Health snapshot

| Area | Status | Notes |
| --- | --- | --- |
| Build pipeline | 🟢 Working | `build planetaire-mono` produces all 8 variants cleanly |
| Tests | 🟢 Passing | 113 passed; ops + recipes covered, incl. e2e |
| Lint / types | 🟢 Clean | ruff + basedpyright, 0 errors |
| Font metadata | 🟡 Bugs | Version string inherited from Hack; see §3.1 |
| Distribution | 🟡 Gaps | TTF-only; no web font / WOFF2; no minimal build |
| CI coverage | 🟡 Gap | CI never builds or validates the fonts |
| Docs accuracy | 🟡 Drift | Variant count says 10 / 8 / 6 in three places; Jinja artifact in README |
| Repo hygiene | 🟡 Heavy | ~13 MB golden manifest + ~35 MB source TTFs committed |
| Presentation | 🟡 Ad hoc | PIL-drawn PNGs; no HTML specimen, no live/animated demo |

Legend: 🟢 good · 🟡 needs work · 🔴 broken

* * *

## 2. What’s Working Well

These are deliberate strengths worth preserving as the project evolves.

- **Clean ops/recipes separation.** `ops/` holds single-purpose, pure-fontTools
  transforms (`merge`, `rename`, `fix`, `zero`, `validate`, `compare`, `regression`,
  `embolden`); `recipes/` composes them into the full build.
  The CLI (`cli.py`) is a thin Typer wrapper that defers imports per-command for fast
  startup. This is the right architecture and should be the template for new ops (e.g.
  the web-font subsetting op proposed below).
- **Pure-Python core, one optional system dep.** Only `embolden` needs FontForge;
  everything else is fontTools.
  The pipeline degrades gracefully (logs a warning, uses pre-generated weights) when
  FontForge is absent — verified in this environment, which has no FontForge yet still
  builds all 8 variants because the intermediate weights are vendored.
- **Dotted-zero implementation is genuinely good.** `ops/zero.py` builds a proper
  12-point quadratic-Bézier circle (default) and a rectangle alternate (`zero.ss01`),
  wires `ss01`/`zero` GSUB features into every script/langsys, and is idempotent (no-op
  if the dot already exists).
  This is careful, correct OpenType work.
- **Regression detection exists.** `ops/regression.py` + `regression generate/verify`
  give per-glyph hash manifests to catch unintended output drift.
  The *idea* is excellent (see §5 for the storage cost caveat).
- **The PDF specimen is substantive.** 11+ pages: cover, multilingual text, Turing / RFC
  1 / microGPT passages, Kerm-colored terminal mockup, full character set, weight
  ladder, legibility pairs, symbol tables, Nerd Font icon grids, provenance.
  Far beyond a stub.
- **Licensing is handled correctly.** OFL-1.1 for the font, MIT for the tooling, full
  upstream license texts vendored under `fonts/source/licenses/`, and the composite
  `license = "OFL-1.1 AND MIT"` SPDX expression in `pyproject.toml`.
- **Modern toolchain.** uv + hatchling + dynamic versioning, basedpyright, ruff,
  trusted-publishing to PyPI via OIDC. Good 2026-era defaults.

* * *

## 3. Font Design & Build — Findings

### 3.1 🔴 Font version metadata is inherited from Hack (correctness bug) — `plt-*`

The built fonts report **Hack’s** version, not Planetaire’s:

```
$ planetaire info fonts/output/PlanetaireMono-Regular.ttf
  Version: Version 3.003;[3114f1256]-release; ttfautohint (v1.7) ... ;Nerd Fonts 3.3.0
```

Root cause: `recipes/planetaire_mono.py` calls `rename_font(...)` **without** a
`version=`, and `ops/rename.py` only sets name ID 5 (version) and refreshes name ID 3
(unique ID) when `version` is provided.
So:

- name ID 5 (version string) → still Hack’s `3.003 … Nerd Fonts 3.3.0`
- name ID 3 (unique ID) → derived from Hack’s version too
- `head.fontRevision` → still Hack’s

Meanwhile the **Typst specimen hardcodes `#let version = "0.1.0"`** and the README gives
no font version at all.
There are now **three disagreeing version sources** (git tag → Python wheel, Hack’s
3.003 → font binary, 0.1.0 → specimen).

**Recommendation:** Establish a single version source (the git tag, same as the Python
package) and thread it through the build: set name IDs 3 & 5, `head.fontRevision`, and
inject it into the specimen at compile time.
This is the single most important fix before any public font release.

### 3.2 🟡 Verify composite/accented glyph component handling in `merge`

`merge_glyphs` copies each in-range codepoint’s glyph by name (`glyf`, `hmtx`, cmap).
For **composite glyphs** (accented Latin like `À`, many Greek/Cyrillic forms built from
base + combining mark components), the copied composite still references its component
glyphs **by name**. Those component glyphs (combining accents at U+0300+ etc.)
are **outside** `PLANETAIRE_LETTER_RANGES`, so they are *not* copied — the composite may
resolve against Hack’s component outlines (wrong shape) or a missing/blank glyph.

The e2e test compares against a reference build and passes, which suggests this is
working in the common cases, but it has not been audited deliberately.
**Action:** add a targeted check that renders/inspects a sample of accented Latin,
Greek, and Cyrillic glyphs and confirms they match B612’s intended outlines (and that no
composite references a missing component).
If issues are found, decompose composites on copy or pull in their components.

### 3.3 🟡 ExtraBold variants are ~4.5 MB (≈1.7× the others)

`PlanetaireMono-ExtraBold*.ttf` are ~4.5 MB vs ~2.6 MB for the rest.
The bloat is inherited from the Hack Nerd Font ExtraBold source (its icon outlines at
heavy weight are larger).
Not a bug, but worth quantifying and deciding whether the ExtraBold icon coverage is
worth the extra weight, especially once a slimmed web/text build exists (§4).

### 3.4 🟡 Hinting strategy is inconsistent between build and showcase

`scripts/generate_showcase.py` **strips** TrueType hinting (`prep`/`fpgm`/`cvt ` and
per-glyph programs) before rendering, with the comment *“merged font inherits Hack’s
hinting tables which are incompatible with B612 glyphs.”* That implies the **shipped
TTFs may carry hinting that is wrong for the B612-derived glyphs.** The build’s `fix`
step sets GASP for smoothing but does not address this.
**Action:** decide a single hinting policy for the shipped fonts — either strip hinting
from the B612-derived glyphs in the build (so the artifact matches what the showcase
proves looks good) or re-hint with ttfautohint.
The showcase shouldn’t need a secret fix the real font lacks.

### 3.5 🟢/🟡 Style-linking metadata

`rename_font` sets `usWeightClass` but relies on each source file already carrying
correct italic/bold bits (`fsSelection`, `head.macStyle`). Because the pipeline loads
the matching Hack style per variant (e.g. `HackNerdFont-Italic` for Italic), this is
generally correct. Worth an explicit assertion in `validate` (italic bit set ⇔ Italic
subfamily; weight class matches expected) so a future source swap can’t silently break
style linking. `validate` already checks weight; extend it.

* * *

## 4. Distribution & Packaging — Findings

### 4.1 🟡 No lightweight / web font build (requested) — `plt-*`

Today every variant is the full ~2.6–4.5 MB Nerd Font (12,138 glyphs).
For web embedding and “clean customized-weight monospace on a site,” that is far too
heavy and ships 11,000+ icons nobody needs for body text.

**Proposed: a second build target, “Planetaire Mono Text” (icon-free).**

- New op `ops/subset.py` (fontTools `subset`) producing a glyph set limited to the
  letterform/symbol ranges actually authored (Latin, Latin Extended, Greek, Cyrillic,
  punctuation, common symbols) — i.e. **drop the Nerd Font PUA icons**.
- Emit **WOFF2 + WOFF** (and keep TTF), per weight.
- Generate a ready-to-use `@font-face` CSS snippet and a `unicode-range`-split option
  for further savings.
- Expected impact: ~12,138 → ~700–1,200 glyphs; TTF ~2.6 MB → a few hundred KB; **WOFF2
  likely ~40–90 KB per weight.** This is the single biggest distribution win and
  directly enables the website work in §6.

Naming/branding decision needed (e.g. `Planetaire Mono` = full/Nerd,
`Planetaire Mono Text` = web/icon-free) — see open questions.

### 4.2 🟡 CI never builds or validates the fonts — `plt-*`

`.github/workflows/ci.yml` runs only `lint` + `pytest`. The actual font artifacts are
built **only** at release time (`release-fonts.yml`), and even then are *not* checked
against the golden manifest (`regression verify`) nor validated beyond a basic
`validate`. A pipeline change that corrupts glyphs would pass CI.

**Action:** add a CI job (Linux, with FontForge installed) that runs
`build download → build planetaire-mono → validate → regression verify`. Cache source
fonts. This makes the regression system actually load-bearing.

### 4.3 🟡 `build download` is a stub but docs imply real downloading

`recipes/sources.py::download_sources` does **not** download anything — it checks for
already-vendored files and raises if absent.
README says “Download source fonts and build all variants.”
Either implement real fetching (from polarsys/b612 and ryanoasis/nerd-fonts releases,
with checksums) or rename/relabel the step to “verify vendored sources” and update the
README. Implementing real downloads also unlocks dropping the binaries from git (§5).

### 4.4 🟡 `pyproject.toml` publish metadata is placeholder

`authors = [{ name="jlevy", email="changeme@example.com" }]`. The Typst cover hardcodes
“Joshua Levy.” `.copier-answers.yml` also carries `changeme@example.com`. Fix
author/email and consider adding `Homepage`/`Documentation` URLs before any PyPI
publish.

### 4.5 🟡 Dual-distribution is slightly confusing

The PyPI package ships the **build tooling**; the **fonts** ship via GitHub Releases.
That’s a reasonable split but should be stated plainly in the README so users don’t
`pip install planetaire` expecting a font.
A one-line “what ships where” note suffices.

* * *

## 5. Repository Hygiene — Findings

- **🟡 `fonts/golden/manifest.json` is ~13 MB** and committed.
  It stores per-glyph hashes for 12k glyphs × 8 variants as verbose JSON. Options: store
  only a hash of hashes per variant plus a compact binary/CBOR form, gzip it, or move to
  a fixture fetched in CI. A 13 MB JSON in every clone is a smell.
- **🟡 ~35 MB of source TTFs committed** (`fonts/source/hack/*ExtraBold*` are ~4.3 MB
  each). Acceptable for a self-contained font repo, but once `download` is real (§4.3),
  prefer fetching with checksums or Git LFS to keep clones light.
- **🟢 `.gitignore`** correctly keeps `fonts/output/` out (only `.gitkeep`).
- **🟡 Stale bead `plt-9r23`** ("Specimen PDF improvements — 10 items") is still
  `in_progress` though all of its blocked children are closed.
  Close it to clean the board.

* * *

## 6. Presentation — Findings & Plan

This is where “well-published font” is won or lost, and it’s the least developed area.
Four deliverables, in priority order.

### 6.1 🟡 README hero/specimen image: systematize, raise quality — `plt-*`

Current README PNGs are drawn imperatively in `scripts/generate_showcase.py` with PIL —
hand-placed `x/y` coordinates, per-token color tuples, manual hinting strip.
It works and is 2× DPI (1500px shown at 750), but it is brittle, hard to restyle, and a
different rendering path from the PDF (so the README and the specimen can drift
visually).

**Recommendation:** generate the home-page specimen from the **same Typst source** as
the PDF (Typst can export PNG/SVG at high DPI), or a dedicated small Typst “hero” doc.
One rendering path → one visual language, fully reproducible via a make target.
Keep it crisp (≥2×), dark-theme, showing real code + the legibility pairs + the dotted
zero.

### 6.2 🟡 Optimize & polish the PDF specimen — `plt-*`

The PDF is good but has rough edges: hardcoded `version = "0.1.0"` (wire to the real
version, §3.1), hardcoded directory listing / git hashes in the terminal mockup
(regenerate from real output so it never goes stale), and it should gain a
**web/text-font page** once §4.1 lands.
Tighten cover typography and ensure the font version + build date are stamped.
Driven by the existing `build specimen` recipe (Typst not installed in this environment
— add it to the toolchain/CI).

### 6.3 🟡 Clean, generated **static HTML specimen** (requested) — `plt-*`

A single self-contained `specimen.html` that loads the **web font** (§4.1) via
`@font-face` and reproduces the specimen content in the browser: weight ladder,
legibility pairs, character set, live `ss01` toggle, code sample.
Generated from a template (not hand-maintained) so it stays in sync.
This is the natural anchor for the site (§6.5).

### 6.4 🟡 Clean **terminal-output demo**, static and/or animated (requested) — `plt-*`

A polished, repeatable render of real terminal output in Planetaire Mono — prompt,
`eza --icons`, git log, syntax-highlighted code — proving the font in context.
Recommended approach: **VHS** (charmbracelet/vhs) or asciinema→agg to produce a crisp
SVG/GIF/MP4 from a scripted `.tape`, so it’s reproducible and updatable.
Static SVG for the README, optional animated version for the site.

### 6.5 🟡 Simple **static site** (requested) — `plt-*`

A minimal static site (single page is fine) hosting: the live HTML specimen (§6.3), the
terminal demo (§6.4), install/terminal-config instructions, and direct download links
for both the full and web/text builds.
Publish via GitHub Pages from a generated `site/` directory.
Keep it dependency-light and fully generated by a make target so it never rots.

* * *

## 7. Documentation — Findings

- **🔴 Jinja templating artifact in README.** The WezTerm block (README lines ~64–67)
  contains `config.font_rules = {{ … }}` — doubled braces left over from Copier/Jinja
  rendering. Should be single braces.
  Sweep the README for other `{{`/ `}}`.
- **🔴 Variant count disagrees across docs.** README says **“10 variants”** (and “build
  all 10 variants”), then later “all **8** variants”; `terminal-config.md` says **“6
  variants.”** The build produces **8**. Standardize on 8 everywhere
  (Regular/Italic/Medium/MediumItalic/Bold/BoldItalic/ExtraBold/ExtraBoldItalic).
- **🟡 Install docs are TTF-only.** Add WOFF2/`@font-face` web-install instructions once
  §4.1 lands.
- **🟡 Template boilerplate remains.** `docs/development.md`, `docs/installation.md`,
  `docs/publishing.md` are largely the simple-modern-uv template (generic Python
  packaging) and barely mention the font workflow (FontForge, Typst, `make fonts`,
  regression). Add a font-specific build/release guide; the generic uv content can stay
  but shouldn’t be the only guidance.
- **🟢 Provenance/credits** in README and specimen are accurate and well-attributed.

* * *

## 8. Prioritized Backlog (beads)

Tracked as beads under epic **`plt-EPIC`** ("Polish Planetaire Mono to published release
quality"). Priorities: **P1** = correctness/distribution blockers, **P2** =
quality/presentation.

| Priority | Item | Ref § |
| --- | --- | --- |
| P1 | Unify font versioning; stop inheriting Hack’s version (name IDs 3/5, fontRevision, specimen) | 3.1 |
| P1 | Add icon-free **web/text build** (subset → WOFF2/WOFF) + `@font-face` CSS | 4.1 |
| P1 | Add CI job that builds + validates + `regression verify`s the fonts | 4.2 |
| P1 | Fix README Jinja `{{ }}` artifact + standardize variant count (→ 8) | 7 |
| P2 | Audit composite/accented glyph component handling in `merge` | 3.2 |
| P2 | Decide & apply a single hinting policy for shipped fonts | 3.4 |
| P2 | Implement real `build download` (or relabel) + checksums | 4.3 |
| P2 | Fix placeholder author/email; add project URLs | 4.4 |
| P2 | Shrink/relocate the 13 MB golden manifest; reconsider committed source TTFs | 5 |
| P2 | Systematize the README home-page specimen PNG (single Typst render path) | 6.1 |
| P2 | Polish PDF specimen (version stamp, regenerate mock data, add web-font page) | 6.2 |
| P2 | Generate clean static **HTML specimen** | 6.3 |
| P2 | Clean terminal-output demo (static SVG + optional animated via VHS) | 6.4 |
| P2 | Simple generated **static site** (GitHub Pages) | 6.5 |
| P2 | Extend `validate` with style-linking assertions | 3.5 |
| P3 | Close stale parent bead `plt-9r23` | 5 |

* * *

## 9. Open Questions for the Owner

1. **Web-font branding.** Two families (`Planetaire Mono` full/Nerd +
   `Planetaire Mono Text` icon-free), or one family with a separate icon-free
   distribution?
2. **Web-font glyph scope.** Strictly the authored letterform ranges (Latin/Greek/
   Cyrillic + punctuation/symbols), or also keep box-drawing/Powerline for terminal web
   use?
3. **Site hosting.** GitHub Pages from this repo (`/docs` or `gh-pages`) acceptable, or
   a separate repo/domain?
4. **Demo format.** Preferred terminal-demo medium — static SVG, animated GIF/SVG, or
   MP4 (VHS) — for the README and site?

* * *

*This review is a living document; update the health snapshot and backlog table as beads
are completed.*
