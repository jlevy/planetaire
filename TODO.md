# Planetaire Mono TODO

Work is tracked in detail with [`tbd`](https://github.com/jlevy/tbd) (beads); run
`tbd list` for live status. This file is the human-readable summary of the open
follow-ups.

## Follow-ups

- **Full-fidelity SemiBold logos** (`plt-ddjw`): the shipped SemiBold masters cap
  emboldening at 500 points, so about 49 ultra-dense Nerd Font logo glyphs (for
  example `dev-ohmyzsh`, 4,676 points) sit at base weight. FontForge `changeWeight`
  is pathologically slow on these (a full-font pass ran over two hours without
  finishing). The difference is visually imperceptible, since those glyphs appear in
  no specimen or README page, but for true full fidelity they should eventually be
  emboldened to 600. Options to explore: parallel-embolden just the capped glyphs
  across cores and merge them into the masters, a faster stroke or overlap method, or
  interpolation from Medium and Bold. Then drop or raise the cap.
- **OTF (CFF) output** (`plt-8cyc`): emit OTF alongside TTF for both families.
- **Cohesive specimen identity** (`plt-n561`): a consistent document ID and date, an
  accent color, and a unified footer across the specimen.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
