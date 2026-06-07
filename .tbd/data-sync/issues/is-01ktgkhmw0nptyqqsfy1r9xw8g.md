---
type: is
id: is-01ktgkhmw0nptyqqsfy1r9xw8g
title: Cut v0.1.2 (GitHub-only) and verify downloads
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-06-07T08:35:16.480Z
updated_at: 2026-06-07T08:35:16.480Z
---
After PR #7 merges to main: tag v0.1.2; release-fonts.yml builds both families (ttf/ + web/ subfolders, WOFF2-only) and publishes the GitHub Release. publish.yml is manual-only (no PyPI). Then download Extended + Text, verify SHA256SUMS, extract, confirm ttf//web layout + README + version 0.1.2, install/validate. Tag via API if the git proxy blocks tag pushes.
