---
type: is
id: is-01ktfewps3af5j0dxsfjzxgw33
title: Add the guideline footer to every owned Markdown doc
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01ktfevdbrypmftxq65hz54y2y
created_at: 2026-06-06T21:54:41.571Z
updated_at: 2026-06-06T22:13:49.061Z
closed_at: 2026-06-06T22:13:49.060Z
close_reason: Added guideline footer to fonts/source/README.md; all other owned docs already had it; vendored/generated excluded.
---
Every owned Markdown doc must end with the common-doc-guidelines footer:
<!-- This document follows common-doc-guidelines.md.\nSee github.com/jlevy/practical-prose and review guidelines before editing.\n-->
Audit shows only fonts/source/README.md is missing it. Add it there. Exclude vendored/generated files: fonts/source/licenses/Hack-LICENSE.md, .claude/skills/**, .agents/skills/** (tbd/flowmark-generated).
