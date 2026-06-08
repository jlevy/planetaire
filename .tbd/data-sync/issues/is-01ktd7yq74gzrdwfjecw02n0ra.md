---
type: is
id: is-01ktd7yq74gzrdwfjecw02n0ra
title: Clean up key-glyph comparison image layout (labels, headers)
kind: task
status: closed
priority: 2
version: 3
labels:
  - readme
  - specimen
dependencies: []
created_at: 2026-06-06T01:14:58.660Z
updated_at: 2026-06-06T01:23:46.584Z
closed_at: 2026-06-06T01:23:46.584Z
close_reason: "content.typ: fixed-width (4.5cm) glyph column aligns all gray labels; bolded ZERO DOT VARIANTS; added bold KEY GLYPH COMPARISONS top header. Applied matching fixed-width column (7cm) to the PDF specimen's disambig. Image/PDF re-render tracked by plt-5kkw."
---
In the legibility comparison image (I / l / 1 with gray labels, plus a 'ZERO DOT VARIANTS' header): (1) the gray labels to the right of each glyph are not vertically aligned across rows — align them cleanly in a column; (2) make the 'ZERO DOT VARIANTS' mid-section header bold; (3) add a matching top header (e.g. 'KEY GLYPH COMPARISONS') above the first group so both groups have a bold header. Edit the Typst/source that lays out this figure.
