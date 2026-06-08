---
type: is
id: is-01ktfmrhegbcg2b383fjpgbbvg
title: "Release: local end-to-end dry run (build, package, checksums, install)"
kind: task
status: closed
priority: 2
version: 5
labels: []
dependencies:
  - type: blocks
    target: is-01ktfmrhqwjgnz37sgrmd9byh9
  - type: blocks
    target: is-01ktfmrj11kys5ra1qcbj82h7r
parent_id: is-01ktfmqk88w01171trdj8ft0vp
created_at: 2026-06-06T23:37:16.496Z
updated_at: 2026-06-06T23:51:21.677Z
closed_at: 2026-06-06T23:51:21.677Z
close_reason: null
---
Locally replicate release-fonts.yml: build both families, create PlanetaireMono-Extended/.Text tar.xz+zip, SHA256SUMS; then extract, verify checksums, install TTFs, validate. Also verify version resolves to 0.1.0 from a local v0.1.0 tag (uv-dynamic-versioning) and is embedded in the fonts. No public release.
