---
type: is
id: is-01ktaz7gyasq4v8hsg6gxe4y6e
title: Unify font versioning; stop inheriting Hack's version
kind: bug
status: closed
priority: 1
version: 7
spec_path: docs/project/specs/active/plan-2026-06-05-finalize-and-publish.md
labels: []
dependencies:
  - type: blocks
    target: is-01ktaz8mj3vcz04jhwfqarnch8
  - type: blocks
    target: is-01ktb2q3yhbsv214dk6kn6qknr
parent_id: is-01ktaz70qyd5ap0c99chx6vfxq
created_at: 2026-06-05T04:04:01.097Z
updated_at: 2026-06-05T05:55:36.986Z
closed_at: 2026-06-05T05:55:36.986Z
close_reason: Added planetaire.version single-source; rename sets name5+fontRevision; recipe threads version; specimen reads via Typst --input
---
Built fonts report Hack's version (name ID 5 = 'Version 3.003 ... Nerd Fonts 3.3.0') because recipes/planetaire_mono.py calls rename_font() without version=, and ops/rename.py only sets name IDs 3/5 when version is provided. The Typst specimen separately hardcodes version='0.1.0', and head.fontRevision is also Hack's. Fix: derive a single version (git tag, same source as the Python package) and thread it through the build to set name IDs 3 (unique ID) and 5 (version), head.fontRevision, and inject into the specimen at compile time. See docs/engineering-review.md §3.1.
