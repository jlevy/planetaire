---
type: is
id: is-01ktnez5fmvrc4ps4v4khqxy88
title: Web-font delivery (Google Fonts model) + synthetic-weight reproducibility
kind: epic
status: open
priority: 1
version: 14
labels: []
dependencies: []
child_order_hints:
  - is-01ktnf0f8kbs9dpjx69j22s6wc
  - is-01ktnf0fk1pped6y033j1a51mw
  - is-01ktnf0fx6qm76y7k418bwp574
  - is-01ktnf0g7ahcwvcqtb1zeqyyyb
  - is-01ktnf0ghew6mqyyyva1ygwt17
  - is-01ktnf0gvq8msx5q9jvacspgq5
  - is-01ktnf0h6mje19vyjz8z284v4y
  - is-01ktnk4b2mtxmdqk2bgf62qnm0
  - is-01ktnk4xc3dg0mac0vtkp339n8
  - is-01ktnk5acrfx5jxtqfm0ext2fe
  - is-01ktnmvbex5633f08qppcxhw3k
created_at: 2026-06-09T05:51:28.754Z
updated_at: 2026-06-09T07:59:57.972Z
---
Make Planetaire Mono Text a first-class web font and close a weight-pipeline provenance gap found during the web-font review.

Two threads:
1) Web delivery (docs/web-font-research.md): adopt the Google Fonts unicode-range subset model so a Latin page pulls ~12 KB/weight instead of ~53 KB, plus free build trims, delivery guidance, and doc-size reconciliation. Decision (2026-06-09): first web package = Google Fonts model, latin + latin-ext subsets, 3 weights.
2) Synthetic-weight reproducibility/quality: the vendored ExtraBold masters are NOT reproducible from our pipeline (foreign lineage), and the emboldened weights (esp. SemiBold 600) carry outline bloat.

Reuses existing beads from epic plt-qt70: plt-ddjw (SemiBold ultra-dense logo glyphs at the point cap) and plt-8cyc (OTF output; related to the variable-font spike). Source of findings: docs/web-font-research.md and the 2026-06-09 metadata investigation of fonts/source/b612.

## Notes

2026-06-09 map after PR #19 and first regen comparison: web split delivery is implemented as Regular/Bold upright base plus optional Regular/Bold italics under the same Planetaire Mono Text family. Remaining/active work is organized as: (1) plt-tis5 for metric-matched fallback CSS/CDN guidance; (2) plt-5qf1 closed, FontForge/provenance captured; (3) plt-hhpi closed, Hack Medium now uses the bounded dense-glyph path so clean temp regeneration completes; (4) plt-2sb5 for committing the clean B612 ExtraBold/ExtraBoldItalic lineage; (5) plt-ddjw for true full-fidelity dense Nerd Font logo glyph emboldening if we do not accept the cap exception; (6) plt-5pr6 in progress for copying/regenerating every generated source master, SHA256SUMS, and provenance docs; (7) plt-xg0o for specimen/golden/metadata/size QA, with first temp artifacts in /private/tmp/planetaire-regen-compare.2Flm4g; (8) plt-c8zu as optional outline cleanup after baseline regeneration is understood; (9) plt-89qo and plt-8cyc as later variable/OTF packaging work.
