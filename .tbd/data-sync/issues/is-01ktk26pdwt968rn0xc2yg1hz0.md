---
type: is
id: is-01ktk26pdwt968rn0xc2yg1hz0
title: "Spacing Review: add the standard-coding-characters true-cell-width grid for italics"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01kthj4yda44ebzchx923mdh31
created_at: 2026-06-08T07:29:55.132Z
updated_at: 2026-06-08T07:29:55.132Z
---
On the 'Spacing Review' page (docs/specimen/planetaire-mono-specimen.typ:739), coding-width-grid (content.typ:304) shows the standard coding characters (A-Z, a-z, 0-9, punctuation, and cell-filling box/powerline glyphs) at their true cell widths with red advance rules -- but only UPRIGHT. Add the same review for ITALICS so italic glyphs' cell widths and overhang are visible against the rules.

IMPLEMENTATION: parameterize coding-width-grid with a style/italic flag (qa-cell renders italic), or add a parallel italic grid, and place it on the Spacing Review page after the upright grid. weight-alignment (content.typ:331) already has an 'it: false' param as precedent. This QA view directly supports verifying the wide-italic condensing/cell-fit work in plt-3h7p.
