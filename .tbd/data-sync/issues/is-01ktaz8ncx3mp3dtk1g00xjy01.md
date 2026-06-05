---
type: is
id: is-01ktaz8ncx3mp3dtk1g00xjy01
title: Build a simple generated static site (GitHub Pages)
kind: feature
status: closed
priority: 2
version: 6
spec_path: docs/project/specs/active/plan-2026-06-05-finalize-and-publish.md
labels: []
dependencies: []
parent_id: is-01ktaz70qyd5ap0c99chx6vfxq
created_at: 2026-06-05T04:04:38.429Z
updated_at: 2026-06-05T06:29:12.958Z
closed_at: 2026-06-05T06:29:12.957Z
close_reason: Static site generator (recipes/site.py + build site + make site) delivers a self-contained landing+specimen+web-fonts site; hero/demo auto-included when produced (plt-7b9q/plt-wgvi); deploy deferred per owner
---
Minimal static site (single page acceptable) hosting the live HTML specimen, the terminal demo, install/terminal-config instructions, and download links for both full and web/text builds. Publish via GitHub Pages from a generated site/ directory, dependency-light, produced by a make target so it never rots. Depends on web font + HTML specimen + terminal demo. See docs/engineering-review.md §6.5.

## Notes

DONE: recipes/site.py + 'planetaire build site' + 'make site' generate a self-contained site/ (landing + HTML specimen + Text web fonts), tested. Hero image (plt-7b9q) and animated demo (plt-wgvi) are auto-included when present but need Typst/VHS to produce. Deployment intentionally deferred per owner.
