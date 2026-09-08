---
type: is
id: is-01m1zw64qn32p8a1437f9mykhx
title: "PR #26 review P26-R1: usWin box differs per face and per subset"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m1zw5fshk142fvk4g9wc52k9
created_at: 2026-09-08T06:44:45.941Z
updated_at: 2026-09-08T07:22:54.830Z
closed_at: 2026-09-08T07:22:54.816Z
close_reason: null
resolution: null
duplicate_of: null
---
merge.py:281-287, planetaire_mono.py:393,413. Derive one family-wide win box (max yMax / -yMin across the family's faces) and stamp every face and subset; drop or make non-shrinking the post-subset re-derive.
