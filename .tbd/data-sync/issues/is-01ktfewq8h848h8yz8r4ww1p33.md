---
type: is
id: is-01ktfewq8h848h8yz8r4ww1p33
title: Fix dash/symbol prose in specimen rendered text (content.typ)
kind: task
status: closed
priority: 2
version: 4
labels: []
dependencies:
  - type: blocks
    target: is-01ktfewqm7eqa37m37x0rz8n22
parent_id: is-01ktfevdbrypmftxq65hz54y2y
created_at: 2026-06-06T21:54:42.064Z
updated_at: 2026-06-06T22:13:47.660Z
closed_at: 2026-06-06T22:13:47.660Z
close_reason: Fixed dash/symbol prose in content.typ (em dash->comma, --->colon, =->word); specimen.typ rendered text too. man-page/range/showcase dashes left as authentic content.
---
Apply prose guidelines to RENDERED specimen text (not code comments):
docs/specimen/content.typ:
- L225 'm — clearly distinct' spaced em dash -> comma.
- L274 'STANDARD CODING CHARACTERS -- TRUE CELL WIDTHS' (-- renders en dash) -> colon.
- L278 'ink inside = a clean monospace grid' -> '= ' to 'means'.
- L309 'WEIGHT ALIGNMENT -- EVERY WEIGHT IS THE SAME WIDTH' -> colon.
- L312 'A single vertical line = identical width' -> 'means'.
Also audit docs/specimen/planetaire-mono-specimen.typ and card.typ rendered text for the same (spaced hyphen, --/---, =/+ used as words). Leave // code comments alone.
