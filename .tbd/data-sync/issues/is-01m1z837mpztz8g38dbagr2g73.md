---
type: is
id: is-01m1z837mpztz8g38dbagr2g73
title: OS/2 vertical metrics report Hack's values, not the merged B612 outlines
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-09-08T00:53:39.093Z
updated_at: 2026-09-08T00:53:39.093Z
---
Planetaire Mono draws B612 Mono's letterforms over a Hack Nerd Font base, but
several OS/2 fields survive the merge as Hack's, so consumers size the face as
if it were Hack.

Measured on the shipped `fonts/web/PlanetaireMonoText-*.woff2` (UPM 2000) with
fontTools + BoundsPen:

| field | table | drawn outline |
| --- | ---: | ---: |
| sxHeight | 1094 (0.547 em) | 1120-1130 (top of `x`, ~0.560 em) |
| sCapHeight | 1458/1460 (0.729 em) | 1520-1525 (top of `H`, ~0.760 em) |
| xAvgCharWidth | 1233-1240 | 1204 (the single cell width) |
| usWinAscent | 1901 | head.yMax 1940-1977 (ink clipped on GDI) |
| usWinDescent | 483 | -head.yMin 560-806 (ink clipped on GDI) |

Two distinct causes, both in `merge_glyphs`/`scale_font_upm`
(src/planetaire/ops/merge.py):

1. `scale_font_upm` scales sTypo*, sxHeight, sCapHeight and hhea from Hack's
   2048 UPM to B612's 2000, but xAvgCharWidth, usWinAscent and usWinDescent are
   left as raw 2048-unit numbers in a 2000-unit font.
2. Even correctly scaled, sxHeight/sCapHeight would still describe Hack's
   letterforms, which the merge has replaced with B612's.

Impact: CSS `font-size-adjust`, editors' line boxes, kpress's mono size rule
(which sizes code by x-height beside a prose face), and font-manager previews
all size the face ~2.4% small in x-height and ~4% small in cap height.

Fix: derive these fields from the merged font's own outlines, per the OpenType
spec's definitions, after every outline-modifying step; add a validate check so
it cannot regress.
