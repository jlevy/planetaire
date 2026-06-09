---
type: is
id: is-01ktnk5acrfx5jxtqfm0ext2fe
title: Specimen and golden QA for regenerated synthetic weights
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01ktnez5fmvrc4ps4v4khqxy88
created_at: 2026-06-09T07:04:44.693Z
updated_at: 2026-06-09T07:04:44.693Z
---
After regenerating the synthetic masters, rebuild Extended and Text, regenerate or verify golden manifests as appropriate, and use the existing PDF/HTML specimen pages to inspect visual differences. Focus review on weights 600 and 800, upright and italic; dense Nerd Font logo glyphs affected by the 600 cap; outline point counts/glyf sizes; monospace bleed warnings; metadata/name-table lineage; and web/font package sizes. Capture before/after artifacts or screenshots sufficient for review before blessing new goldens. If outline cleanup (plt-c8zu) is adopted in the same cycle, include it in this QA pass; otherwise record it as a follow-up.
