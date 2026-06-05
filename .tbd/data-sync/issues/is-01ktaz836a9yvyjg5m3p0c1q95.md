---
type: is
id: is-01ktaz836a9yvyjg5m3p0c1q95
title: Fix placeholder package metadata (author/email) and add project URLs
kind: chore
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-06-05-finalize-and-publish.md
labels: []
dependencies: []
parent_id: is-01ktaz70qyd5ap0c99chx6vfxq
created_at: 2026-06-05T04:04:19.785Z
updated_at: 2026-06-05T05:49:57.637Z
closed_at: 2026-06-05T05:49:57.637Z
close_reason: Real author email + Homepage/Documentation/Issues URLs in pyproject.toml
---
pyproject.toml authors uses email='changeme@example.com'; .copier-answers.yml carries the same; Typst cover hardcodes 'Joshua Levy'. Set real author/email, reconcile naming, and add Homepage/Documentation URLs before any PyPI publish. See docs/engineering-review.md §4.4.
