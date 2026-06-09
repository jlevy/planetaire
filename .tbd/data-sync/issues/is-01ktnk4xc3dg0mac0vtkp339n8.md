---
type: is
id: is-01ktnk4xc3dg0mac0vtkp339n8
title: Clean regeneration pass for every generated source master
kind: task
status: in_progress
priority: 1
version: 3
labels: []
dependencies:
  - type: blocks
    target: is-01ktnk5acrfx5jxtqfm0ext2fe
parent_id: is-01ktnez5fmvrc4ps4v4khqxy88
created_at: 2026-06-09T07:04:31.362Z
updated_at: 2026-06-09T07:58:50.914Z
---
Regenerate every source master that is supposed to be produced by the current Planetaire pipeline, not just the known-bad ExtraBold pair. Scope: B612 Medium/SemiBold from Regular/Italic, Hack Medium/SemiBold from Regular/Italic, B612 ExtraBold/ExtraBoldItalic from Bold/BoldItalic, and any downstream Planetaire outputs affected by those sources. Remove or bypass cached generated files so the pipeline actually runs. Address the SemiBold 600 max_points cap / dense Nerd Font logo omission by either completing the capped glyphs (plt-ddjw), replacing the slow path, or explicitly documenting any remaining exception. Update fonts/source/SHA256SUMS and fonts/source/README.md provenance. This is the coordination pass that proves the committed generated masters match today’s pipeline.

## Notes

2026-06-09 progress: completed a temp clean-regeneration comparison rooted at /private/tmp/planetaire-regen-compare.2Flm4g after fixing plt-hhpi. Baseline current artifacts are in current-output. Regenerated source copy is in regen-source, with regenerated artifacts in regen-output. Commands completed for regenerated source: build planetaire-mono; build text --formats ttf; build text --split --italics; build specimen for current and regen; build images for current and regen at ppi 150; build html-specimen for current and regen. Source-master hash comparison: upstream native masters stayed identical; generated B612 Medium/SemiBold, Hack Medium/SemiBold, and B612 ExtraBold changed. B612 ExtraBold shrank from committed 2,025,528 bytes to regenerated 97,776 bytes, with clean Airbus unique ID Airbus: B612 Mono Bold: Version1.008 and OS/2 weight 800. This confirms the old 800 lineage drift. Not yet done: copy regenerated source masters into fonts/source, update SHA256SUMS and fonts/source/README.md provenance, decide whether to accept the bounded Hack dense-glyph exception or complete plt-ddjw first, then regenerate committed docs/assets at release quality.
