---
type: is
id: is-01ktd7z0kctd0hb3kqjvydthqg
title: "Weights image: render every weight at the same width"
kind: task
status: closed
priority: 2
version: 2
labels:
  - readme
  - specimen
dependencies: []
created_at: 2026-06-06T01:15:08.268Z
updated_at: 2026-06-06T08:00:20.016Z
closed_at: 2026-06-06T08:00:20.016Z
close_reason: "Fixed via plt-bqux: weights now render at identical widths (verified in regenerated weights image + specimen weight-alignment QA panel)."
---
The weights/weight-ladder image currently renders each weight at a different width (different sample words/strings per row). Render every weight using the same string so they are all exactly the same width — more realistic to actual monospace usage. Edit the source that defines the per-weight sample text in the weights figure.
