---
type: is
id: is-01ktfewrywpbj4e4zdpt3gs83h
title: Verify and correct Ghostty config for accuracy (bold -> ExtraBold)
kind: task
status: closed
priority: 1
version: 3
labels: []
dependencies:
  - type: blocks
    target: is-01ktfewpdcygyn84mgdfqw3jk6
parent_id: is-01ktfevdbrypmftxq65hz54y2y
created_at: 2026-06-06T21:54:43.803Z
updated_at: 2026-06-06T22:13:48.482Z
closed_at: 2026-06-06T22:13:48.482Z
close_reason: Ghostty now uses font-style-bold/font-style-bold-italic = ExtraBold (verified against ghostty.org); README quick-config snippet updated to match.
---
Make the Ghostty section completely accurate and try-able. Current uses font-family + font-thicken (synthetic). To honor the 'map bold to ExtraBold (800)' guidance, use Ghostty's real keys (likely font-style-bold = ExtraBold and/or font-family-bold). Verify exact key names against current Ghostty docs (ghostty.org) before committing. Confirm font-family 'Planetaire Mono Extended' matches name ID 1/16.
