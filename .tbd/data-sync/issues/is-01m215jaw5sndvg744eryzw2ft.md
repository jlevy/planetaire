---
type: is
id: is-01m215jaw5sndvg744eryzw2ft
title: LICENSE points at fonts/source/licenses/ paths that do not exist in the release bundle
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01ktnez5fmvrc4ps4v4khqxy88
created_at: 2026-09-08T18:47:57.060Z
updated_at: 2026-09-08T18:47:57.060Z
---
Reported downstream from jlevy/kpress PR #62 (review finding K62-R4).

LICENSE lines ~128/134/139 direct readers to fonts/source/licenses/B612-OFL.txt, Hack-LICENSE.md and NerdFonts-LICENSE. Those paths are repo-relative and resolve in the source tree, but the file is copied verbatim into the release archives, where the licence texts live under licenses/ instead. Confirmed against the extracted v0.2.0 archive: its LICENSE is byte-identical to the repo's and its pointers are dead there.

kpress copies LICENSE to src/kpress/licenses/planetaire-mono.txt, where the same three pointers resolve to nothing at all, and has had to add a mapping paragraph to its fonts README to compensate.

Also: the release bundle's README.txt describes licenses/ as covering '(B612, Hack, Nerd Fonts)' without naming EPL-2.0 or EDL-1.0, though both files are present in it.

Suggested: make the pointers relative to the licence directory itself, or state both layouts.
