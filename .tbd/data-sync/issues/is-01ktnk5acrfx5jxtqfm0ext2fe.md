---
type: is
id: is-01ktnk5acrfx5jxtqfm0ext2fe
title: Specimen and golden QA for regenerated synthetic weights
kind: task
status: open
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01ktnez5fmvrc4ps4v4khqxy88
created_at: 2026-06-09T07:04:44.693Z
updated_at: 2026-06-09T07:59:05.074Z
---
After regenerating the synthetic masters, rebuild Extended and Text, regenerate or verify golden manifests as appropriate, and use the existing PDF/HTML specimen pages to inspect visual differences. Focus review on weights 600 and 800, upright and italic; dense Nerd Font logo glyphs affected by the 600 cap; outline point counts/glyf sizes; monospace bleed warnings; metadata/name-table lineage; and web/font package sizes. Capture before/after artifacts or screenshots sufficient for review before blessing new goldens. If outline cleanup (plt-c8zu) is adopted in the same cycle, include it in this QA pass; otherwise record it as a follow-up.

## Notes

2026-06-09 first comparison artifacts generated in /private/tmp/planetaire-regen-compare.2Flm4g. PDFs: assets-current/planetaire-mono-specimen.pdf and assets-regen/planetaire-mono-specimen.pdf. README-style PNG cards rendered at ppi 150 in assets-current/images and assets-regen/images. HTML specimens generated at current-output/specimen.html and regen-output/specimen.html. ImageMagick AE compare across the 17 PNG cards: 15 were pixel-identical; only weights-dark.png and weights-light.png changed, with AE counts 4556 and 4575 respectively. Highlighted diffs are assets-regen/weights-dark-diff.png and assets-regen/weights-light-diff.png. Initial visual sanity check shows localized changes in generated weight rows, matching the source-master changes. Remaining QA before blessing: inspect full PDF/specimen at release quality, run golden manifest decision, review dense Nerd Font icons if plt-ddjw is completed or explicitly excepted, and compare committed 300 ppi assets before updating docs/images.
