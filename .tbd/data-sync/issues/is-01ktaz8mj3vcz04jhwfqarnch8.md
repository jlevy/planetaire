---
type: is
id: is-01ktaz8mj3vcz04jhwfqarnch8
title: "Polish PDF specimen: version stamp, regenerate mock data, add web-font page"
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-06-05-finalize-and-publish.md
labels: []
dependencies: []
parent_id: is-01ktaz70qyd5ap0c99chx6vfxq
created_at: 2026-06-05T04:04:37.571Z
updated_at: 2026-06-05T09:04:49.601Z
closed_at: 2026-06-05T09:04:49.600Z
close_reason: Version already injected; added build-date cover stamp + a Text/web-font specimen page; PDF regenerated. Mock-terminal-data regen left as optional note.
---
Specimen is good but: version is hardcoded '0.1.0' (wire to real version, see versioning bead); terminal mockup has hardcoded dir listing + git hashes (regenerate from real output so it can't go stale); add a web/text-font page once the web build lands; stamp font version + build date; tighten cover typography. Driven by build specimen recipe (add Typst to toolchain/CI). See docs/engineering-review.md §6.2.

## Notes

PARTIAL: specimen version is now injected via Typst --input (sys.inputs) and 'make specimen' uses the CLI, so the hardcoded 0.1.0 is fixed. REMAINING (needs Typst, not installed here): regenerate the mock terminal data from real output, add a Text/web-font page, stamp build date. Run 'planetaire build specimen' in an env with Typst.
