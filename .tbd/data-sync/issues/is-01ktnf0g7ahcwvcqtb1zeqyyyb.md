---
type: is
id: is-01ktnf0g7ahcwvcqtb1zeqyyyb
title: "Web delivery guidance: minimal recipe, preload, metric-matched fallback @font-face"
kind: task
status: closed
priority: 2
version: 5
labels: []
dependencies: []
parent_id: is-01ktnez5fmvrc4ps4v4khqxy88
created_at: 2026-06-09T05:52:12.521Z
updated_at: 2026-06-09T16:06:00.849Z
closed_at: 2026-06-09T16:06:00.848Z
close_reason: "Delivered web-font usage guidance: generated stack variable and metric-matched local fallback, README/release preload examples, and production cache notes; validated locally."
---
Document and ship the delivery-side best practices. (1) Lead with a minimal web recipe — Regular + one bold (ExtraBold reads best for display), ~27 KB Latin — as the documented default instead of the 10-weight family (~649 KB). (2) Generate a fallback @font-face with size-adjust/ascent-override/descent-override/line-gap-override tuned to ui-monospace so CLS during swap collapses to ~0. (3) preload guidance for above-the-fold weight(s) and a CDN immutable long-cache note. Ref 6.3-6.5. Files: README.md, recipes/site.py, generated @font-face CSS.

## Notes

Implemented delivery guidance and generated CSS support: split Text CSS now emits a --planetaire-mono-text-font-stack variable plus local metric-matched fallback @font-face, site/specimen CSS consumes the stack variable, README/release notes document Regular Latin preload with optional Bold Latin and italic CSS, and release docs call out immutable WOFF2 caching with shorter CSS caching when URLs are not fingerprinted. Validation: uv run --frozen planetaire build text --split --italics; build html-specimen; build site; focused pytest; ruff; basedpyright; full pytest.
