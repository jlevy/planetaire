---
type: is
id: is-01ktgnax1h9tf8vb0zw61z5256
title: Fix en-dash rendering of -- CLI flags in the terminal mockup
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-06-07T09:06:32.614Z
updated_at: 2026-06-07T09:09:27.582Z
closed_at: 2026-06-07T09:09:27.582Z
close_reason: "Confirmed: Typst markup renders -- as an en dash, mangling eza --icons and git --oneline. Escaped to \\-\\- so they render as literal hyphens (verified in re-rendered terminal image). Specimen PDF re-rendered. PR #8."
---
Typst markup converts -- to an en dash, so 'eza -l --icons=always' and 'git log --oneline -3' render the long flags with an en dash (different from the single-hyphen -l). Escape the double hyphens (\-\-) in content.typ prompt() calls so they render as literal hyphens. Re-render terminal images + specimen PDF.
