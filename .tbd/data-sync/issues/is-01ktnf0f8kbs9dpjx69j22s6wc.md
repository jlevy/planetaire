---
type: is
id: is-01ktnf0f8kbs9dpjx69j22s6wc
title: "unicode-range split web build (Google Fonts model): latin + latin-ext, 3 weights"
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01ktnez5fmvrc4ps4v4khqxy88
created_at: 2026-06-09T05:52:11.539Z
updated_at: 2026-06-09T05:52:11.539Z
---
Implement a --split path on the Text build that emits one WOFF2 per script subset and a multi-block @font-face stylesheet with canonical Google Fonts unicode-range descriptors, so browsers fetch only the ranges a page renders. Latin page: ~12 KB/weight instead of ~53 KB.

First package (per 2026-06-09 decision): latin + latin-ext only, 3 weights. OPEN: exact weight trio (Regular/Bold/ExtraBold vs Regular/Medium/Bold vs native Regular/Bold) and upright-only vs +italics.

Canonical ranges (Google Fonts / Fontsource / Bunny):
  latin     = U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD
  latin-ext = U+0100-024F,U+0259,U+1E00-1EFF,U+2020,U+20A0-20AB,U+20AD-20CF,U+2113,U+2C60-2C7F,U+A720-A7FF
(greek/greek-ext/cyrillic/cyrillic-ext available as later subsets; box-drawing/terminal would be a custom subset GF does not define.)

Files: recipes/planetaire_mono.py (build_text, _write_font_face_css), config.py (group TEXT_SUBSET_RANGES into named subsets + per-group unicode-range strings). Ref docs/web-font-research.md 6.2.
