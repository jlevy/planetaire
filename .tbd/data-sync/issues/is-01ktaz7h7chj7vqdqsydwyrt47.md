---
type: is
id: is-01ktaz7h7chj7vqdqsydwyrt47
title: Split into Planetaire Mono Text (web) and Extended (full); add WOFF2/WOFF
kind: feature
status: closed
priority: 1
version: 10
spec_path: docs/project/specs/active/plan-2026-06-05-finalize-and-publish.md
labels: []
dependencies:
  - type: blocks
    target: is-01ktaz8mv1vktxrbd8k2j9a5rf
  - type: blocks
    target: is-01ktaz8mj3vcz04jhwfqarnch8
  - type: blocks
    target: is-01ktb2q3yhbsv214dk6kn6qknr
  - type: blocks
    target: is-01ktb2q4jkpsbxqvq0n3kws8w2
parent_id: is-01ktaz70qyd5ap0c99chx6vfxq
created_at: 2026-06-05T04:04:01.388Z
updated_at: 2026-06-05T06:05:03.532Z
closed_at: 2026-06-05T06:05:03.531Z
close_reason: Added ops/subset.py + build_text recipe + CLI 'build text'; produces Planetaire Mono Text (WOFF2/WOFF/TTF + @font-face CSS), 1317 glyphs/55KB woff2. Full build keeps 'Planetaire Mono' family; Extended hard-rename deferred (noted in spec).
---
Split the family into two builds from one pipeline. (1) Planetaire Mono Text: standard-Unicode coverage for web/regular use -- Latin, Latin Extended, Greek, Cyrillic, punctuation, currency, super/subscripts, common arrows/math, AND box-drawing + block elements + geometric shapes (markdown tables, TUIs, ASCII art like Claude Code graphics). DROP only the ~10,400 Nerd Font PUA icons and Powerline. MEASURED: ~1,376 glyphs, 131KB TTF, ~53KB WOFF2/weight vs 984KB WOFF2 full -- ~18x smaller; box-drawing adds only ~8KB. (2) Planetaire Mono Extended: current full build (Nerd icons + Powerline), RENAMED from 'Planetaire Mono'. Implement via new ops/subset.py (fontTools.subset), TEXT_SUBSET_RANGES in config.py, build_text recipe emitting TTF/WOFF/WOFF2 + generated @font-face CSS. Needs brotli dep for WOFF2. See plan-2026-06-05-finalize-and-publish.md.
