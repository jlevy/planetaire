---
title: Notable Monospaced Fonts for Coding, Agent Work, and Developer UI
description: Research brief on notable coding monospace fonts, brand usage, popularity signals, licenses, and web compatibility
author: Joshua Levy (github.com/jlevy) with LLM assistance
---
# Research: Notable Monospaced Fonts for Coding, Agent Work, and Developer UI

**Date:** 2026-06-09 (last updated 2026-06-09)

**Author:** Joshua Levy (github.com/jlevy) with LLM assistance

**Status:** Research snapshot

## Overview

This brief catalogs notable monospaced fonts for coding, agent work, developer docs,
terminals, and related UI surfaces.
It records factual research inputs: brand usage, license posture, distribution path,
popularity signals, and typographic relevance.

This document is intentionally not the decision record for comparison-tool membership,
default selections, or future implementation work.
Those product and implementation decisions belong in a separate artifact from this
research snapshot.

## Questions to Answer

1. Which modern monospaced fonts are notable for coding, agent-work, terminal, docs, or
   developer-product typography?
2. What do major AI/developer brands use for monospace or code typography?
3. What web distribution paths, package signals, and ecosystem signals are available?
4. What popularity signals are available, including NPM downloads where useful?
5. Which fonts are free/open, conditionally free, paid, restricted, private, or
   ecosystem layers rather than individual typefaces?

## Scope

Included:

- Publicly available, web-loadable monospace fonts with WOFF2 or Fontsource/npm
  distribution where possible.
- Notable paid, restricted, conditional, and private fonts that affect coding-font
  evaluation or brand typography, even when they are not publicly embeddable.
- Brand mono/code usage for OpenAI, Anthropic, Perplexity, GitHub, Google, Vercel,
  Microsoft, JetBrains, and adjacent developer platforms.
- Popularity proxies from NPM downloads, GitHub prominence, vendor defaults, and
  ecosystem role.
- Suitability for coding, terminal proofs, confusables, ligatures, accessibility, and
  agent/code-review workflows.
- License and availability status for the research set.

Excluded:

- Determining current comparison-tool inclusion, default status, or implementation
  priority.
- Font patching work for icon glyphs.
- Native IDE preference surveys, except where official vendor defaults are relevant.

## Findings

### Brand Usage Survey

Major developer and AI brands increasingly use a brand-specific or system mono for docs
and code UI, rather than a classic public coding font.
OpenAI and Vercel are aligned around Geist Mono, Google Developers uses Google Sans
Code, Anthropic uses a custom `anthropicMono`, and Perplexity API Docs use GT Standard
Mono for code-style text.

| Brand / Surface | Observed Mono or Code Font | Confidence | Notes |
| --- | --- | --- | --- |
| OpenAI Developers | Geist Mono | High | The API reference page defines its mono typography variable with Geist Mono. |
| Anthropic Claude Platform | `anthropicMono` | High | Platform docs CSS defines `--font-anthropic-mono` and maps code-like elements to mono styling. |
| Perplexity API Docs | GT Standard Mono | High | Docs CSS sets `.font-mono` to GT Standard Mono; the shell also includes a JetBrains Mono variable class. |
| GitHub Product UI | `ui-monospace`, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace | High | Primer CSS uses a system mono stack rather than a bundled branded coding font. |
| Google Developers | Google Sans Code | High | Devsite variables set code typography to Google Sans Code. |
| Vercel | Geist Mono | High | Vercel publishes Geist and Geist Mono as web-ready OFL fonts. |
| Microsoft developer tools | Cascadia Code | High | Cascadia Code is bundled with Windows Terminal and is the default in Visual Studio. |
| JetBrains IDEs | JetBrains Mono | High | JetBrains describes JetBrains Mono as the default editor font in its IDEs. |

### Notable Font Landscape

The research set spans classic open-source coding faces, brand/docs-oriented monos,
accessibility-led designs, paid professional coding fonts, system fonts, and terminal
icon ecosystems. The table below records why each item is notable; it does not assign
current comparison-tool status.

