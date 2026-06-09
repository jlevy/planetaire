---
type: is
id: is-01ktnk4xc3dg0mac0vtkp339n8
title: Clean regeneration pass for every generated source master
kind: task
status: open
priority: 1
version: 2
labels: []
dependencies:
  - type: blocks
    target: is-01ktnk5acrfx5jxtqfm0ext2fe
parent_id: is-01ktnez5fmvrc4ps4v4khqxy88
created_at: 2026-06-09T07:04:31.362Z
updated_at: 2026-06-09T07:05:36.562Z
---
Regenerate every source master that is supposed to be produced by the current Planetaire pipeline, not just the known-bad ExtraBold pair. Scope: B612 Medium/SemiBold from Regular/Italic, Hack Medium/SemiBold from Regular/Italic, B612 ExtraBold/ExtraBoldItalic from Bold/BoldItalic, and any downstream Planetaire outputs affected by those sources. Remove or bypass cached generated files so the pipeline actually runs. Address the SemiBold 600 max_points cap / dense Nerd Font logo omission by either completing the capped glyphs (plt-ddjw), replacing the slow path, or explicitly documenting any remaining exception. Update fonts/source/SHA256SUMS and fonts/source/README.md provenance. This is the coordination pass that proves the committed generated masters match today’s pipeline.
