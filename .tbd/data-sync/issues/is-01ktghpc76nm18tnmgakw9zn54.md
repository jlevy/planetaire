---
type: is
id: is-01ktghpc76nm18tnmgakw9zn54
title: Package archives as ttf/ + web/ subfolders with per-archive README notes
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01ktghbdpt1ya92g1kb7xpmpmc
created_at: 2026-06-07T08:02:54.310Z
updated_at: 2026-06-07T08:35:15.678Z
closed_at: 2026-06-07T08:35:15.677Z
close_reason: "release-fonts.yml stages ttf/ + web/ subfolders with per-archive README (docs/release/readme-*.txt); archive names unversioned. Dry-run verified structure + sizes (Extended ~19MB, Text ~1MB). PR #7."
---
release-fonts.yml: stage each family into ttf/ (TTFs) and web/ (woff2+woff+css) subfolders before archiving (Inter/Fira convention). Add a short README.txt per archive: Extended -> local install, TTF is the standard option (web fonts also included); Text -> web use, WOFF the standard option (TTF also included). Keep archive names unversioned for stable latest-download URLs. Replicate in the local dry run.
