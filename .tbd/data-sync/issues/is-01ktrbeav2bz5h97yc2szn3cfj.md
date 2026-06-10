---
type: is
id: is-01ktrbeav2bz5h97yc2szn3cfj
title: Add notify-ojoshe.yml repository_dispatch workflow
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-06-10-migrate-hosting-to-ojoshe.md
labels:
  - hosting
  - ci
dependencies:
  - type: blocks
    target: is-01ktrbebgpts09ychnszt71pww
parent_id: is-01ktrbea4hppvkg87tkehkev1v
created_at: 2026-06-10T08:47:34.753Z
updated_at: 2026-06-10T08:50:28.024Z
closed_at: 2026-06-10T08:50:28.023Z
close_reason: "Done in PR #23: .github/workflows/notify-ojoshe.yml added (push to main on site/**, release published)"
---
New .github/workflows/notify-ojoshe.yml: on push to main touching site/** and on published releases, fire repository_dispatch type planetaire-release at the ojoshe repo via gh api, authenticated with secret OJOSHE_DISPATCH_TOKEN. Self-documenting comments; no ojoshe-internal details.
