---
type: is
id: is-01ktgkhmw0nptyqqsfy1r9xw8g
title: Cut v0.1.2 (GitHub-only) and verify downloads
kind: task
status: closed
priority: 1
version: 3
labels: []
dependencies: []
created_at: 2026-06-07T08:35:16.480Z
updated_at: 2026-06-07T08:43:51.987Z
closed_at: 2026-06-07T08:43:51.987Z
close_reason: "v0.1.2 released (GitHub-only). release-fonts.yml success; assets verified: checksums OK; Extended/Text archives are README.txt + ttf/ (8) + web/ (8 WOFF2 + CSS), no WOFF; fonts validate and report Version 0.1.2; README 'latest' URL resolves to v0.1.2 and extracts ttf/. No PyPI (publish.yml manual-only)."
---
After PR #7 merges to main: tag v0.1.2; release-fonts.yml builds both families (ttf/ + web/ subfolders, WOFF2-only) and publishes the GitHub Release. publish.yml is manual-only (no PyPI). Then download Extended + Text, verify SHA256SUMS, extract, confirm ttf//web layout + README + version 0.1.2, install/validate. Tag via API if the git proxy blocks tag pushes.
