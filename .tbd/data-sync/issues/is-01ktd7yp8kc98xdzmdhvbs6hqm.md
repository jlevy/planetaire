---
type: is
id: is-01ktd7yp8kc98xdzmdhvbs6hqm
title: Terminal/specimen code samples must be valid, executable, straight-quoted
kind: bug
status: open
priority: 2
version: 1
labels:
  - readme
  - specimen
dependencies: []
created_at: 2026-06-06T01:14:57.683Z
updated_at: 2026-06-06T01:14:57.683Z
---
Sample content rendered in the terminal/specimen images (Python code and similar) currently contains curly/smart quotes where straight ASCII quotes belong. That is invalid source that would not run. Audit all embedded code samples, ensure they are genuinely executable/runnable, and replace any smart quotes (curly double/single, oriented apostrophes) with straight quotes in code contexts.
