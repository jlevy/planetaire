---
type: is
id: is-01ktnf0fx6qm76y7k418bwp574
title: "Build trims: drop post glyph names + trim name table"
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01ktnez5fmvrc4ps4v4khqxy88
created_at: 2026-06-09T05:52:12.198Z
updated_at: 2026-06-09T06:51:45.644Z
closed_at: 2026-06-09T06:51:45.643Z
close_reason: subset_font now emits web-optimized subsets with post format 3.0/no glyph names and trims name records to essential English identity/license records.
---
ops/subset.py keeps glyph names (post, options.glyph_names=True) and the full all-language name table (name_IDs/name_languages=["*"]); a browser uses neither. Emit post format 3.0 and trim name to the few needed English IDs. ~3 KB (~6%) off every WOFF2 with identical rendering (~30 KB across the 10-weight family). Low risk; do it in the build. Ref docs/web-font-research.md 6.1.
