---
type: is
id: is-01m1zw65bcbzmxwkyshb9v5nrb
title: "PR #26 review P26-R3: CI validates only fonts/output/*.ttf"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m1zw5fshk142fvk4g9wc52k9
created_at: 2026-09-08T06:44:46.572Z
updated_at: 2026-09-08T07:22:54.846Z
closed_at: 2026-09-08T07:22:54.846Z
close_reason: null
resolution: null
duplicate_of: null
---
Extend validate-fonts + CI to fonts/output/*.woff2 and fonts/web/*.woff2; add planetaire validate to scripts/release.py cmd_prepare after sync_web_fonts().