| Font / Family | Category | Notability Signal | Availability |
| --- | --- | --- | --- |
| Planetaire Mono | Project font | B612 letters, Hack punctuation, dotted zero; local font under evaluation in this repository. | Free/open |
| B612 Mono | Upstream/source family | Humanist mono source for Planetaire letterforms; originally designed for aircraft cockpit screens. | Free/open |
| Hack | Classic coding font / Nerd Font base | Practical source-code baseline and important input to Nerd Font patched workflows. | Free/open |
| JetBrains Mono | IDE/default coding font | Official JetBrains IDE editor font; strongest NPM signal in this snapshot. | Free/open |
| IBM Plex Mono | Corporate open-source family | High package adoption and broad neutral personality in developer/web contexts. | Free/open |
| Fira Code | Ligature coding font | Canonical programming-ligature face with high awareness and strong package adoption. | Free/open |
| Geist Mono | Brand/docs/product mono | Vercel-published font; observed in OpenAI developer docs typography. | Free/open |
| Source Code Pro | Classic open coding font | Adobe Source family; long-running neutral source-code benchmark. | Free/open |
| Cascadia Code | Terminal/editor default lineage | Microsoft terminal and Visual Studio lineage, with coding-ligature variants. | Free/open |
| Iosevka | Dense configurable coding font | Narrow, highly configurable coding family; useful density and style benchmark. | Free/open |
| Monaspace Neon | GitHub Next coding family | Part of GitHub Next’s Monaspace family with texture-healing ideas. | Free/open |
| Inconsolata | Humanist coding classic | Long-running humanist mono; useful prose/code contrast point. | Free/open |
| PT Mono | Distinct open mono | Upright, serif-like monospace flavor from ParaType/PT family. | Free/open |
| Roboto Mono | Google ecosystem baseline | Google/Android-era monospace baseline with high package adoption. | Free/open |
| Google Sans Code | Google docs/code face | Observed in Google Developers code typography and Gemini-adjacent surfaces. | Free/open |
| Intel One Mono | Accessibility-led coding font | Designed with low-vision legibility and confusables in mind. | Free/open |
| Atkinson Hyperlegible Mono | Accessibility-led coding font | Mono addition to the Braille Institute/Atkinson Hyperlegible lineage. | Free/open |
| Commit Mono | Modern coding font | Neutral programming font with smart kerning and customization options. | Free/open |
| Martian Mono | Devtool/product mono | Variable mono from Evil Martians; useful branded devtool comparison point. | Free/open |
| Recursive | Variable-axis mono/sans system | Variable axes and casual/linear/mono modes are notable for UI experimentation. | Free/open |
| Victor Mono | Characterful coding font | Distinct cursive italic and ligature personality. | Free/open |
| Berkeley Mono | Paid professional coding font | Strong reputation among developers; visible adoption in AI/product-adjacent brands. | Paid commercial plus trial |
| MonoLisa | Paid professional coding font | Known paid coding font with trial, webfont, variable, symbols, and commercial options. | Paid commercial plus limited trial |
| Operator Mono | Paid professional coding font | Influential Hoefler/Monotype coding-font aesthetic. | Paid commercial |
| PragmataPro | Paid dense coding font | Dense programming font with broad symbol coverage and long-running developer following. | Paid commercial |
| GT Standard Mono | Paid brand/product mono | Observed in Perplexity API Docs; part of Grilli Type’s GT Standard family. | Paid commercial plus trial fonts |
| Input Mono | Conditional private-use coding font | Customizable DJR/Font Bureau coding family; private/unpublished use is free. | Free private/unpublished; paid publishing |
| SF Mono | System/developer font | Common Apple-platform mono reference via system/font stacks. | Restricted Apple developer license |
| `anthropicMono` | Private brand font | Observed in Anthropic docs CSS; not publicly distributed as a reusable font. | Private/custom |
| Nerd Fonts | Icon patching ecosystem | Aggregator/patcher layer for many developer fonts and terminal icons, not one typeface. | Mixed, depends on base font and glyph sources |

