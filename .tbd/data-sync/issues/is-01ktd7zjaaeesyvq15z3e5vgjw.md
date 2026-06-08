---
type: is
id: is-01ktd7zjaaeesyvq15z3e5vgjw
title: "embolden: repr() paths in generated FontForge script"
kind: bug
status: closed
priority: 2
version: 2
labels:
  - pr2
dependencies: []
created_at: 2026-06-06T01:15:26.410Z
updated_at: 2026-06-06T01:15:28.452Z
closed_at: 2026-06-06T01:15:28.451Z
close_reason: "Implemented in commit dda3728 (port of PR #2 clear wins)"
---
Paths interpolated into the generated FontForge script used raw double-quote interpolation, breaking on special characters. Now uses repr(). From PR #2 review.
