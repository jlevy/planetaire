---
type: is
id: is-01ktpq4pjbdyctq80hg3tpn28q
title: Enable GitHub Pages Actions source before merge
kind: task
status: closed
priority: 1
version: 3
labels:
  - deployment
  - github-pages
  - pr-18
dependencies:
  - type: blocks
    target: is-01ktpq52a6nvwpwre9nv3skh25
parent_id: is-01ktnfk8hmkeeje5ydpfaf8ghp
created_at: 2026-06-09T17:33:33.130Z
updated_at: 2026-06-10T10:05:08.111Z
closed_at: 2026-06-10T10:05:08.110Z
close_reason: Done historically (Pages served the site); Pages self-deploy now being retired in favor of ojoshe.com (plt-s5gz/plt-aiz4)
---
One-time GitHub repository setting before merging PR #18: Settings -> Pages -> Build and deployment -> Source: GitHub Actions. Confirm with gh/api that jlevy/planetaire has Pages configured and has_pages becomes true or the Pages endpoint no longer returns 404. No custom domain for this launch.
