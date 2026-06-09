---
type: is
id: is-01ktnez5fmvrc4ps4v4khqxy88
title: Web-font delivery (Google Fonts model) + synthetic-weight reproducibility
kind: epic
status: open
priority: 1
version: 12
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
created_at: 2026-06-09T05:51:28.754Z
updated_at: 2026-06-09T07:06:19.683Z
---
Make Planetaire Mono Text a first-class web font and close a weight-pipeline provenance gap found during the web-font review.

Two threads:
1) Web delivery (docs/web-font-research.md): adopt the Google Fonts unicode-range subset model so a Latin page pulls ~12 KB/weight instead of ~53 KB, plus free build trims, delivery guidance, and doc-size reconciliation. Decision (2026-06-09): first web package = Google Fonts model, latin + latin-ext subsets, 3 weights.
2) Synthetic-weight reproducibility/quality: the vendored ExtraBold masters are NOT reproducible from our pipeline (foreign lineage), and the emboldened weights (esp. SemiBold 600) carry outline bloat.

Reuses existing beads from epic plt-qt70: plt-ddjw (SemiBold ultra-dense logo glyphs at the point cap) and plt-8cyc (OTF output; related to the variable-font spike). Source of findings: docs/web-font-research.md and the 2026-06-09 metadata investigation of fonts/source/b612.

## Notes

2026-06-09 map after PR #19: web split delivery is implemented as Regular/Bold upright base plus optional Regular/Bold italics under the same Planetaire Mono Text family, not the earlier 3-weight default. Remaining work is now organized as: (1) plt-tis5 for metric-matched fallback CSS/CDN guidance; (2) plt-5qf1 to establish FontForge regeneration environment/provenance; (3) plt-2sb5 to fix B612 ExtraBold/ExtraBoldItalic lineage; (4) plt-ddjw to complete SemiBold 600 dense Nerd Font logo glyphs; (5) plt-5pr6 to run a clean regeneration pass for every generated source master from today’s pipeline; (6) plt-xg0o to review regenerated outputs with specimen/golden/metadata/size evidence; (7) plt-c8zu as optional outline cleanup after baseline regeneration is understood; (8) plt-89qo and plt-8cyc as later variable/OTF packaging work.
