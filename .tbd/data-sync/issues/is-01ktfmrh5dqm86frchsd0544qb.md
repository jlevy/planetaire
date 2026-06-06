---
type: is
id: is-01ktfmrh5dqm86frchsd0544qb
title: "Release: audit release-fonts.yml + publish.yml for first-release readiness"
kind: task
status: closed
priority: 2
version: 4
labels: []
dependencies:
  - type: blocks
    target: is-01ktfmrhqwjgnz37sgrmd9byh9
  - type: blocks
    target: is-01ktfmrj11kys5ra1qcbj82h7r
parent_id: is-01ktfmqk88w01171trdj8ft0vp
created_at: 2026-06-06T23:37:16.205Z
updated_at: 2026-06-06T23:51:21.422Z
closed_at: 2026-06-06T23:51:21.421Z
close_reason: null
---
Confirm: build needs no FontForge/Typst (vendored weights); version flows from tag via uv-dynamic-versioning into package + fonts; release-fonts.yml creates the Release and uploads Extended/Text tar.xz+zip + SHA256SUMS; publish.yml needs PyPI trusted publishing configured (pending publisher) for a first release. Note any gaps.
