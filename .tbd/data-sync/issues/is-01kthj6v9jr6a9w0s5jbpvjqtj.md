---
type: is
id: is-01kthj6v9jr6a9w0s5jbpvjqtj
title: Add SemiBold (600) weight + italic to fill the 500->700 gap
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01kthj4yda44ebzchx923mdh31
created_at: 2026-06-07T17:31:08.465Z
updated_at: 2026-06-07T17:31:08.465Z
---
Extend the ladder with SemiBold (600) and SemiBold Italic via the existing FontForge changeWeight approach (as Medium 500 derives from Regular). Tune the change amount so 600 sits cleanly between Medium (500) and Bold (700); review stems/fitting and watch cell bleed. Touch: config.py VARIANTS + weight map; _INTERMEDIATE_WEIGHTS (generate B612Mono-SemiBold/SemiBoldItalic + HackNerdFont-SemiBold/SemiBoldItalic); regenerate golden manifest; tests; specimen weight ladder + waterfall; README weights table; terminal-config. Result: 10 variants per family.
