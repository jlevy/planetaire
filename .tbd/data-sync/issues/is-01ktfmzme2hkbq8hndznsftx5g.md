---
type: is
id: is-01ktfmzme2hkbq8hndznsftx5g
title: "Release process: GitHub-only for v0.1.1 (disable PyPI auto-publish on tags)"
kind: chore
status: closed
priority: 2
version: 3
labels: []
dependencies:
  - type: blocks
    target: is-01ktfmrj11kys5ra1qcbj82h7r
parent_id: is-01ktfmqk88w01171trdj8ft0vp
created_at: 2026-06-06T23:41:08.929Z
updated_at: 2026-06-06T23:51:21.157Z
closed_at: 2026-06-06T23:51:21.156Z
close_reason: null
---
Per user: this pilot release publishes GitHub artifacts only; defer PyPI. Change publish.yml to workflow_dispatch only (remove the push:tags trigger) so tagging v0.1.1 triggers ONLY release-fonts.yml (GitHub Release + Extended/Text archives + SHA256SUMS). PyPI can be enabled later via manual dispatch once trusted publishing is configured. Release-process change -> goes in the release-prep PR.
