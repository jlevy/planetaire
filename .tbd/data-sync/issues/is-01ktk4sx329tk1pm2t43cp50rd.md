---
type: is
id: is-01ktk4sx329tk1pm2t43cp50rd
title: Specimen embedded DejaVu in code blocks; force Planetaire raw font + font QA
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01kthj4yda44ebzchx923mdh31
created_at: 2026-06-08T08:15:21.697Z
updated_at: 2026-06-08T09:44:33.717Z
closed_at: 2026-06-08T09:44:33.716Z
close_reason: null
---
Typst's built-in font for raw (code) elements is DejaVu Sans Mono. Every raw block / inline code span in the specimen that did not explicitly set the Planetaire font (the microGPT code pages 7-9, the inline @font-face span on the Two Packages page) silently rendered in DejaVu, so the specimen PDF embedded DejaVuSansMono + DejaVuSansMono-Oblique.

FIX: added a document-level '#show raw: set text(font: "Planetaire Mono Extended")' right after the global text-font set in docs/specimen/planetaire-mono-specimen.typ (per-block rules still override size, or switch to the Text family for the web-subset demo). Result: a fresh 'planetaire build specimen' embeds only PlanetaireMonoExtended-* (10 weights) + PlanetaireMonoText-Regular (the intentional web-subset demo), 0 DejaVu.

QA: added tests/recipes/test_specimen_fonts.py -- renders the specimen and asserts every embedded /BaseFont is a PlanetaireMono* face (fails on any Typst fallback). Skips if typst or built fonts are absent.

Found while investigating plt-uuag (the 'spindly apostrophe', which was actually a stale committed PDF; the font's U+0027 is intact).
