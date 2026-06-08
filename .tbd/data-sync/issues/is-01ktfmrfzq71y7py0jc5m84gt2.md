---
type: is
id: is-01ktfmrfzq71y7py0jc5m84gt2
title: "Polish: flowmark older spec docs to canonical style"
kind: task
status: closed
priority: 3
version: 3
labels: []
dependencies:
  - type: blocks
    target: is-01ktfmrj11kys5ra1qcbj82h7r
parent_id: is-01ktfmqk88w01171trdj8ft0vp
created_at: 2026-06-06T23:37:14.999Z
updated_at: 2026-06-06T23:51:20.364Z
closed_at: 2026-06-06T23:51:20.364Z
close_reason: null
---
Run flowmark --auto on docs/specs/font-pipeline-plan.md and docs/specs/font-customization-notes.md (and any other owned docs not yet canonical) to bring semantic line breaks + smart quotes in line with the rest. Code blocks untouched.
