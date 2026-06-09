---
type: is
id: is-01ktnf0ghew6mqyyyva1ygwt17
title: Reconcile font-size claims in docs to measured (53-77 KB/wt, avg ~65)
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01ktnez5fmvrc4ps4v4khqxy88
created_at: 2026-06-09T05:52:12.846Z
updated_at: 2026-06-09T06:51:54.610Z
closed_at: 2026-06-09T06:51:54.609Z
close_reason: Updated README, build/release docs, runbook, site copy, release readme, specimen copy, and active spec notes to remove stale 55/65 KB full-Text web claims and describe the measured slim split web profile.
---
Size claims disagree and lean low: README "~65 KB/wt", recipes/site.py "~55 KB/wt", docs/fonts-build-and-release.md "~55 KB/wt", specimen .typ "about 65 KB". Measured Text WOFF2 = 53-77 KB/wt (avg ~65; min Regular 52.7, max SemiBold Italic 77.4). Restate from rebuilt artifacts after the post/name trims land, and add a "regenerate from the build" note so it stops drifting. Ref 9.
