---
type: is
id: is-01ktj5wdkhsdjeaa94s0vpweqf
title: "Version stamp: keep specimen PDF + title current with the release version"
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01kthj4yda44ebzchx923mdh31
created_at: 2026-06-07T23:14:58.289Z
updated_at: 2026-06-07T23:14:58.289Z
---
The specimen injects #version via 'planetaire build specimen --input version=<get_version()>' (from the git tag), but the committed PDF bakes in whatever it was built at -- currently shows v0.1.1. Need a mechanism so the specimen PDF (and any version-bearing artifacts/README) reflect the right version: e.g. regenerate the specimen as part of the release/tag workflow with the release version, or a documented bump step. For later.
