---
type: is
id: is-01m1zw66916faf42c20ye0xxzn
title: "PR #26 review P26-R6: height checks silently skip instead of reporting"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m1zw5fshk142fvk4g9wc52k9
created_at: 2026-09-08T06:44:47.520Z
updated_at: 2026-09-08T07:22:54.867Z
closed_at: 2026-09-08T07:22:54.867Z
close_reason: null
resolution: null
duplicate_of: null
---
validate.py:146-150,183-184. Fail when x/H absent from a subset that should have them; skip with an info Issue only for scripts that lack them by design.
