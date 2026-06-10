---
type: is
id: is-01ktrbeb9r53mqxn1g831yt2mc
title: "Retire self-deploy: delete pages.yml, disable Pages, set repo homepage"
kind: task
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-06-10-migrate-hosting-to-ojoshe.md
labels:
  - hosting
dependencies:
  - type: blocks
    target: is-01ktrbebgpts09ychnszt71pww
parent_id: is-01ktrbea4hppvkg87tkehkev1v
created_at: 2026-06-10T08:47:35.223Z
updated_at: 2026-06-10T08:47:36.097Z
---
Delete .github/workflows/pages.yml (in the migration PR). After the new canonicals are confirmed live on ojoshe.com: Settings -> Pages -> Source: None so jlevy.github.io/planetaire stops serving (no redirect kept), and set the repo homepage to https://ojoshe.com/planetaire/ (subsumes plt-dwes).
