---
type: is
id: is-01ktfewpdcygyn84mgdfqw3jk6
title: Apply common-doc-guidelines to internal Markdown docs (dashes, conjunctions, language)
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01ktfevdbrypmftxq65hz54y2y
created_at: 2026-06-06T21:54:41.195Z
updated_at: 2026-06-06T22:13:49.324Z
closed_at: 2026-06-06T22:13:49.324Z
close_reason: "Markdown guideline pass: +/&->and (fonts/source README, README snippet); 'massive'->'large'; verified no spaced-hyphen dashes in prose; flowmark applied to actively-edited docs."
---
Rigorously apply common-doc-guidelines to all owned Markdown docs: README.md, fonts/source/README.md, docs/development.md, docs/installation.md, docs/publishing.md, docs/terminal-config.md, docs/fonts-build-and-release.md, docs/build-assets.runbook.md, docs/engineering-review.md, docs/specs/*.md, docs/project/specs/active/*.md.

Checks:
- No spaced-hyphen-as-dash (word - word); replace with comma/colon/period or unspaced em dash where truly best.
- Em dashes only when best punctuation, American style (no surrounding spaces).
- Conjunctions: 'and' not + or & in prose (e.g. fonts/source/README.md 'OFL-1.1 + EPL-2.0').
- No extravagant/sweeping language; calibrate confidence.
- Describe present state (no 'previously/removed/renamed' cruft outside review/changelog docs).
- Title Case for H1/H2.
- Consistent list punctuation.
Then run flowmark on every edited Markdown file. Note: em dashes inside code blocks/comments (spec docs) are code and left as-is.
