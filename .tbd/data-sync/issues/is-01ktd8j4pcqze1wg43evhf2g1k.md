---
type: is
id: is-01ktd8j4pcqze1wg43evhf2g1k
title: Medium & ExtraBold weights are not truly monospaced (variable advance widths)
kind: bug
status: open
priority: 1
version: 2
labels:
  - fonts
dependencies:
  - type: blocks
    target: is-01ktd7z0kctd0hb3kqjvydthqg
created_at: 2026-06-06T01:25:35.051Z
updated_at: 2026-06-06T01:25:35.671Z
---
Discovered while investigating the weights image (plt-2txj). The B612 Mono SOURCE masters used for the Medium (500) and ExtraBold (800) weights have NON-uniform per-glyph advance widths, e.g. (upm=2000): ExtraBold A=1360 i=1360 m=1390 0=1360 but period=1300; Medium A=1380 m=1420 period=1300. Regular/Italic/Bold/BoldItalic are a clean uniform 1300. Because ops/merge.py copies the donor hmtx verbatim, Planetaire Mono's Medium and ExtraBold inherit the defect and are not true monospace. This is the real cause of (a) the weights image showing different widths per weight and (b) the period appearing narrower than letters in heavier-weight text (e.g. the .rw vs drw listing rows). FIX: add a pipeline normalization step that forces every glyph in every weight to a single uniform advance width (the monospace cell), adjusting LSB to recenter, so all weights are exactly monospaced. Pure fontTools (no fontforge). Requires rebuilding fonts + regression review + re-rendering specimen/images. NOTE: this changes font OUTPUT metrics — confirm approach with maintainer before shipping.
