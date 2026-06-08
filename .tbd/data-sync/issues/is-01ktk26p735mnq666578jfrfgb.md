---
type: is
id: is-01ktk26p735mnq666578jfrfgb
title: "Specimen Two Families page: drop the 'For the web' CSS block; fix @font-face inline size"
kind: task
status: closed
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01kthj4yda44ebzchx923mdh31
created_at: 2026-06-08T07:29:54.914Z
updated_at: 2026-06-08T09:44:34.068Z
closed_at: 2026-06-08T09:44:34.067Z
close_reason: null
---
On the 'Two Families' page (docs/specimen/planetaire-mono-specimen.typ:688), the 'For the web:' block at lines 713-717 (#v(0.2cm) then #text(size: 9pt, fill: #666)[ `<link rel="stylesheet" href="planetaire-mono-text.css">` then `font-family: "Planetaire Mono Text"` ]) is poorly formatted -- inconsistent sizes and ugly wrapping. Drop it entirely.

Also, the inline `@font-face` code in the Text bullet (line 698, '...shipped with a ready @font-face stylesheet.') renders smaller than the surrounding prose; make the inline code match the surrounding text size (a different color is fine). Check the global '#show raw: set text(... size ...)' rule (line 108) against the 10pt prose so inline code matches its surrounding context.

Note: this page's 'Families' wording should likely become 'Packages' -- tracked in plt-072i.
