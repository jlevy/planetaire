---
type: is
id: is-01ktghbdpt1ya92g1kb7xpmpmc
title: "Next release: standardize release archive naming + structure"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-06-07T07:56:55.374Z
updated_at: 2026-06-07T07:56:55.374Z
---
Make packaging match font-project conventions and fix the 'Extended sounds like a superset of Text' confusion (the real break: the subset Text has web fonts but the superset Extended does not).

Conventions (verified from Fira Code, Inter, JetBrains Mono, Cascadia, Nerd Fonts):
- One archive per font, VERSION in the name (e.g., Fira_Code_v6.2.zip, Inter-4.1.zip).
- Formats split into SUBFOLDERS inside: ttf/, woff2/, woff/ (Inter uses web/ + extras/ttf/).
- Files named Family-Style.ext.

Proposed for Planetaire (release-fonts.yml change):
1. Add version to archive names: PlanetaireMono-Extended-vX.Y.Z.{tar.xz,zip}, PlanetaireMono-Text-vX.Y.Z.{...}.
2. Use subfolders inside each: ttf/ and web/ (woff2 + woff + css).
3. To honor 'Extended is a superset', generate web fonts (woff2/woff) for BOTH families so Extended truly contains everything Text does plus icons (or, if we keep web=Text-only, document it loudly). Decide with the user.
4. Optional: a short README.txt inside each archive.

Implementation: subset/build + ops to emit woff for Extended (if chosen); release-fonts.yml packaging; update README download links/anchors. For next release (v0.2.0).
