---
type: is
id: is-01ktj5081c0cs8hkc4veef0nyy
title: "Full-fidelity SemiBold: embolden the ~49 ultra-dense logo glyphs to 600"
kind: task
status: open
priority: 1
version: 7
labels: []
dependencies:
  - type: blocks
    target: is-01ktnk4xc3dg0mac0vtkp339n8
parent_id: is-01kthj4yda44ebzchx923mdh31
created_at: 2026-06-07T22:59:35.084Z
updated_at: 2026-06-09T15:49:10.208Z
---
The shipped SemiBold masters use a point-count cap (max_points=500 in the recipe): ~49 ultra-dense Nerd Font logo glyphs (e.g. dev-ohmyzsh at 4,676 points) are left at base weight because FontForge changeWeight is pathologically slow on them (a full-font pass ran 2+ hours without finishing). Visually imperceptible (these glyphs appear in no specimen/README page), but for true full fidelity they should eventually be emboldened to 600. Options: parallel-embolden just the capped glyphs across cores then merge into the masters; a faster stroke/overlap method; or interpolating from Medium/Bold. Then drop or raise the cap. Files: src/planetaire/ops/embolden.py, recipes/planetaire_mono.py (_INTERMEDIATE_WEIGHTS max_points).

## Notes

2026-06-09 follow-up prototype results: (1) single-glyph FontForge changeWeight on dev-ohmyzsh from Hack Regular with amount=75 was still running after ~60s and was killed; (2) FontForge glyph.stroke('circular', 75, ...) on the same glyph entered the same internal overlap/mismatched-intersection failure mode and was killed; (3) Hack Regular->Bold interpolation is not useful because all 49 dense glyph outlines are byte/coordinate-identical between Regular and Bold, upright and italic; (4) Hack Regular->ExtraBold has changed outlines for 47/49 dense glyphs but contour/end-point/flag structures are incompatible, so direct interpolation is unsafe. Conclusion: keep the documented 500-point cap for the current reproducible baseline. Full fidelity needs a separate research implementation, likely external robust path offset/boolean tooling or manually curated icon outlines, not FontForge changeWeight/stroke.
