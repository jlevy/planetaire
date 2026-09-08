---
type: is
id: is-01m1zah7stb5dtwmf9s09v51z6
title: Note the OS/2 metrics fix in the next release notes
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-08T01:36:15.161Z
updated_at: 2026-09-08T01:36:15.161Z
---
plt-y36x changes the OS/2 vertical metrics of every shipped face: x-height
1094 -> 1120 and cap height 1458/1460 -> 1520-1525 per 2000 em, plus
xAvgCharWidth 1233-1240 -> 1204 and a usWin box that no longer clips.

The next docs/release/notes/vX.Y.Z.md needs a Fixes entry saying that consumers
reading the table (CSS font-size-adjust, editors' line boxes, font managers)
will now size the face to the letters actually drawn, and that sTypo* and hhea
are unchanged so line height does not move.

No separate action is needed for fonts/web/ and site/fonts/: the release script
(scripts/release.py prepare) rebuilds and refreshes both.
