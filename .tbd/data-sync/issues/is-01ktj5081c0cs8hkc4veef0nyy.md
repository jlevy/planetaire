---
type: is
id: is-01ktj5081c0cs8hkc4veef0nyy
title: "Full-fidelity SemiBold: embolden the ~49 ultra-dense logo glyphs to 600"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01kthj4yda44ebzchx923mdh31
created_at: 2026-06-07T22:59:35.084Z
updated_at: 2026-06-07T22:59:35.084Z
---
The shipped SemiBold masters use a point-count cap (max_points=500 in the recipe): ~49 ultra-dense Nerd Font logo glyphs (e.g. dev-ohmyzsh at 4,676 points) are left at base weight because FontForge changeWeight is pathologically slow on them (a full-font pass ran 2+ hours without finishing). Visually imperceptible (these glyphs appear in no specimen/README page), but for true full fidelity they should eventually be emboldened to 600. Options: parallel-embolden just the capped glyphs across cores then merge into the masters; a faster stroke/overlap method; or interpolating from Medium/Bold. Then drop or raise the cap. Files: src/planetaire/ops/embolden.py, recipes/planetaire_mono.py (_INTERMEDIATE_WEIGHTS max_points).
