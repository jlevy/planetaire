---
type: is
id: is-01ktaz83rn232714xfbb2kcqrj
title: Extend validate with style-linking assertions
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-06-05-finalize-and-publish.md
labels: []
dependencies: []
parent_id: is-01ktaz70qyd5ap0c99chx6vfxq
created_at: 2026-06-05T04:04:20.372Z
updated_at: 2026-06-05T05:55:37.262Z
closed_at: 2026-06-05T05:55:37.261Z
close_reason: validate_font now checks italic/bold style-linking across macStyle/fsSelection/subfamily + REGULAR-bit warning
---
rename_font sets usWeightClass but relies on source files carrying correct italic/bold bits. Add assertions to ops/validate.py: italic bit in fsSelection/head.macStyle set iff subfamily is Italic, and weight class matches expected, so a future source swap can't silently break style linking. See docs/engineering-review.md §3.5.
