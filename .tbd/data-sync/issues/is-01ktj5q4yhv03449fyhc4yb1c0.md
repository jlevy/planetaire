---
type: is
id: is-01ktj5q4yhv03449fyhc4yb1c0
title: normalize_monospace thins wide italic glyphs (uneven stroke weight)
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01kthj4yda44ebzchx923mdh31
created_at: 2026-06-07T23:12:05.584Z
updated_at: 2026-06-07T23:12:05.584Z
---
normalize_monospace horizontally condenses any glyph whose ink exceeds the cell (1204) so nothing bleeds. But slanted, emboldened italic letters are the widest -- e.g. italic y/x/m at ~1440-1480 units are scaled to ~1180 (~0.81x), thinning their vertical-component strokes ~18% and making them look lighter than narrow glyphs (n/o/l, scaled ~0.98-1.00). Diagnosed via ink-area: changeWeight emboldening is uniform across glyphs (~1.45x); the unevenness is entirely from condensing. Affects ALL italic weights, worse the heavier the weight. Fix options: for letter/text glyphs (not box-drawing/powerline/icons), set the uniform advance and recenter the ink but ALLOW it to overhang the cell (italics naturally overhang) rather than horizontal-scaling; keep strict cell-fitting only for the tiling glyphs. Re-verify the monospace invariant tests, the golden manifest, and box-drawing/powerline alignment. File: src/planetaire/ops/monospace.py.
