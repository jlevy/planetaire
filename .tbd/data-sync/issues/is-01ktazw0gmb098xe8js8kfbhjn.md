---
type: is
id: is-01ktazw0gmb098xe8js8kfbhjn
title: Regenerate specimen PDF and showcase images after polish fixes
kind: task
status: closed
priority: 2
version: 3
labels: []
dependencies: []
created_at: 2026-06-05T04:15:12.403Z
updated_at: 2026-06-06T08:00:20.277Z
closed_at: 2026-06-06T08:00:20.277Z
close_reason: Regenerated specimen PDF and all 8 README images with the corrected monospace fonts (typst/fontforge now installed via scripts/setup-dev-tools.sh).
---
The polish pass changed specimen/showcase SOURCES but the rendered artifacts
could not be regenerated in the review environment (typst and fontforge were
not installed). Once a machine with typst + fontforge is available, regenerate
and commit the updated artifacts so they match the source:

- docs/specimen/planetaire-mono-specimen.pdf
  (source fix: French pangram 'pondsjflam' -> 'pondent' in the .typ)
  Command: make specimen   (or: typst compile docs/specimen/planetaire-mono-specimen.typ ...)

- docs/images/weights.png
  (source fix: weight-comparison now includes Medium / Medium Italic = 8 variants)
  Command: make showcase

Both targets require building the fonts first (make build-fonts), which needs
fontforge for the emboldened ExtraBold/Medium weights.
