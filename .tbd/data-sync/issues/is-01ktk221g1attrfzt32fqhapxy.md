---
type: is
id: is-01ktk221g1attrfzt32fqhapxy
title: Rename 'Families' (Text/Extended) to 'Packages' across specimen, README, site
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01kthj4yda44ebzchx923mdh31
created_at: 2026-06-08T07:27:22.624Z
updated_at: 2026-06-08T07:27:22.624Z
---
Text and Extended are not different font families -- they are the same typeface in different packagings: Extended is the full build (added icons/Nerd Font/Powerline) for terminal/local use; Text is a lightweight web subset; they also differ by format (web vs terminal/local). Calling them 'Families' is inaccurate. Adopt 'Packages' (or a similarly accurate term).

Occurrences to update:
- docs/specimen/planetaire-mono-specimen.typ:202  #spec-row("Families", "Extended, Text")
- docs/specimen/planetaire-mono-specimen.typ:688  #section[Two Families: Extended and Text]
- src/planetaire/recipes/site.py:134  <th>Family</th>
- README.md:202  ## Two Families: Text and Extended
Check for other 'family/families' wording that refers to the Text/Extended split. Keep the OpenType nameID family names unchanged (those are legitimately 'family').
