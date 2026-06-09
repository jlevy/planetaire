---
type: is
id: is-01ktnf0g7ahcwvcqtb1zeqyyyb
title: "Web delivery guidance: minimal recipe, preload, metric-matched fallback @font-face"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01ktnez5fmvrc4ps4v4khqxy88
created_at: 2026-06-09T05:52:12.521Z
updated_at: 2026-06-09T05:52:12.521Z
---
Document and ship the delivery-side best practices. (1) Lead with a minimal web recipe — Regular + one bold (ExtraBold reads best for display), ~27 KB Latin — as the documented default instead of the 10-weight family (~649 KB). (2) Generate a fallback @font-face with size-adjust/ascent-override/descent-override/line-gap-override tuned to ui-monospace so CLS during swap collapses to ~0. (3) preload guidance for above-the-fold weight(s) and a CDN immutable long-cache note. Ref 6.3-6.5. Files: README.md, recipes/site.py, generated @font-face CSS.
