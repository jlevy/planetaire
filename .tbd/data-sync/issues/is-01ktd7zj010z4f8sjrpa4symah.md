---
type: is
id: is-01ktd7zj010z4f8sjrpa4symah
title: "merge: hoist setGlyphOrder; fail loudly on unsupported GSUB merge"
kind: bug
status: closed
priority: 2
version: 2
labels:
  - pr2
dependencies: []
created_at: 2026-06-06T01:15:26.081Z
updated_at: 2026-06-06T01:15:28.151Z
closed_at: 2026-06-06T01:15:28.151Z
close_reason: "Implemented in commit dda3728 (port of PR #2 clear wins)"
---
merge_glyphs called setGlyphOrder inside the copy loop and appended donor GSUB feature records with unremapped lookup indices (corrupt table). Hoisted setGlyphOrder out of the loop and raise NotImplementedError on the unsupported GSUB merge path. From PR #2 review.
