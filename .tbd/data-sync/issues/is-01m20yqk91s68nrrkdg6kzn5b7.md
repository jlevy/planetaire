---
type: is
id: is-01m20yqk91s68nrrkdg6kzn5b7
title: Web-font sync globs too broadly and can publish stale split subsets
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-08T16:48:29.459Z
updated_at: 2026-09-08T16:52:52.756Z
closed_at: 2026-09-08T16:52:52.756Z
close_reason: "Fixed on fix/release-font-version-stamp (commit 38d8cd9): explicit --version threaded into the font builds and release.py, enumerated published file set, devtools/check_web_fonts.py gating CI and release finalize, and a byte-for-byte test."
resolution: null
duplicate_of: null
---
`sync_web_font_dir()` in scripts/release.py copied `fonts/output/PlanetaireMonoText-*.woff2`
and `planetaire-mono-text*.css` into fonts/web/ and site/fonts/. Both globs are wider than
the published set: the first matches the `--split` subset slices
(`PlanetaireMonoText-Regular-latin.woff2`), the second matches the italic companion
stylesheet. fonts/output is a working directory that keeps whatever earlier builds left
there, so a release run against a dirty fonts/output swept 21 stale split files into both
published directories.

docs/website.runbook.md documented the same glob as the manual refresh recipe, and its
'or from a release archive' variant was worse: the archive's web/ folder *is* the split
layout.

Fixed with plt-0204: the file set is enumerated in `config.text_web_font_file_names()`
and used by release.py's sync, by devtools/check_web_fonts.py (which also removes
anything else from the directories), and by the CI gate. The runbook now points at
`check_web_fonts.py --write` instead of a cp glob.
