---
type: is
id: is-01ktaz82m4m25551f3rhqn14vz
title: Decide and apply a single hinting policy for shipped fonts
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-06-05-finalize-and-publish.md
labels: []
dependencies: []
parent_id: is-01ktaz70qyd5ap0c99chx6vfxq
created_at: 2026-06-05T04:04:19.204Z
updated_at: 2026-06-05T06:19:50.042Z
closed_at: 2026-06-05T06:19:50.042Z
close_reason: "Policy: strip donor (B612) instructions in merge (default); Hack keeps native hinting; Text fully unhinted. Applied + tested + manifest regenerated."
---
scripts/generate_showcase.py strips TrueType hinting before rendering ('Hack's hinting is incompatible with B612 glyphs'), implying shipped TTFs carry hinting that's wrong for B612-derived glyphs. The showcase shouldn't need a fix the real font lacks. Decide one policy for the artifact: strip hinting from B612-derived glyphs in the build, or re-hint with ttfautohint. See docs/engineering-review.md §3.4.
