---
type: is
id: is-01kthj6vk0dp2t00y5dhn8vy82
title: Emit OTF (CFF) alongside TTF for both families
kind: task
status: open
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01kthj4yda44ebzchx923mdh31
created_at: 2026-06-07T17:31:08.767Z
updated_at: 2026-06-08T07:27:23.269Z
---
Add OTF (CFF/cubic) desktop output for Extended and Text (some tools prefer OTF). Convert built TrueType outlines to CFF via fontTools (quadratic->cubic). Add otf to build formats; package into the desktop set (decide: rename ttf/ -> desktop/ holding ttf+otf, or add an otf/ folder beside ttf/); update release-fonts.yml, the per-archive README, and the README. Validate the OTFs.
