---
type: is
id: is-01ktrbeb2dh447219g0h7jfxww
title: Create OJOSHE_DISPATCH_TOKEN PAT and add as repo secret (owner)
kind: task
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-06-10-migrate-hosting-to-ojoshe.md
assignee: jlevy
labels:
  - hosting
dependencies:
  - type: blocks
    target: is-01ktrbeb9r53mqxn1g831yt2mc
parent_id: is-01ktrbea4hppvkg87tkehkev1v
created_at: 2026-06-10T08:47:34.988Z
updated_at: 2026-06-10T08:47:35.912Z
---
Manual owner step: create a fine-grained PAT scoped to the ojoshe repo with Contents: read/write, and store it as secret OJOSHE_DISPATCH_TOKEN in jlevy/planetaire. Needed because GITHUB_TOKEN cannot dispatch cross-repo. Do before merging the migration PR so the merge propagates to ojoshe.com.
