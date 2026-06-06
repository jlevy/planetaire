---
type: is
id: is-01ktfewrm2eekw9e427n8jfpbm
title: Add accurate macOS Terminal.app install + config instructions
kind: task
status: closed
priority: 2
version: 3
labels: []
dependencies:
  - type: blocks
    target: is-01ktfewpdcygyn84mgdfqw3jk6
parent_id: is-01ktfevdbrypmftxq65hz54y2y
created_at: 2026-06-06T21:54:43.458Z
updated_at: 2026-06-06T22:13:48.209Z
closed_at: 2026-06-06T22:13:48.208Z
close_reason: Added macOS Terminal.app section + macOS font-install path; documented that Terminal.app applies family Bold and cannot map bold->ExtraBold.
---
terminal-config.md has no Apple Terminal.app section. Add accurate, followable steps:
- Install the font on macOS (download PlanetaireMono-Extended from Releases; double-click TTFs -> Font Book Install, or copy to ~/Library/Fonts). Link to README Install.
- Terminal.app: Settings (Cmd+,) > Profiles > Text > Font 'Change...' > select family 'Planetaire Mono Extended' + size. Note honestly: Terminal.app has only 'Use bold fonts' (uses the family's Bold 700); it has no per-intensity mapping, so ExtraBold-as-bold needs Ghostty/WezTerm. Verify behavior claims before committing.
