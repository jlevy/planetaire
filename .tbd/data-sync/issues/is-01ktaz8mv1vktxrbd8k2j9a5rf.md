---
type: is
id: is-01ktaz8mv1vktxrbd8k2j9a5rf
title: Generate a clean static HTML specimen
kind: feature
status: closed
priority: 2
version: 6
spec_path: docs/project/specs/active/plan-2026-06-05-finalize-and-publish.md
labels: []
dependencies:
  - type: blocks
    target: is-01ktaz8ncx3mp3dtk1g00xjy01
parent_id: is-01ktaz70qyd5ap0c99chx6vfxq
created_at: 2026-06-05T04:04:37.856Z
updated_at: 2026-06-05T06:21:48.570Z
closed_at: 2026-06-05T06:21:48.570Z
close_reason: generate_html_specimen() + CLI/Makefile; self-contained dark-theme specimen using Text woff2 with ss01 toggle
---
A self-contained specimen.html that loads the web font via @font-face and reproduces the specimen in-browser: weight ladder, legibility pairs, character set, live ss01 toggle, code sample. Generated from a template (not hand-maintained) so it stays in sync. Anchors the static site. Depends on the web/text font build. See docs/engineering-review.md §6.3.
