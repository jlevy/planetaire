# Planetaire Mono as a Web Font: Size Review and Best Practices

**Date:** 2026-06-09 **Author:** Web-font research pass (Claude Code) **Scope:** The
`Planetaire Mono Text` web build (WOFF2 + generated `@font-face` CSS): measured sizes,
how it compares to other monospace web fonts, and the best practices worth adopting to
keep it light enough for marketing sites and CDNs without losing quality.

All Planetaire / B612 / Hack numbers below are **measured first-hand** in this repo with
fontTools (subset + WOFF2/brotli), so they are reproducible.
Third-party font sizes are *characterized* rather than measured: this sandbox blocks
outbound downloads, so exact bytes for JetBrains Mono et al.
must be confirmed with the tools listed in
[§7](#7-reproducing-and-verifying-the-numbers).
The methodology is identical, so the relative picture holds.

* * *

## 1. TL;DR

- **Planetaire Mono Text is already a sensible web font.** It ships WOFF2 with
  `font-display: swap`, hinting stripped, and the 10k Nerd Font icons removed — the
  right baseline.
- **The shipped Text WOFF2 weights are 53–77 KB each (avg ~65 KB).** That is *not* heavy
  per glyph; it is heavy only because each file bundles **~1,300 glyphs** (full Latin +
  Greek + Cyrillic + symbols) that a typical marketing site never renders.
- **Per-glyph, Planetaire is competitive with its parents:** ~39 bytes/glyph vs Hack’s
  ~35 and B612’s ~48 (full Text range).
  Its **Latin-only core is ~12 KB**, right in the band of mainstream mono web fonts.
- **The single biggest win is a `unicode-range` split** (latin / latin-ext / greek /
  cyrillic). A Latin-dominant page would then pull **~12 KB**, not 53 KB, per weight, and
  fetch Greek/Cyrillic only if used.
- **Two free quick wins** the build doesn’t take yet: drop `post` glyph names (about 2.2
  KB/weight) and trim the `name` table (about 0.9 KB/weight) — together ~6% off every
  file with zero visual change.
- **For marketing sites the dominant lever is loading fewer weights.** Regular +
  ExtraBold, Latin-only, is **~27 KB total**; the full 10-weight family is ~649 KB. Make
  the “load two weights” path the documented default.
- **Generated weights cost extra bytes.** The FontForge-emboldened Medium/SemiBold/
  ExtraBold carry ~25% more contour points per glyph (32–33 vs ~26) than the native
  Regular/Bold, so they are the largest files.
  An outline-simplify pass could recover some of that.
- **Doc drift:** the repo quotes “~55 KB/wt” in three places and “~65 KB” in two; the
  measured family average is ~65 KB and the range is 53–77 KB. Worth reconciling to the
  measured numbers.

* * *

## 2. Measured sizes (shipped `Planetaire Mono Text`)

Built with `planetaire build text` (subset to text ranges, hinting dropped) and measured
as written:

| Weight | WOFF2 | TTF |  | Weight | WOFF2 | TTF |
| --- | ---: | ---: | --- | --- | ---: | ---: |
| Regular (400) | **52.7 KB** | 137 KB |  | Italic (400) | 59.3 KB | 150 KB |
| Medium (500) | 64.6 KB | 162 KB |  | Medium Italic | 74.6 KB | 180 KB |
| SemiBold (600) | 66.8 KB | 165 KB |  | SemiBold Italic | **77.4 KB** | 184 KB |
| Bold (700) | 54.5 KB | 143 KB |  | Bold Italic | 59.2 KB | 149 KB |
| ExtraBold (800) | 65.6 KB | 167 KB |  | ExtraBold Italic | 73.8 KB | 178 KB |

**Family total (all 10 WOFF2): ~649 KB.** Average 65 KB; min 52.7 (Regular), max 77.4
(SemiBold Italic).

Two patterns matter for the web:

1. **Italics run ~10–15% larger** than their upright partners (oblique outlines compress
   slightly worse).
2. **The FontForge-emboldened weights (Medium 500, SemiBold 600, ExtraBold 800) are the
   heavy ones** — heavier than the native Bold (700). `changeWeight` adds contour points
   and its overlap removal complicates outlines: ~32–33 points/glyph for the generated
   weights vs ~26 for native Regular/Bold.
   That ~25% point bloat is why SemiBold (165 KB TTF) outweighs Bold (143 KB).

* * *

## 3. Where the bytes go

`Planetaire Mono Text Regular` — 1,317 glyphs, 137 KB TTF:

| Table | Size | Notes |
| --- | ---: | --- |
| `glyf` | 115 KB | Outlines — the irreducible core. |
| `post` | 11.8 KB | **Glyph names. Not needed on the web.** Currently kept. |
| `name` | 3.1 KB | Full name table, all languages. Trimmable for the web. |
| `hmtx` | 3.0 KB | Advance widths (uniform for monospace, compresses well). |
| `loca` | 2.6 KB | Glyph offsets. |
| `cmap` | 0.9 KB | Character map. |
| `GSUB`/`OS/2`/… | <0.3 KB | Features (incl. `ss01`/`zero`), metrics. |

The build already does the big thing right — **hinting is stripped**
(`drop_hinting=True` in `ops/subset.py`), so there is no `prep`/`fpgm`/`cvt`, only a
small `gasp`. The two remaining non-outline costs (`post`, `name`) are pure web
overhead; see [§6](#6-best-practices-to-adopt).

* * *

## 4. How it compares

### 4.1 First-party comparison (measured here, identical options)

Same subsetter, same ranges, hinting + glyph names dropped, WOFF2/brotli, Regular
weight:

| Font | Full Text range | Latin-core only |
| --- | --- | --- |
| **B612 Mono** (parent letterforms) | 468 glyphs · 21.9 KB · 48 B/glyph | 219 glyphs · 11.2 KB |
| **Hack** (parent base/metrics) | 1,323 glyphs · 45.3 KB · **35 B/glyph** | 281 glyphs · 12.6 KB |
| **Planetaire Mono Text** | 1,317 glyphs · 49.7 KB · 39 B/glyph | 252 glyphs · **11.9 KB** |

(The 49.7 KB here vs 52.7 KB shipped is exactly the two web optimizations of
[§6.1](#61-quick-wins-free-bytes) — dropping `post` names and trimming `name`.)

Reading this:

- **B612 looks small only because it covers far less** (468 vs 1,317 glyphs — original
  B612 lacks much of Latin-Extended/Greek-Extended).
  Per glyph it is the *heaviest* of the three (48 B/glyph): its humanist curves and
  light-trap notches carry more nodes.
- **Hack is the lean benchmark** at 35 B/glyph (machine-drawn, low-contrast outlines).
- **Planetaire sits between them (39 B/glyph)** — it pairs B612’s richer letterforms
  with Hack’s coverage, so it is ~10% heavier than pure Hack and noticeably lighter than
  pure B612 per glyph.
  That is the expected, defensible cost of the hybrid.
- **At Latin-core the three are within ~1.5 KB of each other (~11–13 KB).** Planetaire’s
  Latin core is essentially free of any hybrid penalty.

### 4.2 The broader field

Direct downloads are blocked in this sandbox, so treat these as the well-established
*shape* of the landscape, to be confirmed via
[§7](#7-reproducing-and-verifying-the-numbers):

- Mainstream mono web fonts on Google Fonts / Fontsource are served **split by
  `unicode-range`**, so the file a Latin page actually pulls is a **single-weight,
  Latin- only subset of ~95–280 glyphs**, which generally lands in the **~10–30 KB
  WOFF2** band (Roboto Mono and Fira Mono toward the low end; JetBrains Mono toward the
  high end because of its large character set and code ligatures).
- **Planetaire’s Latin core (~12 KB) is squarely in that band** — competitive, not
  heavy. The 53 KB headline number is an apples-to-oranges artifact of shipping
  Latin+Greek+Cyrillic **in one file** instead of three range-split files.

The takeaway is methodological: **Planetaire is not byte-inefficient; it is
coverage-rich and un-split.** Closing the gap is a packaging change
([§6.2](#62-the-big-win-unicode-range-splitting)), not a redraw.

* * *

## 5. The `unicode-range` insight (Latin-core budgets)

Measured Latin-core (Basic Latin + Latin-1 + General Punctuation, ~250 glyphs), names
dropped:

| Weight | Latin-core WOFF2 |
| --- | ---: |
| Regular | 11.9 KB |
| Bold | 12.4 KB |
| Medium | 14.6 KB |
| SemiBold | 15.0 KB |
| ExtraBold | 15.0 KB |
| **Regular + ExtraBold (typical marketing pair)** | **26.9 KB** |
| All 5 upright weights | 68.9 KB |

So a marketing page that uses two weights of Latin text can run on **~27 KB of font**,
versus ~107 KB if it naïvely loads the two full Text files, versus ~649 KB if it loads
the whole family. The font is only “too heavy” if it is delivered without these levers.

* * *

## 6. Best practices to adopt

Ordered by value.
The build already nails the fundamentals — WOFF2, `font-display: swap`,
hinting stripped, a separate icon-free `Text` family, a generated `@font-face`
stylesheet. The items below are what is left.

### 6.1 Quick wins (free bytes)

`ops/subset.py` currently keeps glyph names (`options.glyph_names = True`) and the full,
all-language `name` table (`name_IDs/name_languages = ["*"]`). Neither is used by a
browser.

- **Drop `post` glyph names** (emit `post` format 3.0): −~2.2 KB/weight.
- **Trim the `name` table** to the handful of needed IDs in English: −~0.9 KB/weight.

Together ~3 KB (~6%) off **every** file, identical rendering.
~30 KB across the shipped family.
Low risk; do this in the build, not by hand.

### 6.2 The big win: `unicode-range` splitting

Split each weight into separate WOFF2 files by script — `latin`, `latin-ext`, `greek`,
`cyrillic` — and emit one `@font-face` per range with a matching `unicode-range`
descriptor (the same model Google Fonts uses).
The browser then downloads only the ranges a page actually renders.

- Latin-only page: **~12 KB/weight** instead of ~53 KB.
- Greek/Cyrillic still “just work,” fetched on demand.
- Implementation: a `--split` mode on the Text build that loops the range groups through
  the existing subsetter and writes a multi-block stylesheet.
  The ranges already exist in `config.TEXT_SUBSET_RANGES`; they just need grouping +
  per-group `unicode-range` strings.

This is the change that makes the headline size objection disappear.

### 6.3 Make “two weights” the documented default

The heaviest practical mistake a site can make is loading all ten weights.
The README/site should lead with a **minimal web recipe** — Regular + one bold
(ExtraBold reads best for display) — and present the full family as opt-in.
~27 KB (Latin) vs ~649 KB is the difference between “fine on a CDN” and “a problem.”

### 6.4 `font-display` strategy

`swap` (current) is a safe default but causes a visible swap + layout shift (CLS) when
the web font differs in metrics from the fallback.
Two refinements:

- For a marketing hero where the font *is* the brand, consider `font-display: optional`
  (no swap flash; uses the web font only if it arrives in time, else fallback for that
  load) or `swap` plus a **metric-matched fallback** (below).
- Add a **fallback `@font-face` with metric overrides** — `size-adjust`,
  `ascent-override`, `descent-override`, `line-gap-override` tuned so `ui-monospace`/
  `monospace` occupies the same box as Planetaire.
  This collapses CLS to ~0 during the swap.
  The values are derived from the font’s metrics and can be generated alongside the CSS.

### 6.5 Delivery hygiene (document, don’t just ship files)

- **`preload` the above-the-fold weight(s):**
  `<link rel="preload" as="font" type="font/woff2" crossorigin>` for Regular (and the
  display weight) so they aren’t discovered late in the CSS.
- **Self-host on the CDN with long-lived immutable caching**
  (`Cache-Control: public, max-age=31536000, immutable`); version the filenames.
  WOFF2 is already compressed, so no extra gzip/brotli on the wire is needed.
- **Per-site subsetting for the truly weight-conscious:** point users at `glyphhanger` /
  `subset-font` to cut to the exact glyphs a site uses — a landing page often needs <120
  glyphs, i.e. a few KB/weight.

### 6.6 Trim the heavy generated weights (quality/size tradeoff)

Because the emboldened Medium/SemiBold/ExtraBold carry ~25% more points per glyph
([§2](#2-measured-sizes-shipped-planetaire-mono-text)), a careful `removeOverlap` +
`simplify` pass after emboldening could shave their `glyf` size.
This touches outlines, so it needs a visual/regression check before adoption — flag,
don’t auto-apply.

### 6.7 Variable font (longer term)

A single variable WOFF2 spanning 400–800 would beat ten static files for a site that
wants the whole ramp, and lets the browser interpolate intermediate weights.
It is a real build change (the weight masters are partly FontForge-emboldened, not
interpolation-ready) and is tracked conceptually alongside the OTF item in `TODO.md` —
worth a spike, not urgent.
For the common two-weight marketing case, static + `unicode-range` already wins.

* * *

## 7. Reproducing and verifying the numbers

First-party numbers here come from `planetaire build text` plus a fontTools subset/WOFF2
pass (drop hinting, drop glyph names, brotli).
To fill in exact third-party bytes that this sandbox could not fetch:

- **google-webfonts-helper** (`gwfh.mranftl.com`) — pick a font + subset + weight and
  read the served WOFF2 size.
- **Fontsource** (`fontsource.org`, `@fontsource/*` on npm/jsdelivr) — per-subset,
  per-weight WOFF2 files with listed sizes.
- **glyphhanger** / **fonttools subset** — re-subset any font to the *same* range as a
  Planetaire build and compare like-for-like (the only honest comparison, since coverage
  per file is what dominates).

* * *

## 8. Recommendations (prioritized)

| Priority | Item | Impact | Ref |
| --- | --- | --- | --- |
| P1 | `unicode-range` split (latin / latin-ext / greek / cyrillic) | ~53 KB → ~12 KB per weight for Latin pages | 6.2 |
| P1 | Document a minimal “Regular + one bold” web recipe as the default | 649 KB → ~27 KB typical marketing load | 6.3 |
| P2 | Drop `post` glyph names + trim `name` table in the build | −~3 KB (~6%) every file, no visual change | 6.1 |
| P2 | Reconcile size claims in docs to measured (53–77 KB, avg ~65) | Accuracy | 9 |
| P2 | Ship a metric-override fallback `@font-face` + preload guidance | ~0 CLS, faster first paint | 6.4–6.5 |
| P3 | `removeOverlap`/`simplify` pass on emboldened weights | Trim the 3 heavy weights | 6.6 |
| P3 | Variable-font spike | One file for the full ramp | 6.7 |

* * *

## 9. Note on doc drift

Current size claims disagree and lean low:

- `README.md` (download table): “~65 KB/weight WOFF2”.
- `recipes/site.py`: “~55 KB/wt WOFF2”.
- `docs/fonts-build-and-release.md`: “~55 KB WOFF2/weight”.
- `docs/specimen/...typ`: “about 65 KB per weight”.

Measured: **avg ~65 KB, range 53 KB (Regular) – 77 KB (SemiBold Italic).** The “~55 KB”
figures are anchored to Regular and understate the italics and emboldened weights.
Once the [§6.1](#61-quick-wins-free-bytes) trims land, restate from the rebuilt
artifacts (a “regenerate from the build” note keeps this from drifting again).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
</content> </invoke>
