---
type: is
id: is-01ktaz8n3xjqktg4nkhz5wtw22
title: Clean terminal-output demo (static SVG + optional animation)
kind: feature
status: closed
priority: 2
version: 7
spec_path: docs/project/specs/active/plan-2026-06-05-finalize-and-publish.md
labels: []
dependencies:
  - type: blocks
    target: is-01ktaz8ncx3mp3dtk1g00xjy01
parent_id: is-01ktaz70qyd5ap0c99chx6vfxq
created_at: 2026-06-05T04:04:38.141Z
updated_at: 2026-06-05T09:02:10.015Z
closed_at: 2026-06-05T09:02:10.015Z
close_reason: VHS terminal demo (terminal-demo.tape) renders GIF+PNG showing planetaire+flowmark in real CLI use; embedded in README; site pulls it from docs/images
---
Produce a clean terminal-output demo of Planetaire Mono in live CLI use, scripting real programs (e.g. Claude Code, mark) via a VHS .tape so it is reproducible. Output a static SVG for the README and an animated version (GIF/SVG/webm) for the site. Use a fixed terminal theme + font so frames are deterministic. See plan-2026-06-05-finalize-and-publish.md.

## Notes

BLOCKED on VHS (charmbracelet/vhs, not installed in this env). Plan: add a checked-in .tape scripting real programs (Claude Code, flowmark) against a fixed theme + Planetaire Mono Extended; output terminal-demo.svg (README) + animated (site). The site generator already auto-includes terminal-demo.{svg,gif,webm} from fonts/output when present.
