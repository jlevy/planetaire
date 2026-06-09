---
type: is
id: is-01ktnmvbex5633f08qppcxhw3k
title: Bound Hack generated-master regeneration before full regen comparison
kind: task
status: closed
priority: 1
version: 4
labels: []
dependencies:
  - type: blocks
    target: is-01ktnk4xc3dg0mac0vtkp339n8
parent_id: is-01ktnez5fmvrc4ps4v4khqxy88
created_at: 2026-06-09T07:34:15.260Z
updated_at: 2026-06-09T07:58:25.522Z
closed_at: 2026-06-09T07:58:25.522Z
close_reason: Bounded Hack Medium regeneration implemented and validated with a forced temp clean regen; full-fidelity dense-logo work remains tracked separately in plt-ddjw.
---
A forced clean regeneration in /private/tmp/planetaire-regen-compare.2Flm4g regenerated B612 Medium/SemiBold from the temp source copy, then stalled on HackNerdFont-Medium.ttf. The active FontForge script opened HackNerdFont-Regular.ttf with amount=40, target weight 500, and max_points=None; it ran at 99 percent CPU for many minutes while emitting thousands of FontForge spline, overlap, winding, and mapped-glyph warnings, then was killed. This shows the full-regeneration blocker is broader than the known 600 cap bead: Hack Medium also enters an unbounded dense-glyph path. Fix by adding a bounded, parallel, or otherwise reproducible fast path for Hack Medium/SemiBold regeneration, or by documenting a deliberate exception with generated-master provenance. After this lands, rerun the temp clean regen and comparison for all generated masters.

## Notes

Implemented in src/planetaire/recipes/planetaire_mono.py by applying the existing 500-point dense-glyph cap to HackNerdFont-Medium.ttf and HackNerdFont-MediumItalic.ttf. Validation: forced temp regeneration completed from /private/tmp/planetaire-regen-compare.2Flm4g/regen-source into /private/tmp/planetaire-regen-compare.2Flm4g/regen-output; previously stalled Hack Medium now generated, followed by Hack Medium Italic, Hack SemiBold, Hack SemiBold Italic, B612 ExtraBold, B612 ExtraBold Italic, and all Extended outputs. Follow-up full-fidelity work for the 49 skipped dense Nerd Font logo glyphs remains in plt-ddjw.
