---
type: is
id: is-01ktnf0gvq8msx5q9jvacspgq5
title: Outline cleanup on emboldened weights (removeOverlap/simplify); SemiBold 600 quality
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01ktnez5fmvrc4ps4v4khqxy88
created_at: 2026-06-09T05:52:13.175Z
updated_at: 2026-06-09T05:52:13.175Z
---
The FontForge-emboldened weights carry ~25% more contour points (~32-33 vs ~26 for native Regular/Bold). SemiBold 600 is the heaviest and most distorted: it uses the largest single changeWeight step (change_amount=75 from Regular, vs Medium 40 and ExtraBold 30) with no follow-up cleanup. A removeOverlap + simplify pass after emboldening could shave glyf size and clean letter outlines. NOTE: SemiBold is generated from Regular (400), NOT from Medium (500) — no compounding; the "500" in the recipe tuple is max_points, not a source. Touches outlines -> visual + golden regression check before adopting. Ref 6.6. Related: plt-ddjw (ultra-dense logo glyphs left at the cap).
