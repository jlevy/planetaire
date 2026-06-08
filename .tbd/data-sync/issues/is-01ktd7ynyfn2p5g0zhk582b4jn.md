---
type: is
id: is-01ktd7ynyfn2p5g0zhk582b4jn
title: "README: pair every font image as dark-then-light"
kind: task
status: closed
priority: 2
version: 3
labels:
  - readme
dependencies: []
created_at: 2026-06-06T01:14:57.359Z
updated_at: 2026-06-06T01:20:55.688Z
closed_at: 2026-06-06T01:20:55.688Z
close_reason: Replaced 4 auto-switching <picture> blocks with explicit dark-then-light <img> pairs
---
On the README home page, present each font specimen image as the dark version immediately followed by its corresponding light version (every font image should be paired dark-then-light). Cleaner and clearer than the current single picture/source dark-OR-light swap. Affects README.md image blocks and possibly the image-generation recipes so both variants are emitted and referenced.
