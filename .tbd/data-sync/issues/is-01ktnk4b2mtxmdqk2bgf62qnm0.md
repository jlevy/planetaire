---
type: is
id: is-01ktnk4b2mtxmdqk2bgf62qnm0
title: FontForge regeneration environment + provenance capture
kind: task
status: closed
priority: 1
version: 7
labels: []
dependencies:
  - type: blocks
    target: is-01ktnf0fk1pped6y033j1a51mw
  - type: blocks
    target: is-01ktj5081c0cs8hkc4veef0nyy
  - type: blocks
    target: is-01ktnk4xc3dg0mac0vtkp339n8
parent_id: is-01ktnez5fmvrc4ps4v4khqxy88
created_at: 2026-06-09T07:04:12.627Z
updated_at: 2026-06-09T07:35:39.694Z
closed_at: 2026-06-09T07:35:39.693Z
close_reason: Environment and provenance captured. FontForge is available locally and baseline build evidence is recorded; full regeneration is now blocked by plt-hhpi rather than by missing setup.
---
Set up a reproducible environment for regenerating synthetic font masters with FontForge, which is not available in the Codex sandbox. Record FontForge version, platform, command sequence, and source commit. Use this before touching generated masters so Medium/SemiBold/ExtraBold regeneration can be audited later. Expected evidence: fontforge --version output, exact planetaire commands or Python entrypoints, before/after SHA256 summary, and notes about whether the run happened locally or in CI.

## Notes

2026-06-09 provenance capture: platform Darwin arm64, Darwin Kernel 25.2.0; FontForge 20251009, build date 2025-10-09 19:02 UTC; typst 0.14.2; source commit 778812a7bfbf45ac6ac1a65d8f322b9b542189d9 on claude/slim-web-fonts. Comparison root: /private/tmp/planetaire-regen-compare.2Flm4g. Baseline commands completed: uv run --frozen planetaire build planetaire-mono --output-dir /private/tmp/planetaire-regen-compare.2Flm4g/current-output; uv run --frozen planetaire build text --output-dir /private/tmp/planetaire-regen-compare.2Flm4g/current-output --formats ttf; uv run --frozen planetaire build text --output-dir /private/tmp/planetaire-regen-compare.2Flm4g/current-output --split --italics. Forced clean regen command attempted against temp source copy: uv run --frozen planetaire build planetaire-mono --source-dir /private/tmp/planetaire-regen-compare.2Flm4g/regen-source --output-dir /private/tmp/planetaire-regen-compare.2Flm4g/regen-output. It regenerated B612 Medium/SemiBold and italic companions in the temp source copy, then stalled on HackNerdFont-Medium.ttf with max_points=None and was killed. New blocker is plt-hhpi; full all-master comparison should resume after that fix.
