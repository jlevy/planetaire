---
type: is
id: is-01ktfewqm7eqa37m37x0rz8n22
title: Regenerate specimen PDF and README images after specimen text edits
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01ktfevdbrypmftxq65hz54y2y
created_at: 2026-06-06T21:54:42.438Z
updated_at: 2026-06-06T22:13:49.602Z
closed_at: 2026-06-06T22:13:49.602Z
close_reason: Installed typst+fontforge, built both families, regenerated specimen PDF + README features images (other 6 images byte-identical => deterministic). fonts/output gitignored. Lint + 152 tests pass.
---
Specimen text changes require regenerating artifacts so committed outputs match source. Install tooling via scripts/setup-dev-tools.sh (typst, fontforge) or 'make dev-tools'; then 'make specimen' (PDF) and 'planetaire build images' (8 README PNGs). Update golden manifest only if fonts changed (they should not). If typst/network is unavailable in this env, document the blocker and leave regeneration for a tooling-capable run. Depends on the content.typ edits.
