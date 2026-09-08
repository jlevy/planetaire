---
type: is
id: is-01m20xcvzykg12ybjnxarp1203
title: Release builds the CDN web fonts before the tag exists, so fonts/web lags one version
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
created_at: 2026-09-08T16:25:09.374Z
updated_at: 2026-09-08T16:52:52.737Z
closed_at: 2026-09-08T16:52:52.733Z
close_reason: "Fixed on fix/release-font-version-stamp (commit 38d8cd9): explicit --version threaded into the font builds and release.py, enumerated published file set, devtools/check_web_fonts.py gating CI and release finalize, and a byte-for-byte test."
resolution: null
duplicate_of: null
---
The v0.2.0 release turned red on main's CI.

## Root cause

`scripts/release.py prepare` builds the fonts before `finalize` creates the tag, and
`build_planetaire_mono`/`build_text` take the version from `planetaire.version.get_version()`,
which reads the latest reachable git tag. At prepare time that is still the *previous*
release, so the committed `fonts/web/` and `site/fonts/` stamp the previous version into
name ID 5 and `head.fontRevision`. CI rebuilds at the tagged commit, where the tag does
exist, and stamps the new one.

The specimen PDF already avoids this: release.py passes `build specimen --version X.Y.Z`
explicitly. The font build has no such option.

## Why it surfaced now

PR #26 added the CI step 'Check committed fonts/web matches a rebuild' (`fonts` job in
.github/workflows/ci.yml). v0.2.0 (28589de) is the first release that gate has seen. The
lag itself predates it: v0.1.5's committed fonts/web says `Version 0.1.4`.

## Impact

None for users. A face-by-face diff shows only name ID 5 and head.fontRevision differ;
every OS/2 metric, bounding box and advance is identical, and both the release archives
(built by release-fonts.yml at the tag) and the CDN copy carry the corrected metrics.
It is a stale version stamp in the committed web fonts, and a red main.

## Fix

- Thread an explicit `--version` into `build planetaire-mono` and `build text`, the way
  `build specimen` already does, and pass the version being released from release.py.
- Make the CI rebuild derive the same version explicitly (from the tag) rather than
  implicitly, so the comparison is well defined on a release commit and an ordinary one.
- Gate it: a shared checker that rebuilds and compares fonts/web + site/fonts byte for
  byte, run by CI and by release finalize, plus a test that a release build and a
  rebuild at the resulting commit agree byte for byte.