### License and Availability

Availability matters for downstream use because the same font can be suitable for local
coding but unsuitable for public web embedding, redistribution, or product UI bundling.
This section records observed license posture for the research set.
It is a practical engineering summary, not legal advice.

Free/open fonts in this research set:

| Font | Availability | License | Source / Notes |
| --- | --- | --- | --- |
| Planetaire Mono | Free/open | OFL-1.1 | Final font files are OFL-1.1; upstream components include B612 OFL/EPL context, Hack MIT plus Bitstream Vera, and Nerd Fonts mixed OFL/MIT obligations. |
| B612 Mono | Free/open | OFL-1.1 / EPL upstream context | Planetaire’s local license notes B612 Mono source licensing context. |
| Hack | Free/open | MIT + Bitstream Vera License | Hack’s license chain is MIT plus Bitstream Vera; it is not OFL-only. |
| Fira Code | Free/open | OFL-1.1 | Upstream and Fontsource package metadata both identify OFL-1.1. |
| IBM Plex Mono | Free/open | OFL-1.1 | Includes the reserved font name “Plex”. |
| JetBrains Mono | Free/open | OFL-1.1 | Upstream license file confirms OFL-1.1. |
| Geist Mono | Free/open | OFL-1.1 | Vercel publishes downloadable web formats and states the family is under OFL. |
| Source Code Pro | Free/open | OFL-1.1 | Adobe Source reserved-name and trademark notes apply. |
| PT Mono | Free/open | OFL-1.1 | Google Fonts OFL file includes ParaType/PT reserved names. |
| Inconsolata | Free/open | OFL-1.1 | Google Fonts OFL file. |
| Cascadia Code | Free/open | OFL-1.1 | Includes the reserved font name Cascadia Code. |
| Iosevka | Free/open | OFL-1.1 | Upstream license file confirms OFL-1.1. |
| Monaspace Neon | Free/open | OFL-1.1 | Monaspace and subfamily reserved names apply. |
| Roboto Mono | Free/open | OFL-1.1 | Current googlefonts/RobotoMono license is OFL-1.1; older Roboto references can mention Apache-2.0, so use the mono repo/license file for this candidate. |
| Google Sans Code | Free/open | OFL-1.1 | Upstream googlefonts/googlesans-code license file confirms OFL-1.1; `Google`, `Google Sans`, and `Google Sans Code` are Google trademarks, and upstream states no RFNs are included in the OFL copyright statement. |
| Intel One Mono | Free/open | OFL-1.1 | Includes the reserved font name “Intel”. |
| Atkinson Hyperlegible Mono | Free/open | OFL-1.1 | Google Fonts mono repo license confirms OFL-1.1. |
| Commit Mono | Free/open | OFL-1.1 | Font files are OFL-1.1; website/source code is MIT. |
| Martian Mono | Free/open | OFL-1.1 | Upstream Evil Martians repo license confirms OFL-1.1. |
| Recursive | Free/open | OFL-1.1 | Fontsource package metadata identifies OFL-1.1. |
| Victor Mono | Free/open | OFL-1.1 | Fontsource package metadata identifies OFL-1.1. |

Paid, restricted, private, and conditional fonts:

