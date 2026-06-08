---
type: is
id: is-01ktfews8v19zwp7x3454gcvpt
title: Fix stale font family names in terminal-config.md (iTerm2/Kitty)
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies:
  - type: blocks
    target: is-01ktfewpdcygyn84mgdfqw3jk6
parent_id: is-01ktfevdbrypmftxq65hz54y2y
created_at: 2026-06-06T21:54:44.123Z
updated_at: 2026-06-06T22:13:48.784Z
closed_at: 2026-06-06T22:13:48.783Z
close_reason: Fixed stale 'Planetaire Mono' -> 'Planetaire Mono Extended' in iTerm2 and Kitty entries.
---
Family was renamed to 'Planetaire Mono Extended' (config FAMILY_NAME), but terminal-config.md still uses the old 'Planetaire Mono' in iTerm2 (lines ~79,81) and Kitty (lines ~88-91). Update to 'Planetaire Mono Extended' and the correct full names ('Planetaire Mono Extended ExtraBold', etc.). Do not expand these unusual terminals; just make them accurate.
