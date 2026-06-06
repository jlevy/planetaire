---
type: is
id: is-01ktd7ypjrzsxwr8kyn1m4pq0a
title: Fix monospace alignment of ls listing sample (.rw / drw rows)
kind: bug
status: closed
priority: 2
version: 3
labels:
  - readme
  - specimen
dependencies: []
created_at: 2026-06-06T01:14:58.008Z
updated_at: 2026-06-06T01:23:46.915Z
closed_at: 2026-06-06T01:23:46.915Z
close_reason: "content.typ dir-entry: permissions field pinned to a fixed 7em box so .rw/drw rows align regardless of the period vs d advance. Image re-render tracked by plt-5kkw."
---
In the terminal listing sample (ls-style output), the rows starting with '.rw' and 'drw' are not vertically aligned, making it look non-monospace. Likely a leading-period vs letter width or column-padding issue in the sample text. Make every listing row line up perfectly in the rendered monospace output.