| Font | Availability | License Posture | Notability Signal |
| --- | --- | --- | --- |
| Berkeley Mono | Paid commercial plus trial | U.S. Graphics says the Developer license is for personal use and does not cover commercial use; commercial plans are sold by company size and are restricted for some app categories. | Strong paid coding reference with visible developer and AI/product adoption. |
| MonoLisa | Paid commercial plus limited trial | Purchase/EULA required; the site lists commercial-use features, webfont/variable options, an Indie license tier, and a free limited trial. | Known paid coding font with practical webfont and variable-font options. |
| Operator Mono | Paid commercial | Hoefler/Monotype retail font; needs vendor license review before any use beyond personal/local testing. | Influential historical coding-font aesthetic. |
| PragmataPro | Paid commercial | Purchase required; optional premium features. | Dense, symbol-heavy paid programming font with long-running developer following. |
| GT Standard Mono | Paid commercial plus trial fonts | Grilli Type sells GT Standard and offers free trial fonts. | Perplexity docs use GT Standard Mono, making it a useful brand/reference mono. |
| Input Mono | Free private/unpublished; paid publishing | DJR states Input is free for private/unpublished use, while public-facing usage such as websites or print requires Type Network licensing. | Strong customizable coding font system with many style and glyph defaults. |
| SF Mono | Restricted system/developer license | Apple’s license limits the San Francisco font to mockups for Apple-platform software and forbids broader embedding/redistribution. | Important macOS/iOS developer reference, but not safely embeddable. |
| `anthropicMono` | Private/custom | Observed in Anthropic docs CSS; no public reusable license found. | Brand reference only. |

### Popularity Signals

NPM downloads are helpful for web-compatible distribution, especially Fontsource
packages, but they are not the same as IDE/editor preference.
They overrepresent fonts commonly bundled into web apps and underrepresent fonts
installed through OS packages, IDE defaults, GitHub releases, Homebrew, or direct zip
downloads.

Snapshot from the NPM downloads API, `last-month` window 2026-05-04 through 2026-06-02:

| Package | Font | Downloads |
| --- | --- | ---: |
| `@fontsource/jetbrains-mono` | JetBrains Mono | 1,627,414 |
| `@fontsource/ibm-plex-mono` | IBM Plex Mono | 1,168,591 |
| `@fontsource/roboto-mono` | Roboto Mono | 556,697 |
| `@fontsource/fira-code` | Fira Code | 418,992 |
| `@fontsource/geist-mono` | Geist Mono | 404,907 |
| `@fontsource/source-code-pro` | Source Code Pro | 250,853 |
| `@fontsource/inconsolata` | Inconsolata | 98,216 |
| `@fontsource/pt-mono` | PT Mono | 43,044 |
| `@fontsource/commit-mono` | Commit Mono | 29,859 |
| `@fontsource/cascadia-code` | Cascadia Code | 23,478 |
| `@fontsource/recursive` | Recursive | 19,314 |
| `hack-font` | Hack | 11,080 |
| `@fontsource/iosevka` | Iosevka | 11,044 |
| `@fontsource/atkinson-hyperlegible-mono` | Atkinson Hyperlegible Mono | 9,426 |
| `@fontsource/monaspace-neon` | Monaspace Neon | 7,422 |
| `@fontsource/intel-one-mono` | Intel One Mono | 5,823 |
| `@fontsource/google-sans-code` | Google Sans Code | 5,108 |
| `@fontsource/martian-mono` | Martian Mono | 2,612 |
| `@azurity/pure-nerd-font` | Nerd Font package proxy | 1,698 |
| `nerd-fonts-woff2` | Nerd Font package proxy | 586 |

Nerd Fonts is better understood as an ecosystem layer than a single font candidate.
Its official site positions it as an aggregator and patcher for developer-targeted
fonts, adding glyphs from icon sets such as Font Awesome, Devicons, Octicons, Codicons,
Material Design Icons, Font Logos, and Powerline symbol sets.
NPM package downloads are a weak proxy here because most Nerd Font use comes through
direct downloads, Homebrew, Linux packages, editor/terminal setup guides, or patched
font releases rather than one canonical NPM package.

### Nerd Fonts Ecosystem Signals

Nerd Fonts is not a typeface.
It is a distribution and patching ecosystem, and Nerd Font availability is a feature of
individual base fonts.
That makes it useful in two ways:

1. It surfaces which developer fonts are actively packaged for terminal/icon workflows.
2. It provides ecosystem metrics that complement NPM downloads and brand usage.

