---
type: is
id: is-01m215j1eene0f4ere43bvj4x4
title: Re-release so the published v0.2.0 artifacts and the tagged tree agree on the version
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01ktnez5fmvrc4ps4v4khqxy88
created_at: 2026-09-08T18:47:47.403Z
updated_at: 2026-09-08T18:47:47.403Z
---
Reported downstream from jlevy/kpress PR #62 (review finding K62-R3), which vendors these faces.

The fonts committed at tag v0.2.0 carry 'Version 0.1.5' in nameID 5 and '0.1.5;PlanetaireMonoText-*' in nameID 3. Cause, already fixed on this branch by 38d8cd9: scripts/release.py prepare built the fonts before finalize created the tag, and src/planetaire/version.py resolves from `git describe --tags --abbrev=0`, so the release commit stamped the preceding tag.

The fix is not enough on its own, because it does not re-tag or re-release. Two divergent v0.2.0 artifact sets are published:

- git tree at tag v0.2.0, which jsDelivr serves at @v0.2.0 -- stamped 0.1.5, licenses/ has OFL only;
- the GitHub release archives (PlanetaireMono-{Text,Extended}.{tar.xz,zip}), built by CI at the tagged commit -- stamped 0.2.0, licenses/ has all five texts.

Downstreams that follow the documented jsDelivr fetch line get the stale-stamped bytes, and always will: kpress pins them by sha256 and its NOTICE.md now has to explain why a PDF font list says 0.1.5. Verified metadata-only: 1317 glyphs, identical glyph order, zero outline-differing glyphs, identical advances/lsb, identical 1316-entry cmap, identical OS/2; only name[3], name[5], head.fontRevision and head.checkSumAdjustment differ.

Suggested: cut v0.2.1 from this branch so the tree, the archives and the CDN agree, and downstreams have a pin whose internal records match its name.
