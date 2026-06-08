---
type: is
id: is-01ktaz82x1fqvh2gswsfj6y7qd
title: Implement real 'build download' with checksums (or relabel step)
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-06-05-finalize-and-publish.md
labels: []
dependencies: []
parent_id: is-01ktaz70qyd5ap0c99chx6vfxq
created_at: 2026-06-05T04:04:19.489Z
updated_at: 2026-06-05T06:12:40.889Z
closed_at: 2026-06-05T06:12:40.889Z
close_reason: Implemented verify_sources() with SHA256SUMS integrity checking; relabeled command honestly (network fetch still TODO, noted)
---
recipes/sources.py::download_sources does not download -- it only checks vendored files and raises if absent -- yet README says 'Download source fonts and build'. Either implement real fetching from polarsys/b612 and ryanoasis/nerd-fonts releases with SHA256 checksums, or rename/relabel the step to 'verify vendored sources' and fix the README. Real downloads also unlock dropping binaries from git. See docs/engineering-review.md §4.3.
