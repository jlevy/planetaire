---
type: is
id: is-01m1zw65nbz8yhdr5fbw7r74w6
title: "PR #26 review P26-R4: font_ink_extent mutates the font it measures"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m1zw5fshk142fvk4g9wc52k9
created_at: 2026-09-08T06:44:46.891Z
updated_at: 2026-09-08T07:22:54.854Z
closed_at: 2026-09-08T07:22:54.854Z
close_reason: null
resolution: null
duplicate_of: null
---
merge.py:219-225 glyph.recalcBounds called from read-only validate.py:183. Use ControlBoundsPen over getGlyphSet().
