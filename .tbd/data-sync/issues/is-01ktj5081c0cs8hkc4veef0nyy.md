---
type: is
id: is-01ktj5081c0cs8hkc4veef0nyy
title: "Full-fidelity SemiBold: embolden the ~49 ultra-dense logo glyphs to 600"
kind: task
status: open
priority: 1
version: 4
labels: []
dependencies:
  - type: blocks
    target: is-01ktnk4xc3dg0mac0vtkp339n8
parent_id: is-01kthj4yda44ebzchx923mdh31
created_at: 2026-06-07T22:59:35.084Z
updated_at: 2026-06-09T07:59:30.347Z
---
The shipped SemiBold masters use a point-count cap (max_points=500 in the recipe): ~49 ultra-dense Nerd Font logo glyphs (e.g. dev-ohmyzsh at 4,676 points) are left at base weight because FontForge changeWeight is pathologically slow on them (a full-font pass ran 2+ hours without finishing). Visually imperceptible (these glyphs appear in no specimen/README page), but for true full fidelity they should eventually be emboldened to 600. Options: parallel-embolden just the capped glyphs across cores then merge into the masters; a faster stroke/overlap method; or interpolating from Medium/Bold. Then drop or raise the cap. Files: src/planetaire/ops/embolden.py, recipes/planetaire_mono.py (_INTERMEDIATE_WEIGHTS max_points).

## Notes

2026-06-09 status after temp clean regen: applying the 500-point cap to Hack Medium as well as SemiBold (plt-hhpi) makes full temp regeneration complete, but the same 49 dense Nerd Font logo glyphs above the cap still keep source-weight outlines. The densest examples in Hack Regular are dev-ohmyzsh 4676 points, dev-composer 2583, linux-openbsd 2257, dev-postcss 2015, and dev-renpy 1788. This bead remains the full-fidelity path if we want 500/600 Hack generated masters to embolden those dense icons rather than document the cap as an intentional exception.
