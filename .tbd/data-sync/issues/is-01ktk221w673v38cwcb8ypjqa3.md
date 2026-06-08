---
type: is
id: is-01ktk221w673v38cwcb8ypjqa3
title: "Specimen: drop the ASCII character table"
kind: task
status: closed
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01kthj4yda44ebzchx923mdh31
created_at: 2026-06-08T07:27:23.013Z
updated_at: 2026-06-08T09:44:33.892Z
closed_at: 2026-06-08T09:44:33.892Z
close_reason: null
---
Remove the 'ASCII CHARACTER TABLE (HEXADECIMAL)' block from the specimen -- it does not add much. It starts at docs/specimen/planetaire-mono-specimen.typ:497 (#label[ASCII CHARACTER TABLE (HEXADECIMAL)], the #v(0.1cm) at :498, and the following #block(...)[ ... ] containing the man-page 'ascii' octal/hex/decimal excerpt). Remove the label, the spacing, and the whole block; check the surrounding #v spacing and section flow so the following content still lays out cleanly.
