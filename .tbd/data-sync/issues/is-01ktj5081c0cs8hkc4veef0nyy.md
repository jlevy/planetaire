---
type: is
id: is-01ktj5081c0cs8hkc4veef0nyy
title: "Full-fidelity SemiBold: embolden the ~49 ultra-dense logo glyphs to 600"
kind: task
status: open
priority: 1
version: 3
labels: []
dependencies:
  - type: blocks
    target: is-01ktnk4xc3dg0mac0vtkp339n8
parent_id: is-01kthj4yda44ebzchx923mdh31
created_at: 2026-06-07T22:59:35.084Z
updated_at: 2026-06-09T07:05:47.184Z
---
The shipped SemiBold masters use a point-count cap (max_points=500 in the recipe): ~49 ultra-dense Nerd Font logo glyphs (e.g. dev-ohmyzsh at 4,676 points) are left at base weight because FontForge changeWeight is pathologically slow on them (a full-font pass ran 2+ hours without finishing). Visually imperceptible (these glyphs appear in no specimen/README page), but for true full fidelity they should eventually be emboldened to 600. Options: parallel-embolden just the capped glyphs across cores then merge into the masters; a faster stroke/overlap method; or interpolating from Medium/Bold. Then drop or raise the cap. Files: src/planetaire/ops/embolden.py, recipes/planetaire_mono.py (_INTERMEDIATE_WEIGHTS max_points).

## Notes

User reconfirmed 2026-06-09 that the 600 weight should ideally be regenerated because the current SemiBold cap left some dense Nerd Font icons at base weight. Treat this as part of the broader generated-master regeneration work under plt-96bv, not just a low-priority visual-fidelity cleanup. Requires FontForge environment/provenance bead plt-5qf1.
