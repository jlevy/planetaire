---
type: is
id: is-01ktj5wdkhsdjeaa94s0vpweqf
title: "Version stamp: keep specimen PDF + title current with the release version"
kind: task
status: open
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01kthj4yda44ebzchx923mdh31
created_at: 2026-06-07T23:14:58.289Z
updated_at: 2026-06-08T02:28:26.898Z
---
Version derivation FIXED (commit 4e75675): version.py now resolves the release version from the latest git tag (metadata fallback for installed builds), so the specimen/fonts stamp the current release automatically and a new tag updates everything with no manual step. Remaining (P3 release hygiene): ensure the release workflow re-runs 'planetaire build specimen' + 'build images' at the tag so the COMMITTED specimen PDF and README banner reflect the new version (otherwise they lag until the next rebuild).
