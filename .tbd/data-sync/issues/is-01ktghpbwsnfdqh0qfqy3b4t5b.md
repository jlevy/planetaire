---
type: is
id: is-01ktghpbwsnfdqh0qfqy3b4t5b
title: Build WOFF2/WOFF + CSS for the Extended family (make it a true superset)
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01ktghbdpt1ya92g1kb7xpmpmc
created_at: 2026-06-07T08:02:53.976Z
updated_at: 2026-06-07T08:35:15.402Z
closed_at: 2026-06-07T08:35:15.393Z
close_reason: "build_planetaire_mono emits WOFF2 + planetaire-mono-extended.css from the full glyph set; _write_font_face_css parameterized by family. WOFF2-only. Tests updated. PR #7."
---
Extend build_planetaire_mono to also emit woff2/woff (full font, no subset) + planetaire-mono-extended.css, mirroring build_text. Parameterize _write_font_face_css with the family name. So Extended ships TTF + WOFF2 + WOFF + CSS (superset of Text in both glyphs and formats). Add/adjust tests.