Snapshot from the official Nerd Fonts site and GitHub repository, checked 2026-06-09:

| Metric | Value |
| --- | --- |
| Project role | Iconic font aggregator, glyph/icon collection, and font patcher |
| Icon coverage claim | 10,390+ icons |
| Patched programming fonts claim | 68+ patched and ready-to-use programming fonts |
| Current patcher/release line | v3.4.0 |
| GitHub stars | 63.3k |
| GitHub forks | 3.9k |
| GitHub watchers | 402 |
| GitHub releases | 38 |
| Latest GitHub release observed | v3.4.0, 2025-04-24 |

Research-set fonts with official Nerd Fonts patched distributions:

| Base Font in Research Set | Nerd Fonts Distribution Name | Nerd Fonts Version / Notes |
| --- | --- | --- |
| Hack | Hack | 3.003 |
| Fira Code | FiraCode | 6.2 |
| IBM Plex Mono | BlexMono | 2.004 (6.4.0); renamed because IBM Plex Mono is a reserved font name. |
| JetBrains Mono | JetBrainsMono | 2.304 |
| Geist Mono | GeistMono | 1.401 |
| Source Code Pro | SauceCodePro | 2.042; renamed because Adobe Source reserved-name/trademark terms apply. |
| Inconsolata | Inconsolata | 3.000; InconsolataGo and Inconsolata LGC are also present. |
| Cascadia Code | CaskaydiaCove | 2407.24; CaskaydiaMono covers Cascadia Mono without ligatures. |
| Iosevka | Iosevka | 33.2.1 patched-source version; IosevkaTerm and IosevkaTermSlab are also present. |
| Monaspace | Monaspice | 1.200 patched-source version; Nerd Fonts distribution covers Monaspace under the Monaspice name. |
| Roboto Mono | RobotoMono | 3.0 |
| Intel One Mono | IntoneMono | 1.4.0; renamed because Intel One Mono is a reserved font name. |
| Atkinson Hyperlegible Mono | AtkynsonMono | 2.001; renamed because Atkinson Hyperlegible Mono is a reserved font name. |
| Commit Mono | CommitMono | 1.143 |
| Martian Mono | MartianMono | 1.1.0 |
| Recursive Mono | RecMono | 1.085 |
| Victor Mono | VictorMono | 1.5.6 |

Research-set fonts not observed in the Nerd Fonts downloads list:

| Font | Note |
| --- | --- |
| Planetaire Mono | Project font; can be patched locally if needed. |
| B612 Mono | Source lineage for Planetaire, not observed as an official Nerd Fonts download. |
| PT Mono | Not observed as an official Nerd Fonts download. |
| Google Sans Code | Not observed as an official Nerd Fonts download. |
| Berkeley Mono | Paid font; Nerd Fonts README lists proprietary/commercial fonts separately as good fonts to patch, not included distributions. |
| MonoLisa | Paid font; not observed as an official Nerd Fonts download. |
| Operator Mono | Paid font; Nerd Fonts README lists it among commercial/proprietary fonts that could benefit from patching but are not included. |
| PragmataPro | Paid font; Nerd Fonts README lists it among commercial/proprietary fonts that could benefit from patching but are not included. |
| GT Standard Mono | Paid font; not observed as an official Nerd Fonts download. |
| Input Mono | Conditional private-use font; Nerd Fonts README lists it among fonts that could benefit from patching but are not included. |
| SF Mono | Restricted Apple font; Nerd Fonts README lists it among fonts that could benefit from patching but are not included. |
| `anthropicMono` | Private/custom brand font; not observed as an official Nerd Fonts download. |

Additional Nerd Fonts-distributed fonts that may be worth tracking as ecosystem-derived
candidates:

