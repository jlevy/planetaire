# Planetaire Mono TODO

Work is tracked in detail with [`tbd`](https://github.com/jlevy/tbd) (beads); run
`tbd list` for live status.
This file is the human-readable summary of the open follow-ups, ordered by priority.

## P1

The web-font and weight-reproducibility work is grouped under epic `plt-96bv`
(**Web-font delivery (Google Fonts model) + synthetic-weight reproducibility**), whose
items are tagged `plt-96bv` across P1–P3 below.
It came out of the web-font size review (`docs/web-font-research.md`) and a metadata
investigation of the vendored B612 masters.

- **unicode-range split web build** (`plt-3p61`, `plt-96bv`): ship the Google Fonts
  subset model — one WOFF2 per script plus a `unicode-range` `@font-face` stylesheet so
  a page fetches only what it renders.
  First package: `latin` + `latin-ext`, 3 weights.
  A Latin page then pulls ~12 KB/weight instead of ~53 KB.
- **Reproducible ExtraBold lineage** (`plt-2sb5`, `plt-96bv`): the vendored
  `B612Mono-ExtraBold*` files are an old hand-built artifact (ttfautohint v1.8.4,
  FontLab, a “B612 Mono Liga Nerd Font” lineage), not pipeline output — unlike
  Medium/SemiBold, which are genuine `embolden_font` outputs from Regular.
  Regenerate ExtraBold from the vendored Bold so every synthetic weight shares one
  clean, reproducible lineage, and fix the `fonts/source/README.md` provenance note (it
  omits SemiBold and mislabels ExtraBold).

## P2

- **Full-fidelity SemiBold logos** (`plt-ddjw`): the shipped SemiBold masters cap
  emboldening at 500 points, so about 49 ultra-dense Nerd Font logo glyphs (for example
  `dev-ohmyzsh`, 4,676 points) sit at base weight.
  FontForge `changeWeight` is pathologically slow on these (a full-font pass ran over
  two hours without finishing).
  The difference is visually imperceptible, since those glyphs appear in no specimen or
  README page, but for true full fidelity they should eventually be emboldened to 600.
  Options to explore: parallel-embolden just the capped glyphs across cores and merge
  them into the masters, a faster stroke or overlap method, or interpolation from Medium
  and Bold. Then drop or raise the cap.
- **Build trims: drop `post` names + trim `name`** (`plt-9azf`, `plt-96bv`): emit `post`
  format 3.0 and an English-only `name` table — about 6% off every web file with no
  visual change (~30 KB across the family).
- **Web delivery guidance** (`plt-tis5`, `plt-96bv`): document a minimal “Regular + one
  bold” recipe (~27 KB Latin) as the default rather than the ~649 KB full family, add a
  metric-matched fallback `@font-face` (≈0 CLS during swap), and `preload` plus
  immutable-cache guidance.
- **Reconcile size claims** (`plt-g0uj`, `plt-96bv`): the docs quote ~55–65 KB/weight;
  the measured Text WOFF2 is 53–77 KB/weight (avg ~65). Restate from rebuilt artifacts
  once the build trims land.

## P3

- **OTF (CFF) output** (`plt-8cyc`): emit OTF alongside TTF for both families (deferred
  until the specimen and packaging work is settled).
- **Cohesive specimen identity** (`plt-n561`): the cover now carries the little-planet
  logo, the version and date, and a page footer; the remaining piece is an accent color
  applied consistently across the specimen.
- **Version stamp** (`plt-makk`): the specimen PDF and title are stamped with the
  package version automatically at build; keep them current at each release.
- **Outline cleanup on emboldened weights** (`plt-c8zu`, `plt-96bv`): a `removeOverlap`
  \+ `simplify` pass to trim the heavy emboldened weights and clean SemiBold (600)
  outlines (its emboldening uses the largest single `changeWeight` step, from Regular —
  not a compounded chain through Medium).
  Needs a visual and regression check.
- **Variable-font spike** (`plt-89qo`, `plt-96bv`): one 400–800 variable WOFF2 for the
  whole weight ramp; the masters are partly FontForge-emboldened, so it needs a spike.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
