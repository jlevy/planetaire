---
type: is
id: is-01ktd7zhnnbmfzwdt3kjqcex98
title: "regression: any outline-hash change is 'changed', not 'trivial'"
kind: bug
status: closed
priority: 1
version: 2
labels:
  - pr2
dependencies: []
created_at: 2026-06-06T01:15:25.748Z
updated_at: 2026-06-06T01:15:27.852Z
closed_at: 2026-06-06T01:15:27.851Z
close_reason: "Implemented in commit dda3728 (port of PR #2 clear wins)"
---
Regression detector classified a glyph whose outline hash changed but advance width stayed equal as 'trivial', silently hiding real outline regressions. Now any hash difference is classified 'changed'. From PR #2 review.