| Font | Nerd Fonts Signal |
| --- | --- |
| 0xProto | Programming font focused on source-code legibility; Nerd Fonts version 2.300. |
| Adwaita Mono | GNOME monospace typeface; Nerd Fonts version 32.4. |
| MesloLG | Customized Menlo-derived terminal font with slashed zeros; Nerd Fonts version 1.21. |
| Monoid | Ligatures, distinguishable glyphs, large operators and punctuation; Nerd Fonts version 0.61. |
| Mononoki | Designed around character differentiation and resolution sizes; Nerd Fonts version 1.6. |
| Space Mono | Squarish character lines and dotted zero; Nerd Fonts version 1.001. |
| Fantasque Sans Mono | Handwriting-like character; Nerd Fonts version 1.8.0. |
| Departure Mono | Pixel-style monospaced font; Nerd Fonts version 1.422. |
| Zed Mono | Rounded Iosevka-derived font from Zed; Nerd Fonts version 1.2.0. |

### Tracking Categories

The research set uses these factual categories so implementation-specific status can be
decided elsewhere:

| Category | Meaning |
| --- | --- |
| Free/open | Font can be studied, embedded, redistributed, or bundled under an open license, subject to the exact license terms and reserved-name rules. |
| Paid commercial | Font requires purchase or vendor licensing for normal professional, product, or public-facing use. |
| Conditional | Font has a limited free use case, such as private or unpublished local use, plus paid terms for publishing or commercial use. |
| Restricted system/developer | Font is available in a platform or developer context but has license restrictions that limit embedding, redistribution, or general website use. |
| Private/custom | Font is observed in a product or brand surface but no public reusable license was found. |
| Ecosystem layer | Item is not a single typeface; it changes, patches, aggregates, or distributes multiple fonts. |

## Key Insights

1. Brand usage and coding-font popularity point in different directions.
   The high-visibility AI/developer docs surfaces often use custom or brand-adjacent
   monos, while package popularity favors broad open-source families like JetBrains
   Mono, IBM Plex Mono, Roboto Mono, Fira Code, and Geist Mono.
2. Agent-work typography evaluation depends heavily on dense scanning, unambiguous
   glyphs, and low-friction web loading.
   Ligatures are a notable feature axis, but not the only useful signal.
3. Accessibility-led monos are a distinct part of the landscape.
   Intel One Mono and Atkinson Hyperlegible Mono are not the top NPM packages, but they
   directly address confusability and low-vision readability concerns.
4. Nerd Fonts is a separate axis from base typeface selection.
   For terminal and agent tool UIs, patched icons matter, but they can obscure the
   underlying type design question when treated as the same kind of candidate.

## Use of This Brief

This brief is a factual input for later product and implementation decisions.
Downstream comparison-tool data can reference these fields; current inclusion, default
status, loading behavior, and prioritization belong in a separate decision record or
source file.

## Maintenance Notes

- NPM download counts are a dated snapshot; keep the API window with each update.
- Brand usage evidence retains the inspected surface and confidence level.
- Nerd Fonts metrics are ecosystem-level metrics, while Nerd Font availability is a
  per-font feature.
- License posture comes from upstream license files or vendor EULAs when a font becomes
  relevant to embedding, redistribution, or public publishing.
- New notable fonts can be added by extending the landscape and license tables without
  assigning comparison-tool status in this document.

## Methodology

Research was conducted on 2026-06-09 using official/vendor pages, live page CSS
inspection for brand docs, the GitHub Primer CSS source, Fontsource CDN URL checks, and
NPM downloads API queries.
License research used upstream license files, NPM package license metadata, and vendor
purchase/license pages.
Nerd Fonts ecosystem metrics used the official Nerd Fonts site, downloads page, and
GitHub repository metadata.
The NPM snapshot used `https://api.npmjs.org/downloads/point/last-month/<package>` for
each candidate package.
The downloads window returned by the API was 2026-05-04 through 2026-06-02.

Brand usage findings are marked high confidence when confirmed from live CSS or official
repository source. Popularity findings are lower-confidence as a measure of human
preference because package downloads are affected by build pipelines, caching, and
transitive usage.

## References

