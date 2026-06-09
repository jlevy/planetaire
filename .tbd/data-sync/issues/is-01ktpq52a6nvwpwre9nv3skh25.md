---
type: is
id: is-01ktpq52a6nvwpwre9nv3skh25
title: "Mark PR #18 ready and merge after final CI"
kind: task
status: open
priority: 1
version: 2
labels:
  - deployment
  - github-pages
  - pr-18
dependencies:
  - type: blocks
    target: is-01ktpq5cwkdcrm8b5rt75xcyxg
parent_id: is-01ktnfk8hmkeeje5ydpfaf8ghp
created_at: 2026-06-09T17:33:45.157Z
updated_at: 2026-06-09T17:34:40.729Z
---
After the local PR state is resolved and Pages is enabled, mark PR #18 ready for review if still draft, ensure CI passes on the final pushed head, and merge static-site into main. The merge is the trigger for .github/workflows/pages.yml because it runs on push to main touching site/** or the workflow.
