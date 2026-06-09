---
type: is
id: is-01ktpq427atbwhje6pqqdttbh5
title: Resolve local PR state before launch
kind: task
status: open
priority: 1
version: 3
labels:
  - deployment
  - github-pages
  - pr-18
dependencies:
  - type: blocks
    target: is-01ktpq52a6nvwpwre9nv3skh25
  - type: blocks
    target: is-01ktpq808dh36nzxhr4dx137ah
parent_id: is-01ktnfk8hmkeeje5ydpfaf8ghp
created_at: 2026-06-09T17:33:12.297Z
updated_at: 2026-06-09T17:35:27.374Z
---
Before final PR validation, decide what to do with the current uncommitted working-tree changes: site/compare.css and site/compare.html look like current compact-controls work and should be reviewed, tested, committed, and pushed if intended; .tbd/config.yml, .agents/skills/flowmark/, and .codex/ should be reviewed separately so unrelated local setup does not leak into the site PR. Re-run git status and ensure PR #18 reflects the intended final site code.