- [OpenAI API Reference](https://developers.openai.com/api/reference/overview)
- [Anthropic Claude Platform Docs](https://platform.claude.com/docs/en/intro)
- [Perplexity API Docs](https://docs.perplexity.ai/docs/getting-started/overview)
- [Primer CSS typography variables](https://github.com/primer/css/blob/163a19f3e8afa29e2ffc3e688b5ac17b2717fbdb/src/support/variables/typography.scss)
- [Google Developers](https://developers.google.com/)
- [Vercel Geist](https://vercel.com/font)
- [Planetaire license](../../../LICENSE)
- [B612](https://github.com/polarsys/b612)
- [JetBrains Mono](https://www.jetbrains.com/lp/mono/)
- [Fira Code](https://github.com/tonsky/FiraCode)
- [Fira Code license](https://github.com/tonsky/FiraCode/blob/master/LICENSE)
- [IBM Plex license](https://github.com/IBM/plex/blob/master/LICENSE.txt)
- [JetBrains Mono OFL](https://github.com/JetBrains/JetBrainsMono/blob/master/OFL.txt)
- [Hack license](https://github.com/source-foundry/Hack/blob/master/LICENSE.md)
- [Monaspace](https://monaspace.githubnext.com/)
- [Monaspace license](https://github.com/githubnext/monaspace/blob/main/LICENSE)
- [Iosevka license](https://github.com/be5invis/Iosevka/blob/main/LICENSE.md)
- [Intel One Mono](https://github.com/intel/intel-one-mono)
- [Intel One Mono OFL](https://github.com/intel/intel-one-mono/blob/main/OFL.txt)
- [Source Code Pro](https://github.com/adobe-fonts/source-code-pro)
- [Source Code Pro license](https://github.com/adobe-fonts/source-code-pro/blob/release/LICENSE.md)
- [Cascadia Code](https://github.com/microsoft/cascadia-code)
- [Cascadia Code license](https://github.com/microsoft/cascadia-code/blob/main/LICENSE)
- [Atkinson Hyperlegible Font](https://www.brailleinstitute.org/freefont/)
- [Atkinson Hyperlegible Mono OFL](https://github.com/googlefonts/atkinson-hyperlegible-next-mono/blob/main/OFL.txt)
- [Commit Mono](https://commitmono.com/)
- [Commit Mono licenses](https://github.com/eigilnikolajsen/commit-mono)
- [Martian Mono](https://evilmartians.com/products/martian-mono)
- [Martian Mono OFL](https://github.com/evilmartians/mono/blob/main/OFL.txt)
- [Google Sans Code OFL](https://github.com/googlefonts/googlesans-code/blob/main/OFL.txt)
- [Roboto Mono OFL](https://github.com/googlefonts/RobotoMono/blob/main/OFL.txt)
- [PT Mono OFL](https://github.com/google/fonts/blob/main/ofl/ptmono/OFL.txt)
- [Inconsolata OFL](https://github.com/google/fonts/blob/main/ofl/inconsolata/OFL.txt)
- [Vercel Geist](https://vercel.com/font)
- [Recursive](https://github.com/arrowtype/recursive)
- [Victor Mono](https://github.com/rubjo/victor-mono)
- [Berkeley Mono](https://usgraphics.com/products/berkeley-mono)
- [MonoLisa](https://www.monolisa.dev/)
- [Operator Mono](https://www.typography.com/fonts/operator/overview)
- [PragmataPro](https://fsd.it/shop/fonts/pragmatapro/)
- [GT Standard](https://www.grillitype.com/typeface/gt-standard)
- [Input Mono](https://input.djr.com/download/)
- [Apple Fonts license](https://developer.apple.com/fonts/)
- [Nerd Fonts](https://www.nerdfonts.com/)
- [Nerd Fonts downloads](https://www.nerdfonts.com/font-downloads)
- [Nerd Fonts GitHub repository](https://github.com/ryanoasis/nerd-fonts)
- [NPM downloads API](https://github.com/npm/registry/blob/main/docs/download-counts.md)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
