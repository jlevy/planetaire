---
type: is
id: is-01ktfmqk88w01171trdj8ft0vp
title: "Planetaire Mono v0.1.0: final polish, release, and end-to-end verification"
kind: epic
status: open
priority: 1
version: 12
labels: []
dependencies: []
child_order_hints:
  - is-01ktfmrfnyd1k3dkhh09dsa4te
  - is-01ktfmrfzq71y7py0jc5m84gt2
  - is-01ktfmrg8z480x64x3rmjvk2ez
  - is-01ktfmrgjtfncfa0q7anrx9njs
  - is-01ktfmrgw69ww2xajtkt7j2ymq
  - is-01ktfmrh5dqm86frchsd0544qb
  - is-01ktfmrhegbcg2b383fjpgbbvg
  - is-01ktfmrhqwjgnz37sgrmd9byh9
  - is-01ktfmrj11kys5ra1qcbj82h7r
  - is-01ktfmrja2hp9mjh78y0mrbgkd
  - is-01ktfmzme2hkbq8hndznsftx5g
created_at: 2026-06-06T23:36:45.575Z
updated_at: 2026-06-06T23:41:08.929Z
---
First official release (v0.1.0). Sequence: (1) final polish on a cleanup branch -> PR; (2) audit + local dry-run of the release process; (3) any release-process fixes -> branch + PR; (4) cut v0.1.0 (tag) and monitor release-fonts.yml + publish.yml; (5) verify downloads end to end. Release mechanics: tag-driven (push vX.Y.Z); uv-dynamic-versioning derives the version from the tag; build needs neither FontForge nor Typst (intermediate weights vendored). PyPI publish uses trusted publishing (must be configured on PyPI for a first release).
