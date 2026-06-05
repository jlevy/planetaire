---
type: is
id: is-01ktaz8m8cwr6y2gg4bctwy9pz
title: Systematize README home-page specimen image (single render path)
kind: task
status: closed
priority: 2
version: 6
spec_path: docs/project/specs/active/plan-2026-06-05-finalize-and-publish.md
labels: []
dependencies:
  - type: blocks
    target: is-01ktaz8ncx3mp3dtk1g00xjy01
parent_id: is-01ktaz70qyd5ap0c99chx6vfxq
created_at: 2026-06-05T04:04:37.260Z
updated_at: 2026-06-05T08:53:40.742Z
closed_at: 2026-06-05T08:53:40.732Z
close_reason: Hero rendered from docs/specimen/hero.typ via 'build hero' (single Typst render path); committed docs/images/hero.png + regenerated specimen PDF
---
README PNGs are drawn imperatively in scripts/generate_showcase.py (hand-placed x/y, per-token colors, manual hinting strip) -- brittle and a different rendering path from the PDF, so README and specimen can drift. Generate the home-page specimen from the same Typst source (Typst can export high-DPI PNG/SVG) or a small dedicated Typst hero doc, via a make target. One visual language, fully reproducible, >=2x DPI, dark theme, real code + legibility pairs + dotted zero. See docs/engineering-review.md §6.1.

## Notes

BLOCKED on Typst (not installed in this env). Plan: render the README hero/specimen image from the same Typst source as the PDF (typst compile --format png/svg at >=2x) via a 'make hero' target, replacing the PIL script in scripts/generate_showcase.py. The site/HTML specimen generators already exist and can supply layout reference.
