---
type: is
id: is-01ktd7yp8kc98xdzmdhvbs6hqm
title: Terminal/specimen code samples must be valid, executable, straight-quoted
kind: bug
status: closed
priority: 2
version: 2
labels:
  - readme
  - specimen
dependencies: []
created_at: 2026-06-06T01:14:57.683Z
updated_at: 2026-06-06T01:25:34.800Z
closed_at: 2026-06-06T01:25:34.799Z
close_reason: "Audited all specimen/image code samples: orbit-code, the terminal one-liner, microgpt.py, and the HTML sample all already use straight ASCII quotes. The only curly quotes are intentional U+201C/201D in the Turing PROSE passage (correct typography, not code). Added a missing 'import math' to orbit-code so it is genuinely runnable. No invalid quotes in any code sample."
---
Sample content rendered in the terminal/specimen images (Python code and similar) currently contains curly/smart quotes where straight ASCII quotes belong. That is invalid source that would not run. Audit all embedded code samples, ensure they are genuinely executable/runnable, and replace any smart quotes (curly double/single, oriented apostrophes) with straight quotes in code contexts.
