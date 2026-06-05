---
type: is
id: is-01ktb2q48q0c77c5x5hd9v3ehm
title: Investigate ExtraBold ~4.5MB weight; decide icon coverage
kind: task
status: closed
priority: 3
version: 3
spec_path: docs/project/specs/active/plan-2026-06-05-finalize-and-publish.md
labels: []
dependencies: []
parent_id: is-01ktaz70qyd5ap0c99chx6vfxq
created_at: 2026-06-05T05:04:58.134Z
updated_at: 2026-06-05T06:14:33.994Z
closed_at: 2026-06-05T06:14:33.994Z
close_reason: "Investigated: glyf-only bloat from heavier ExtraBold icon outlines; keep full coverage in Extended (Text drops icons). Documented in bead notes."
---
ExtraBold variants are ~4.5MB vs ~2.6MB for the rest, inherited from Hack Nerd Font's heavier ExtraBold icon outlines. Quantify the source of the bloat and decide whether ExtraBold needs full icon coverage in the Extended build (the Text build already drops icons, so this only affects Extended ExtraBold). Document the decision. See engineering-review.md 3.3.

## Notes

FINDING: ExtraBold 4.27MB vs Regular 2.50MB; the entire delta is in 'glyf' (3.94MB vs 2.17MB) at equal glyph count (~12k) — Hack Nerd icon outlines are ~80% larger at weight 800 (heavier strokes). post/loca/hmtx unchanged. DECISION: (1) Text family drops icons, so ExtraBold Text is small (non-issue). (2) Extended keeps full icon coverage — ExtraBold is the recommended terminal-bold weight where icons matter; 4.5MB TTF (~1.x MB woff2) is acceptable for a desktop font. No action; revisit only if a slim 'Extended-no-icons-extrabold' is ever requested.
