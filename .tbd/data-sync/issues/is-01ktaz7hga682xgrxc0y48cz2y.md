---
type: is
id: is-01ktaz7hga682xgrxc0y48cz2y
title: Add CI job to build, validate, and regression-verify the fonts
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-06-05-finalize-and-publish.md
labels: []
dependencies: []
parent_id: is-01ktaz70qyd5ap0c99chx6vfxq
created_at: 2026-06-05T04:04:01.674Z
updated_at: 2026-06-05T06:08:26.422Z
closed_at: 2026-06-05T06:08:26.422Z
close_reason: "Added 'fonts' CI job: builds Extended+Text, validates both, regression-verify"
---
CI (.github/workflows/ci.yml) currently only lints + pytest; the font artifacts are never built or checked in CI, and release-fonts.yml does not run regression verify. Add a Linux CI job (with FontForge + Typst installed, source fonts cached) running: build download -> build planetaire-mono -> validate fonts/output/*.ttf -> regression verify. Makes the golden manifest load-bearing. See docs/engineering-review.md §4.2.
