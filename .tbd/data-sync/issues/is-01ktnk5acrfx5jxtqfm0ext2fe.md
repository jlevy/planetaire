---
type: is
id: is-01ktnk5acrfx5jxtqfm0ext2fe
title: Specimen and golden QA for regenerated synthetic weights
kind: task
status: closed
priority: 1
version: 4
labels: []
dependencies: []
parent_id: is-01ktnez5fmvrc4ps4v4khqxy88
created_at: 2026-06-09T07:04:44.693Z
updated_at: 2026-06-09T15:32:34.888Z
closed_at: 2026-06-09T15:32:34.887Z
close_reason: "Specimen/golden QA completed: old/new PDF rendered and compared, changed pages reviewed, no visual regressions found, golden regenerated and verified."
---
After regenerating the synthetic masters, rebuild Extended and Text, regenerate or verify golden manifests as appropriate, and use the existing PDF/HTML specimen pages to inspect visual differences. Focus review on weights 600 and 800, upright and italic; dense Nerd Font logo glyphs affected by the 600 cap; outline point counts/glyf sizes; monospace bleed warnings; metadata/name-table lineage; and web/font package sizes. Capture before/after artifacts or screenshots sufficient for review before blessing new goldens. If outline cleanup (plt-c8zu) is adopted in the same cycle, include it in this QA pass; otherwise record it as a follow-up.

## Notes

2026-06-09 completed committed visual/golden QA. Old specimen baseline copied to /private/tmp/planetaire-final-compare.5kvRGG/before/planetaire-mono-specimen.pdf; regenerated specimen copied to /private/tmp/planetaire-final-compare.5kvRGG/after/planetaire-mono-specimen.pdf. Both PDFs are 22 pages, A4, Typst 0.14.2. Rendered with pdftoppm at 144 dpi and compared with ImageMagick AE. Changed pages: 1 (138 pixels, build date 2026-06-08 -> 2026-06-09), 13 (1674 pixels, weight specimen generated-master outline differences only), 19 (115453 pixels, expected prose refresh for slim Regular/Bold Latin-range web CSS; layout reviewed OK), 21 (399 pixels, tiny generated-weight glyph differences on width/alignment page). The other 18 pages are pixel-identical. README image regeneration changed only weights-dark.png and weights-light.png; all other generated PNG cards were byte-identical. Visual verdict: no regressions found; generated-weight differences are localized, expected, and preserve width/layout. Golden manifest regenerated and regression verify passes with 119646 identical glyph records.
