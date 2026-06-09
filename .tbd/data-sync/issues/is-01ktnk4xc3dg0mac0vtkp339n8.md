---
type: is
id: is-01ktnk4xc3dg0mac0vtkp339n8
title: Clean regeneration pass for every generated source master
kind: task
status: closed
priority: 1
version: 5
labels: []
dependencies:
  - type: blocks
    target: is-01ktnk5acrfx5jxtqfm0ext2fe
parent_id: is-01ktnez5fmvrc4ps4v4khqxy88
created_at: 2026-06-09T07:04:31.362Z
updated_at: 2026-06-09T15:31:43.655Z
closed_at: 2026-06-09T15:31:43.654Z
close_reason: "Clean generated-master regeneration pass is committed locally: source masters, checksums, provenance docs, outputs, specimen, image cards, and golden manifest were rebuilt and validated. Dense-logo full fidelity remains as plt-ddjw."
---
Regenerate every source master that is supposed to be produced by the current Planetaire pipeline, not just the known-bad ExtraBold pair. Scope: B612 Medium/SemiBold from Regular/Italic, Hack Medium/SemiBold from Regular/Italic, B612 ExtraBold/ExtraBoldItalic from Bold/BoldItalic, and any downstream Planetaire outputs affected by those sources. Remove or bypass cached generated files so the pipeline actually runs. Address the SemiBold 600 max_points cap / dense Nerd Font logo omission by either completing the capped glyphs (plt-ddjw), replacing the slow path, or explicitly documenting any remaining exception. Update fonts/source/SHA256SUMS and fonts/source/README.md provenance. This is the coordination pass that proves the committed generated masters match today’s pipeline.

## Notes

2026-06-09 completed committed regeneration pass. Copied regenerated source masters into fonts/source for B612 Medium/SemiBold/ExtraBold and Hack Medium/SemiBold, upright and italic; updated fonts/source/SHA256SUMS; updated fonts/source/README.md and src/planetaire/recipes/sources.py provenance text. Rebuilt fonts/output Extended and Text, split web fonts, HTML specimen, PDF specimen, README images, and golden manifest. The deliberate exception is the existing dense Nerd Font logo cap: 49 ultra-dense Hack glyphs above 500 points keep source outlines; that full-fidelity work remains tracked in plt-ddjw rather than blocking this reproducible baseline. Validation: build download verified 20 source fonts; validate fonts/output/*.ttf produced only known bleed warnings; regression verify passes after golden regeneration; ruff, basedpyright, pytest all passed.
