---
title: Recommendations for Monospace Font Tracking and Comparison
description: Decision-oriented recommendations derived from the 2026-06-09 monospace font research snapshot
author: Joshua Levy (github.com/jlevy) with LLM assistance
---
# Recommendations: Monospace Font Tracking and Comparison

**Date:** 2026-06-09

**Author:** Joshua Levy (github.com/jlevy) with LLM assistance

**Status:** Proposed recommendation

## Source Research

This recommendation document depends on the factual research snapshot in
[research-2026-06-09-monospace-coding-fonts.md](./research-2026-06-09-monospace-coding-fonts.md).

The research doc should remain a catalog of facts: notable fonts, brand usage,
distribution paths, popularity signals, licenses, and availability.
This document is the place for interpretation, prioritization, and current comparison
tool choices.

## Recommendation Summary

Use a two-layer model:

1. Keep the research brief broad and neutral.
2. Keep comparison-tool status in maintainable data, with explicit buckets for loaded
   fonts, default-visible fonts, and reference-only tracked fonts.

For the public web comparison tool, load only fonts that are free/open or already
licensed for the project.
Paid, restricted, private, and conditionally free fonts should be tracked as references
without `@font-face` URLs unless a suitable license is obtained and recorded.
Use six default-visible fonts so the first screen stays focused while covering the
project font, lineage baseline, ligatures, open-source popularity, IDE defaults, and
modern AI/developer-docs typography.

## Recommended Current Buckets

### Default Visible Set

These should be the first fonts users see when opening the comparison tool:

| Font | Reason |
| --- | --- |
| Planetaire Mono | The project font under evaluation. |
| Hack | Directly relevant to Planetaire’s punctuation and Nerd Font lineage. |
| Fira Code | Canonical programming-ligature comparison point. |
| IBM Plex Mono | High-adoption neutral open-source mono. |
| JetBrains Mono | Strongest current developer/package adoption signal and IDE-default reference. |
| Geist Mono | OpenAI/Vercel-adjacent modern developer-docs and product UI face. |

### Selectable Loaded Set

These should remain available in the broader selector because they provide useful
coverage across brand usage, defaults, accessibility, density, and style:

| Font | Role |
| --- | --- |
| Source Code Pro | Adobe/open-source coding classic. |
| PT Mono | Distinct upright, serif-like mono flavor. |
| Inconsolata | Humanist coding classic. |
| Cascadia Code | Microsoft terminal/editor lineage. |
| Iosevka | Narrow, configurable density benchmark. |
| Monaspace Neon | GitHub Next texture-healing family reference. |
| Roboto Mono | Google ecosystem baseline with high web package usage. |
| Google Sans Code | Google Developers and Gemini-adjacent code face. |
| Intel One Mono | Low-vision-informed coding font. |
| Atkinson Hyperlegible Mono | Accessibility-led mono reference. |
| Commit Mono | Modern neutral programming font with smart kerning. |
| Martian Mono | Variable mono useful for branded devtool comparison. |

### Reference-Only Tracking

These are notable enough to track, but should not be loaded into the public comparator
by default:

| Font / Family | Tracking Reason | Current Handling |
| --- | --- | --- |
| Berkeley Mono | High-quality paid professional coding font with visible developer and AI/product adoption. | Paid reference only. |
| MonoLisa | Well-known paid coding font with trial, webfont, variable, and commercial options. | Paid reference only. |
| Operator Mono | Influential paid coding-font aesthetic. | Paid reference only. |
| PragmataPro | Dense paid coding font with broad symbol coverage. | Paid reference only. |
| GT Standard Mono | Perplexity docs use GT Standard Mono. | Paid brand/reference only. |
| Input Mono | Strong customizable coding family with private-use download and paid publishing terms. | Conditional reference only. |
| SF Mono | Important Apple-platform system mono, but license-restricted. | Restricted system reference only. |
| `anthropicMono` | Anthropic docs brand mono with no public reusable license found. | Private brand reference only. |
| Recursive | Interesting free/open variable-axis system. | Track until axis choices are deliberate. |
| Victor Mono | Distinct cursive italic and ligature personality. | Track as lower-priority free/open comparison candidate. |
| B612 Mono | Upstream/source family for Planetaire letterforms. | Track as source lineage; add only if direct upstream comparison becomes useful. |
| Nerd Fonts | Terminal icon ecosystem rather than one typeface. | Track as ecosystem metadata and per-font icon distribution status, not as a font candidate. |

## Data Model Guidance

Keep `site/compare-fonts.js` as the browser-loadable source of truth for comparison-tool
font status. Each font entry should carry:

- Stable `id`, display `name`, CSS `family`, and source kind.
- Upstream `sourceUrl` for every loaded and reference-only font.
- Web font faces only when the project can legally load them.
- `default` only for the initial visible set.
- `npmPackage` and dated download snapshot when available.
- `brandRefs` and `notes` when useful.
- `availability` and `license` metadata for all loaded fonts.
- `nerdFont` metadata when a font has an official Nerd Fonts patched distribution,
  including Nerd Fonts family name, version, and reserved-name notes.

Keep reference-only entries in a separate collection, not mixed with loaded `@font-face`
entries. That makes paid or private fonts visible to future research and UI work without
accidentally embedding them.

Keep Nerd Fonts project metrics in ecosystem-level metadata, separate from font entries.
Useful fields include patched-font count, icon count, release line, GitHub stars/forks,
and the date the snapshot was checked.
Use those metrics as a support/popularity signal for terminal workflows, not as proof of
base typeface quality.

## UI Guidance

The next useful UI improvement is grouping/filtering, not adding more fonts
indiscriminately. Recommended groups:

- Popular/default
- Brand/docs
- Classic coding
- Accessibility
- Dense/compact
- Ligature-oriented
- Terminal/ecosystem
- Reference-only

The reference-only group should display metadata and license posture, but it should not
render live proofs unless a local licensed font is intentionally selected or uploaded in
a future workflow.

For the terminal/ecosystem group, expose Nerd Fonts as a capability badge on individual
fonts, for example “Nerd Fonts: FiraCode 6.2” or “Nerd Fonts: CaskaydiaCove 2407.24”. Do
not make “Nerd Fonts” itself selectable as a font unless the future UI is explicitly
rendering the symbols-only fallback font or an uploaded patched font file.

## Refresh Cadence

Refresh the NPM download snapshot when the comparison list changes materially or before
publishing a new public release.
Keep the API window beside the numbers so old rankings do not look current.

Review paid/restricted license posture before any implementation change that would load,
bundle, redistribute, or publicly display the font files.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
