---
type: is
id: is-01ktnk4b2mtxmdqk2bgf62qnm0
title: FontForge regeneration environment + provenance capture
kind: task
status: open
priority: 1
version: 4
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
updated_at: 2026-06-09T07:05:16.311Z
---
Set up a reproducible environment for regenerating synthetic font masters with FontForge, which is not available in the Codex sandbox. Record FontForge version, platform, command sequence, and source commit. Use this before touching generated masters so Medium/SemiBold/ExtraBold regeneration can be audited later. Expected evidence: fontforge --version output, exact planetaire commands or Python entrypoints, before/after SHA256 summary, and notes about whether the run happened locally or in CI.
