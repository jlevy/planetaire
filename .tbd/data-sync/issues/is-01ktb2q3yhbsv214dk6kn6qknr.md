---
type: is
id: is-01ktb2q3yhbsv214dk6kn6qknr
title: Package both Text and Extended families in release-fonts.yml
kind: task
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-06-05-finalize-and-publish.md
labels: []
dependencies: []
parent_id: is-01ktaz70qyd5ap0c99chx6vfxq
created_at: 2026-06-05T05:04:57.809Z
updated_at: 2026-06-05T06:08:26.684Z
closed_at: 2026-06-05T06:08:26.684Z
close_reason: release-fonts.yml now builds+packages both families with per-artifact SHA256
---
Update .github/workflows/release-fonts.yml to build and publish BOTH families on a tag: Extended (TTF archive, as today) and Text (TTF + WOFF2 + WOFF + generated @font-face CSS). Emit SHA-256 checksums for every artifact. Depends on the Text/Extended split (plt-py0f) and unified versioning (plt-g5ht). See plan-2026-06-05-finalize-and-publish.md (Rollout / API Changes).
