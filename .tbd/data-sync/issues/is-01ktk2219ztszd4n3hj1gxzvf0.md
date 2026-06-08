---
type: is
id: is-01ktk2219ztszd4n3hj1gxzvf0
title: "Specimen About page: true blank lines between paragraphs (man-page spacing)"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01kthj4yda44ebzchx923mdh31
created_at: 2026-06-08T07:27:22.431Z
updated_at: 2026-06-08T07:27:22.431Z
---
On the About page of the specimen, the spacing between paragraphs (and before/after the bulleted list) comes from Typst paragraph/block spacing, not true blank lines. Make it read like true monospace text (a man page): exactly one full blank monospace line between paragraphs and around the list.

FIX: set the block/par spacing on the About/card content so inter-paragraph and list gaps equal one blank line of the monospace grid (block spacing ~= line height/leading) rather than the current partial spacing; verify it reads evenly like fixed-pitch text. File: docs/specimen/planetaire-mono-specimen.typ (About/card content; check card.typ / content.typ if shared).
