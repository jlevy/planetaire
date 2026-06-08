---
type: is
id: is-01ktaz7ht9ex895fhg3rd9g8hm
title: Fix README Jinja '{{ }}' artifact and standardize variant count to 8
kind: bug
status: closed
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-06-05-finalize-and-publish.md
labels: []
dependencies: []
parent_id: is-01ktaz70qyd5ap0c99chx6vfxq
created_at: 2026-06-05T04:04:01.993Z
updated_at: 2026-06-05T05:49:57.383Z
closed_at: 2026-06-05T05:49:57.383Z
close_reason: Fixed WezTerm Jinja artifact, standardized variant count to 8 (README + terminal-config), added Families section and dual-distribution note
---
Doc-accuracy fixes: (1) README WezTerm block (~lines 64-67) has doubled braces 'config.font_rules = {{ ... }}' from Copier/Jinja; make single braces; sweep for other braces. (2) Variant count says 10 (twice), 8, and 6 across README/terminal-config; standardize on 8. (3) Document the new Text/Extended family split and dual distribution (PyPI=tooling, GitHub Releases=fonts). See plan-2026-06-05-finalize-and-publish.md.
