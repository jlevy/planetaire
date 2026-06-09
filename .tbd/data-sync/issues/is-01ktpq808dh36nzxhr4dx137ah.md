---
type: is
id: is-01ktpq808dh36nzxhr4dx137ah
title: Run final pre-merge static-site QA on PR head
kind: task
status: open
priority: 1
version: 2
labels:
  - deployment
  - github-pages
  - qa
  - pr-18
dependencies:
  - type: blocks
    target: is-01ktpq52a6nvwpwre9nv3skh25
parent_id: is-01ktnfk8hmkeeje5ydpfaf8ghp
created_at: 2026-06-09T17:35:21.356Z
updated_at: 2026-06-09T17:35:33.446Z
---
After resolving local changes and pushing the intended final PR head, run a final static-site validation before marking PR #18 ready/mergeable: serve site/ locally, verify index.html and compare.html in browser at desktop and mobile widths, exercise homepage tabs/theme and comparator controls, confirm bundled fonts/SVG load, check no console errors or horizontal overflow, and clean up known HTML validation nits if they are still present (decorative comments with repeated hyphens in index.html; raw ampersand in the Google Fonts URL in compare.html).
