---
type: is
id: is-01ktfmrja2hp9mjh78y0mrbgkd
title: "Release: verify downloads + install end to end from the published release"
kind: task
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01ktfmqk88w01171trdj8ft0vp
created_at: 2026-06-06T23:37:17.378Z
updated_at: 2026-06-06T23:59:50.408Z
closed_at: 2026-06-06T23:59:50.408Z
close_reason: Downloaded all assets from the v0.1.1 Release; sha256sum -c OK; Extended->8 TTFs, Text->8 TTF/WOFF2/WOFF+CSS; fonts validate (exit 0) and report Version 0.1.1. README 'latest' URL resolves to v0.1.1 and extracts cleanly.
---
After v0.1.0 is released: download Extended + Text archives from the release, verify against SHA256SUMS, extract, install, and validate the fonts; check the GitHub Release page and (if published) the PyPI page.
