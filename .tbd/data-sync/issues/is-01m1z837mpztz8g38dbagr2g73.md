---
type: is
id: is-01m1z837mpztz8g38dbagr2g73
title: OS/2 vertical metrics report Hack's values, not the merged B612 outlines
kind: bug
status: closed
priority: 1
version: 5
labels: []
dependencies: []
created_at: 2026-09-08T00:53:39.093Z
updated_at: 2026-09-08T08:07:46.498Z
closed_at: 2026-09-08T08:07:46.498Z
close_reason: OS/2 metrics fix shipped in v0.2.0 (release commit 28589de, tag v0.2.0). Corrected metrics verified in the release archives, the tagged fonts/web, and on the jsDelivr CDN; the site is live on the @v0.2.0 pin. The separate release-commit CI gate failure is tracked as follow-up work, not this bug.
resolution: null
duplicate_of: null
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

## Notes

Fixed on fix/os2-vertical-metrics; PR https://github.com/jlevy/planetaire/pull/26, merged as 2e6702e (CI green: build 3.12/3.13/3.14 + fonts). derive_os2_metrics measures sxHeight, sCapHeight, xAvgCharWidth and the usWin box off the merged outlines; validate check guards it; all 10 shipped weights rebuilt and exact.

Released as v0.2.0 on 2026-09-08.

- Release commit 28589deb5e7df5c5f77ed23d83b784a85ef8484b, annotated tag v0.2.0 (tag object 17fdc53c1986571175931c8efa732e99499d8f81).
- Cut with the documented flow: make release VERSION=0.2.0 -> review -> make release-finalize VERSION=0.2.0 -> git push origin main -> git push origin v0.2.0.
- GitHub release https://github.com/jlevy/planetaire/releases/tag/v0.2.0, all five assets attached, body from docs/release/notes/v0.2.0.md, releases/latest resolves to v0.2.0.
- Corrected metrics verified in the release archive TTFs and in the tagged fonts/web: sxHeight 1120-1130, sCapHeight 1520-1525, xAvgCharWidth 1204, family-wide usWinAscent/usWinDescent 1977/806 identical on all ten faces.
- jsDelivr serves @v0.2.0 (CSS, WOFF2, specimen PDF all HTTP 200, x-jsd-version 0.2.0); ojoshe.com/planetaire/ redeployed and now loads the @v0.2.0 pin on all three pages.

Follow-up, not part of this bug: main CI is red on the new 'Check committed fonts/web matches a rebuild' gate added in b51dba6. The committed CDN fonts are stamped with the previous tag because release.py builds them before the tag exists, so a rebuild at the tagged commit disagrees. Verified to be the version stamp only - every OS/2 metric, bbox and advance is identical. Structural; will recur on every release until release.py passes an explicit version to the font build the way it already does for the specimen.
