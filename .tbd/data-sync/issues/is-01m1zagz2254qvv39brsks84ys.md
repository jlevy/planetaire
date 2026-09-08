---
type: is
id: is-01m1zagz2254qvv39brsks84ys
title: PANOSE bWeight is stale on the synthetic weights
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-09-08T01:36:06.208Z
updated_at: 2026-09-08T01:36:06.208Z
---
`rename_font` sets `OS/2.usWeightClass` for every variant, but PANOSE digit 3
(bWeight) is whatever the Hack master carried, so the two disagree on the
weights the pipeline synthesizes:

| face | usWeightClass | PANOSE bWeight |
| --- | ---: | --- |
| Regular | 400 | 6 (Medium) |
| Medium | 500 | 6 (Medium) |
| SemiBold | 600 | 6 (Medium) |
| Bold | 700 | 8 (Bold) |
| ExtraBold | 800 | 8 (Bold) |

SemiBold should read 7 (Demi) and ExtraBold 9 (Heavy). PANOSE is a coarse
classification used by font matchers and substitution tables, so the impact is
small, but `set_fixed_pitch_flags` already corrects `bProportion`, and the same
place could map usWeightClass to bWeight.

Found while fixing plt-y36x (OS/2 metrics derived from the merged outlines);
out of scope there because PANOSE is a classification, not a measurement.
