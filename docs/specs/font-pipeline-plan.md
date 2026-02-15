# Feature: Planetaire Mono Font Pipeline

**Date:** 2026-02-15

**Author:** jlevy

**Status:** Draft

## Overview

Planetaire Mono is a high-quality monospace font for terminals and code editors, derived
from the B612 Mono typeface (originally designed for aircraft cockpit displays by Airbus,
optimized for legibility). The name "Planetaire" is a nod to the novel *The Little Prince*
by Antoine de Saint-Exupery, in which the little prince lives on asteroid B-612.

This project packages:
1. The **original source fonts** (B612 Mono Liga Nerd Font from the carlosedp fork, plus
   Hack Nerd Font for fallback glyphs).
2. The **font modification scripts** that transform and improve these fonts.
3. A **CLI tool** (`planetaire`) that runs the full transformation pipeline to produce
   Planetaire Mono in all weights.

## Goals

- Produce a single, self-contained Planetaire Mono font family with all needed glyphs
  (letters, figures, punctuation, Nerd Font icons) — no CSS fallback chain required.
- Provide Regular (400), Bold (700), ExtraBold (800) weights, each with italic variants.
- Fix known issues in B612 (uneven special characters) by compositing the best glyphs
  from B612 and Hack.
- Leverage B612's built-in dotted zero (default) with optional slashed zero via OpenType
  `'zero'` feature.
- Create a clean, repeatable pipeline: original fonts in, Planetaire Mono out.
- Publish the tool as a Python CLI package via PyPI so others can reproduce the build.

## Non-Goals

- Creating an entirely new typeface from scratch.
- Supporting variable/OpenType font features beyond what the sources provide.
- Modifying the Hack Nerd Font itself (used only as a glyph donor).

---

## Background

### The B612 Typeface

B612 is an open-source font family designed for aircraft cockpit displays. It was developed
by Airbus in collaboration with ENAC and Universite de Toulouse III, with design by
Intactile DESIGN. Released under the Eclipse Public License v2.0, Eclipse Distribution
License v1.0, and SIL Open Font License v1.1.

Key properties:
- Maximizes distance between character forms for disambiguation
- Respects letter primitives for readability
- Harmonizes forms and spacing
- Completely hinted for all characters
- UPM: 2000

B612 is exceptionally legible at small sizes and in adverse conditions, making it ideal
for terminal use.

### The carlosedp/b612 Fork

The fonts used as input come from
[carlosedp/b612](https://github.com/carlosedp/b612), a fork that adds:

1. **Dotted zero** (default), with OpenType features for alternatives:
   - `'zero'` — slashed zero
   - `'ezer'` — empty zero (original B612 style)
   - These were edited in FontLab from VFB sources.
2. **Ligatures** from FiraCode, applied via the
   [Ligaturizer](https://github.com/ToxicFrog/Ligaturizer) tool using FontForge.
3. **Nerd Font patching** (powerline symbols, devicons, etc.) via the
   [Nerd Fonts Docker patcher](https://github.com/ryanoasis/nerd-fonts/).
4. **Digital signature fix** using `gftools fix-nonhinting` (fixes DSIG, GASP, and PREP
   tables).

The fork provides fonts in several directories:
- `fonts/original/` — unmodified B612 (empty zero, no ligatures, no Nerd Fonts)
- `fonts/plain/` — B612 with dotted/slashed zero only (no ligatures, no Nerd Fonts)
- `fonts/ligatures/` — B612 with zero fixes + ligatures (no Nerd Fonts)
- `fonts/ligatures_nerd/` — B612 with zero fixes + ligatures + Nerd Font glyphs

The resulting font family is named **B612MonoLigaNerdFont** and provides four base
variants: Regular, Bold, Italic, BoldItalic.

**Source repo:** Checked out at `attic/b612-carlosedp/`

### The Hack Nerd Font

[Hack](https://github.com/source-foundry/Hack) is a typeface designed for source code,
based on Bitstream Vera Sans Mono / DejaVu Sans Mono. It has clean, consistent
punctuation and excellent glyph coverage.

[Nerd Fonts](https://github.com/ryanoasis/nerd-fonts) patches Hack with additional glyphs
(powerline, Font Awesome, devicons, etc.).

Key properties:
- UPM: 2048 (note: differs from B612's 2000 — merging will require UPM normalization)
- Licensed under MIT (Hack) + Bitstream Vera License (upstream)
- Nerd Fonts patched versions are under MIT + SIL OFL

**Source repos:** Checked out at `attic/hack-source/` and `attic/nerd-fonts/`

### The Nerd Fonts Patcher

The [Nerd Fonts patcher](https://github.com/ryanoasis/nerd-fonts) (`font-patcher`) is a
2,374-line Python script that uses FontForge to inject symbol glyphs into any font. It is
the standard tool used by both carlosedp and the Nerd Fonts project itself.

**Core algorithm (the `copy_glyphs()` method, ~500 lines):**
1. For each glyph in a symbol font range:
   - Determine the target Unicode codepoint (exact or remapped)
   - Copy the glyph outline from symbol font to target font (FontForge copy/paste)
   - Scale the glyph to fit the target font's cell dimensions
   - Position/align the glyph (left/center/right, vertical centering)
   - Set advance width (monospace or proportional)

**Glyph sources** (11+ symbol font families in `src/glyphs/`):

| Source | Unicode Range | Description |
|--------|---------------|-------------|
| Seti-UI + Custom | U+E4FA-E5FF | Dev file type icons |
| Devicons | U+E600-E7EF | Programming language icons |
| Powerline | U+E0A0-E0D7 | Terminal separator arrows |
| Font Awesome | U+ED00-F2FF | 1000+ general icons |
| Font Awesome Ext | U+E000-E0A9 | Extended FA icons |
| Material Design | U+F0001-F1AF0 | Material icons (massive set) |
| Weather Icons | U+F000-F0EB | Weather symbols |
| Octicons | U+F000-F306 | GitHub icons |
| Codicons | U+EA60-EC1E | VS Code icons |
| Font Logos | U+F300-F381 | Brand/company logos |
| Pomicons | U+E000-E00A | Pomodoro icons |
| Box Drawing | U+2500-259F | Unicode box drawing |
| Braille | U+2800-28FF | Braille patterns (generated) |

**Scaling system:** Supports multiple stretch modes — `'pa'` (preserve aspect ratio),
`'xy'` (independent scaling), `'^'` (fill cell height), `'2'` (double-width). Each glyph
set has configured stretch, alignment, and overlap parameters.

**Mono vs. non-Mono:** The `--mono` flag forces all glyphs to single-cell width. Without
it (`HackNerdFont` vs `HackNerdFontMono`), glyphs can be double-width for better
rendering of icons.

**Key FontForge APIs used:** `font.copy()`/`font.paste()` for outline transfer,
`glyph.transform(psMat.scale/translate)` for geometry, `glyph.boundingBox()` for
measurement, `font.generate()` for output.

**Complexity assessment for porting to fontTools:**
- Glyph outline copying: feasible via fontTools pens (~80% straightforward)
- Scaling/positioning: feasible via `fontTools.misc.transform` matrices
- Font encoding/cmap manipulation: more cumbersome than FontForge's selection API
- Estimated effort: ~500-800 LOC, 2-3 weeks for a clean port
- **However:** Not necessary for Planetaire (see Approach Evaluation below)

### Prior Work in the Kerm Repository

All prior font work was done inside the [kerm](https://github.com/jlevy/kerm) terminal
emulator project. The relevant artifacts are archived in `attic/kerm/` within this
repository.

---

## Reconstruction of All Prior Changes

### Step 1: Source Font Acquisition

Two font families were obtained for use in kerm.

**B612MonoLigaNerdFont** — An older build from the carlosedp fork (NOT the current version
in the repo):

| File | Size | Glyphs | Version | Weight |
|------|------|--------|---------|--------|
| `B612MonoLigaNerdFont-Regular.ttf` | 1.9 MB | 5,144 | 1.010; ttfautohint v1.8.4 | 400 |
| `B612MonoLigaNerdFont-Bold.ttf` | 1.9 MB | 5,144 | 1.010 | 700 |
| `B612MonoLigaNerdFont-Italic.ttf` | 1.9 MB | 5,144 | 1.010 | 400 |
| `B612MonoLigaNerdFont-BoldIta.ttf` | 1.9 MB | 5,144 | 1.010 | 700 |

**HackNerdFont** (non-Mono variant, for wider double-width Nerd Font glyphs):

| File | Size | Glyphs | Version | Weight |
|------|------|--------|---------|--------|
| `HackNerdFont-Regular.ttf` | 2.5 MB | 11,957 | 3.003; Nerd Fonts 3.3.0 | 400 |
| `HackNerdFont-Bold.ttf` | 2.6 MB | 11,957 | 3.003 | 700 |
| `HackNerdFont-Italic.ttf` | 2.6 MB | 11,957 | 3.003 | 400 |
| `HackNerdFont-BoldItalic.ttf` | 2.6 MB | 11,957 | 3.003 | 700 |

**Key discrepancy discovered:** The kerm fonts differ significantly from the current
carlosedp repo:

| Property | Kerm version | Current carlosedp repo |
|----------|-------------|----------------------|
| Version | 1.010; ttfautohint v1.8.4 | 1.009; Nerd Fonts 3.4.0 |
| Glyphs | 5,144 | 11,357 |
| Size | ~1.9 MB | ~2.5 MB |
| Family name | `B612Mono Liga NerdFont` | `B612MonoLiga Nerd Font` |
| Has DSIG | Yes | No |
| Has PfEd | No | Yes |

The kerm version appears to be from an earlier Nerd Fonts patcher run (fewer glyphs,
different naming convention). The current carlosedp repo has substantially more glyphs
from Nerd Fonts 3.4.0.

**Decision needed:** For Planetaire, we should use the latest carlosedp fonts
(`fonts/ligatures_nerd/`) as the B612 source, not the older kerm versions.

### Step 2: ExtraBold Weight Generation

**Script:** `attic/kerm/bin/embolden_font.py`
**Tool:** FontForge (run as `fontforge -script embolden_font.py <input.ttf>`)

**Process:**
1. Opens a Bold (weight 700) TTF font.
2. Iterates over all glyphs and applies `glyph.changeWeight()` to increase stroke
   thickness by a configurable number of units.
3. Selective glyph processing:
   - **Skip entirely:** `fae-gut`, `dev-ohmyzsh`, `uniE24B` (these glyphs would break
     or look wrong if emboldened).
   - **Half-weight:** `dev-babel`, `dev-postcss` (lighter emboldening to preserve detail).
   - **Full weight:** All other glyphs.
4. Updates font metadata: `os2_weight`, `fontname`, `fullname`, `familyname`, weight
   string.
5. Generates an unhinted TTF.
6. Runs `ttfautohint` on the output for screen rendering.
7. Removes the intermediate unhinted file.

**Configuration used for B612:**
```python
WEIGHT_CLASSES = [800]                       # ExtraBold only (not Black/900)
WEIGHT_CHANGES = {800: 30, 900: 45}          # 30 units for ExtraBold
BOLD_SUFFIXES = ["Bold", "BoldItalic", "BoldIta"]
```

**Output files generated:**

| File | Size | Weight | Style |
|------|------|--------|-------|
| `B612MonoLigaNerdFont-ExtraBold.ttf` | 2.0 MB | 800 | Normal |
| `B612MonoLigaNerdFont-ExtraBoldItalic.ttf` | 2.0 MB | 800 | Italic |

The same process was applied to Hack Nerd Font Bold variants to produce
`HackNerdFont-ExtraBold.ttf` (4.3 MB) and `HackNerdFont-ExtraBoldItalic.ttf` (4.3 MB).

### Step 3: CSS-Level Font Compositing

**File:** `attic/kerm/lib/utils/fonts.ts`

Rather than merging fonts at the binary level, kerm used a **CSS unicode-range fallback
strategy**:

1. **B612MonoLigaNerdFont** loaded with restricted `unicode-range` (letters and numbers
   only).
2. **Hack Nerd Font** loaded as full fallback with no unicode-range restriction.

**Why:**
- B612 has the most legible and aesthetically pleasing letterforms and figures.
- B612's punctuation and special characters were found to be inconsistent — uneven sizing
  and visual weight.
- Hack provides cleaner punctuation and comprehensive glyph coverage.

**Limitation:** CSS-level compositing only works in browser/Electron contexts. Does not
work in native terminals, IDEs, or general distribution.

### Step 4: Zero Glyph

The original B612 zero (`0`) is ambiguous — it lacks a dot or slash to distinguish it
from uppercase `O`.

**Resolution:** The carlosedp fork already fixes this:
- **Default:** Dotted zero (center dot inside the zero)
- **`'zero'` OpenType feature:** Slashed zero alternative
- **`'ezer'` OpenType feature:** Empty zero (original B612 style)

The kerm fonts in `attic/kerm/assets/fonts/` include these OpenType features (confirmed
via fontTools inspection: GSUB features include `calt`, `ezer`, `zero`).

For Planetaire, we will preserve these OpenType features so users can choose their
preferred zero style.

### Step 5: Font Configuration in Kerm

**File:** `attic/kerm/app/config/config-default.json`

```json
{
  "fontSize": 12,
  "fontFamily": "\"B612Mono Liga NerdFont\", \"Hack Nerd Font\", Menlo, ...",
  "fontWeight": "400",
  "fontWeightBold": "800"
}
```

Notable: Bold text uses weight **800** (ExtraBold), not 700 (Bold). This was deliberate —
at small sizes, standard Bold was not visually distinct enough from Regular.

### Step 6: Font Experimentation Timeline

Several font families were evaluated before settling on B612 + Hack:

| Date | Commit | Description |
|------|--------|-------------|
| 2025-01-13 | `e0ced10b` | `embolden_font.py` created; Hack ExtraBold generated |
| 2025-01-13 | `68a38693` | Extended to Monaspace Ne ExtraBold |
| 2025-01-13 | `8c72d3a8` | Added B612MonoLigaNerdFont (all 6 variants) |
| 2025-01-14 | `bea2cfc1` | B612 for letters + Monaspace for rest |
| 2025-01-14 | `f2a13c27` | Switched fallback from Monaspace to Hack |
| 2025-01-23 | `63125cfd` | Switched to non-Mono Hack variant (wider Nerd glyphs) |

Other fonts evaluated (in `attic/kerm/assets-extras/fonts/`): GoMono, iMWriting Mono,
RecMonoLinear, Monaspace Ne/Xe.

### Supporting Scripts

| Script | Purpose | Needed for Planetaire? |
|--------|---------|----------------------|
| `attic/kerm/bin/embolden_font.py` | Generate heavier weights via FontForge | Yes — port to module |
| `attic/kerm/bin/dump_font_metadata.py` | Inspect font metadata via FontForge | Yes — rewrite with fontTools |
| `attic/kerm/bin/otf_to_ttf.py` | OTF-to-TTF conversion via FontForge | No — sources are TTF |
| `attic/kerm/bin/decode_mac_xattrs.py` | macOS xattr inspection | No |

---

## Source Font Provenance

### B612MonoLigaNerdFont Build Chain

The B612MonoLigaNerdFont files are produced by a multi-step process documented in the
carlosedp fork README:

```
Original B612Mono (polarsys/b612)
  │  Copyright (c) 2012 AIRBUS
  │  License: EPL-2.0 + EDL-1.0 + OFL-1.1
  │
  ▼
FontLab: Add dotted/slashed zero (carlosedp)
  │  Edited from VFB sources
  │  Added OpenType features: 'zero', 'ezer'
  │
  ▼
Ligaturizer (ToxicFrog/Ligaturizer)
  │  Ligatures from FiraCode
  │  FiraCode Copyright (c) 2015 Nikita Prokopov (OFL-1.1)
  │  Requires: fontforge
  │
  ▼
Nerd Fonts Patcher (ryanoasis/nerd-fonts)
  │  Added powerline, devicons, Font Awesome, etc.
  │  Nerd Fonts License: MIT (code) + OFL-1.1 (glyphs)
  │  Run via: docker run nerdfonts/patcher -c
  │
  ▼
gftools fix-nonhinting
  │  Fix DSIG, GASP, PREP tables
  │  Script: scripts/build.sh
  │
  ▼
B612MonoLigaNerdFont-{Regular,Bold,Italic,BoldItalic}.ttf
  └─ fonts/ligatures_nerd/
```

### Hack Nerd Font Build Chain

```
Hack v3.003 (source-foundry/Hack)
  │  Copyright (c) 2018 Source Foundry Authors
  │  Copyright (c) 2003 Bitstream, Inc.
  │  License: MIT + Bitstream Vera License
  │
  ▼
Nerd Fonts Patcher v3.3.0+ (ryanoasis/nerd-fonts)
  │  Added powerline, devicons, Font Awesome, etc.
  │
  ▼
HackNerdFont-{Regular,Bold,Italic,BoldItalic}.ttf
  └─ From Nerd Fonts releases (Hack.zip)
```

### Source Download Locations

**B612MonoLigaNerdFont TTFs** (from carlosedp/b612, `fonts/ligatures_nerd/`):
```
https://raw.githubusercontent.com/carlosedp/b612/master/fonts/ligatures_nerd/B612MonoLigaNerdFont-Regular.ttf
https://raw.githubusercontent.com/carlosedp/b612/master/fonts/ligatures_nerd/B612MonoLigaNerdFont-Bold.ttf
https://raw.githubusercontent.com/carlosedp/b612/master/fonts/ligatures_nerd/B612MonoLigaNerdFont-Italic.ttf
https://raw.githubusercontent.com/carlosedp/b612/master/fonts/ligatures_nerd/B612MonoLigaNerdFont-BoldItalic.ttf
```

**Hack Nerd Font** (from Nerd Fonts releases):
```
https://github.com/ryanoasis/nerd-fonts/releases/download/v3.4.0/Hack.tar.xz
```
Extract only `HackNerdFont-{Regular,Bold,Italic,BoldItalic}.ttf` (non-Mono variant).

### License Summary

| Component | License(s) | Copyright |
|-----------|-----------|-----------|
| B612 (original) | EPL-2.0 + EDL-1.0 + OFL-1.1 | (c) 2012 AIRBUS |
| FiraCode ligatures | OFL-1.1 | (c) 2015 Nikita Prokopov |
| Hack | MIT + Bitstream Vera License | (c) 2018 Source Foundry Authors, (c) 2003 Bitstream |
| Nerd Fonts glyphs | OFL-1.1 | (c) Ryan McIntyre |
| Nerd Fonts patcher | MIT | (c) Ryan McIntyre |

Planetaire Mono should be distributed under **OFL-1.1** (the common denominator for font
redistribution, compatible with all source licenses).

### Source Repos (Checked Out in `attic/`)

| Directory | Repository | Purpose |
|-----------|-----------|---------|
| `attic/kerm/` | jlevy/kerm | Prior font work, scripts, generated fonts |
| `attic/b612-carlosedp/` | carlosedp/b612 | B612 fork with zero fixes, ligatures, Nerd Fonts |
| `attic/b612-original/` | polarsys/b612 | Original B612 for reference |
| `attic/hack-source/` | source-foundry/Hack | Original Hack font source |
| `attic/nerd-fonts/` | ryanoasis/nerd-fonts | Nerd Fonts patcher and glyph sources |

---

## Analysis of carlosedp Fork (vs. Original polarsys/b612)

The carlosedp fork was compared against the original polarsys/b612 repo to understand
every change made. The fork history is a single squashed commit
(`00aec07`, October 9, 2025) that encompasses all modifications.

### Changes by Category

#### 1. Source Format Change: UFO -> VFC

The original polarsys repo contained **4,800+ UFO files** (text-based, git-trackable font
sources) plus VFB (FontForge Binary) files. The carlosedp fork **replaced all of these**
with 8 **VFC files** (FontLab binary format).

**Implication:** The zero glyph modifications were done in FontLab, a proprietary tool
($99-$399). The VFC format is opaque binary, making it impossible to diff individual glyph
changes in git. This is a step backward for reproducibility.

**For Planetaire:** We do NOT need to reproduce the FontLab editing step. The carlosedp
fork already provides the finished TTF outputs with dotted zero, slashed zero OpenType
features, and all glyph modifications baked in. We consume these as pre-built inputs.

#### 2. Zero Glyph Modifications

- Created a dual-zero system: **dotted zero** (default) + **slashed zero** (via `'zero'`
  OpenType feature) + **empty zero** (via `'ezer'` OpenType feature)
- Applied to both B612 and B612Mono families
- Also created separate `SlashedZero/` subdirectories with slashed zero as the default
  (font-level variant, not just OpenType feature)
- Font file sizes increased 5-70% over originals (indicating new glyph data)

#### 3. Ligature Addition

- Used [Ligaturizer](https://github.com/ToxicFrog/Ligaturizer) (carlosedp's own fork)
  to merge FiraCode ligatures into B612
- Created new font families: `B612Liga` and `B612MonoLiga`
- Ligatures add 20-40% to font file size
- Configured via OpenType `calt` (contextual alternates) feature
- Some ligatures disabled (e.g., `/*` and `*/` to avoid comment interference)

#### 4. Nerd Fonts Patching

- Applied Nerd Fonts patcher via Docker: `docker run nerdfonts/patcher -c`
- Created `B612LigaNerdFont` and `B612MonoLigaNerdFont` families
- File sizes explode from ~200KB to ~2.5MB per font (10-25x increase)
- Only applied to ligaturized variants (not plain fonts)
- Nerd Fonts version not pinned — uses latest Docker image

#### 5. Build Script Rewrite

- Original `scripts/build.sh` (70 lines): VFB->UFO conversion + DSIG fix
- New `scripts/build.sh` (101 lines): Processes 40+ font variants across all directories
- Key operations: `gftools fix-nonhinting` on all fonts (fixes GASP, PREP, DSIG tables)
- Removed VFB->UFO conversion (no longer relevant with VFC sources)
- Added prerequisite checking for `gftools` and `psfnormalize`

#### 6. Documentation and Specimens

- README expanded from 32 to 116 lines with build instructions, VSCode config examples
- Added license files (OFL.txt, EPL-2.0.html, edl-v10.html)
- Added specimen images and text files
- Added AUTHORS.txt, CONTRIBUTORS.txt, TRADEMARKS.md

### Output Organization (48 Total Font Files)

| Directory | Families | Files | Features |
|-----------|----------|-------|----------|
| `fonts/original/` | B612, B612Mono | 8 | Unmodified upstream |
| `fonts/plain/` | B612, B612Mono (+ SlashedZero) | 16 | Dotted/slashed zero |
| `fonts/ligatures/` | B612Liga, B612MonoLiga (+ SlashedZero) | 16 | + FiraCode ligatures |
| `fonts/ligatures_nerd/` | B612LigaNerdFont, B612MonoLigaNerdFont | 8 | + Nerd Font glyphs |

### Best Practices to Adopt

1. **`gftools fix-nonhinting`:** Always run as a final step — fixes GASP, PREP, and DSIG
   tables for proper rendering on all platforms. We should include this in our pipeline.

2. **OpenType feature-based variants:** Using `'zero'`/`'ezer'` features instead of
   separate font files for zero style is elegant. Users configure in their editor rather
   than swapping font files. We preserve this.

3. **Layered build:** Plain -> Ligatures -> Nerd Fonts is a clean progression. Each step
   adds features without modifying the previous layer's work.

4. **Non-Mono Nerd Font variant:** The fork only provides `B612MonoLigaNerdFont`, not a
   non-Mono variant. Kerm switched to non-Mono Hack specifically for wider icon glyphs.
   This is a valid design choice we should support.

### Things We Do Differently

1. **No FontLab dependency:** We consume pre-built TTFs, not VFC sources.
2. **No Docker dependency:** We use Python (fontTools) directly instead of Docker.
3. **No Ligaturizer step:** B612MonoLigaNerdFont already includes ligatures.
4. **No Nerd Fonts patcher step:** Both source fonts already include NF glyphs.
5. **Binary font merging:** Our novel contribution — combining B612 + Hack at the glyph
   level, which neither carlosedp nor any existing project does.

---

## Approach Evaluation: Nerd Fonts Integration

Three approaches were considered for how Planetaire handles Nerd Font glyphs:

### Option A: Run the Nerd Fonts Patcher Ourselves

Re-run `font-patcher` on our merged font to inject Nerd Font glyphs from source SVGs/OTFs.

**Pros:**
- Full control over glyph selection, scaling, and positioning
- Can update Nerd Fonts version independently of upstream fonts
- Could customize which glyph sets to include

**Cons:**
- Requires FontForge as a system dependency (complex C library, not pip-installable)
- The patcher is 2,374 lines of complex code we'd need to invoke/maintain
- Docker is the recommended way to run it (heavyweight)
- Duplicates work already done in source fonts
- Would need to handle the complex scaling/positioning logic for 11+ symbol sets

**Verdict:** Overkill. Both our source fonts already include Nerd Font glyphs.

### Option B: Port Nerd Fonts Patcher Logic to fontTools (Pure Python)

Rewrite the core `copy_glyphs()` logic using fontTools instead of FontForge.

**Pros:**
- Pure Python, no system dependencies
- Full control and customization
- Modern, maintainable codebase

**Cons:**
- Estimated 500-800 LOC to port, 2-3 weeks of effort
- FontForge's copy/paste/transform APIs don't have 1:1 fontTools equivalents
- Would need to handle glyph outline formats (TrueType quadratic vs CFF cubic)
- Risk of subtle rendering differences
- Still duplicates work already done in source fonts

**Verdict:** Interesting long-term option but unnecessary for v1.

### Option C: Use Pre-Patched Source Fonts (Recommended)

Take B612MonoLigaNerdFont (already has NF 3.4.0 glyphs) and HackNerdFont (already has
NF 3.3.0+ glyphs) as inputs. Our pipeline only does the novel work: merging letterforms,
generating ExtraBold weights, and renaming.

**Pros:**
- Simplest approach — no Nerd Fonts patcher dependency at all
- Both sources already battle-tested with correct glyph scaling/positioning
- Eliminates FontForge dependency for Nerd Font patching entirely
- Pure Python pipeline (fontTools) except for ExtraBold generation
- Fastest path to working output

**Cons:**
- Tied to upstream Nerd Fonts versions embedded in source fonts
- Can't independently update Nerd Font glyph set without new source fonts
- Two different NF versions in sources (B612 has 3.4.0, Hack has 3.3.0)

**Mitigation for version mismatch:** Since we're taking *different* glyphs from each font
(B612 for letters/digits, Hack for punctuation/symbols/NF icons), and Nerd Font glyphs
primarily come from the Hack base, the version difference is manageable. Both have
comprehensive NF coverage. We can periodically update source fonts as new versions release.

**Decision: Option C.** Use pre-patched fonts. This keeps the pipeline straightforward
Python, avoids Docker and FontForge for NF patching, and focuses our engineering effort
on the novel merging step that no existing tool provides.

### Future Upgrade Path

If we ever need to independently re-patch with a newer Nerd Fonts version:
1. Download the latest `font-patcher` and glyph sources from nerd-fonts releases
2. Run it on our merged (pre-NF) font: `fontforge -script font-patcher PlanetaireMono.ttf -c`
3. This can be a documented manual step or optional pipeline phase
4. The patcher is designed for exactly this use case — patching any font

---

## Design

### Target Font Family: Planetaire Mono

| Variant | Weight | Style | Source |
|---------|--------|-------|--------|
| Planetaire Mono Regular | 400 | Normal | B612 letters/figures merged into Hack base |
| Planetaire Mono Italic | 400 | Italic | B612 Italic + Hack Italic |
| Planetaire Mono Bold | 700 | Normal | B612 Bold + Hack Bold |
| Planetaire Mono Bold Italic | 700 | Italic | B612 BoldItalic + Hack BoldItalic |
| Planetaire Mono ExtraBold | 800 | Normal | Emboldened Bold composite |
| Planetaire Mono ExtraBold Italic | 800 | Italic | Emboldened BoldItalic composite |

### Approach: Binary Font Merging

Replace the CSS-level unicode-range compositing with actual binary font merging using
`fontTools` (Python). This produces standalone TTF files that work everywhere — native
terminals, IDEs, editors — without requiring CSS font stacking.

**Merging strategy:**
1. Start with Hack Nerd Font as the base (full glyph coverage).
2. Copy B612 glyphs for letters, digits, and extended Latin/Greek/Cyrillic ranges.
3. Preserve B612's OpenType features (`calt` for ligatures, `zero` for slashed zero,
   `ezer` for empty zero).
4. Keep Hack glyphs for punctuation, symbols, box-drawing, Nerd Font icons.
5. Handle UPM mismatch: B612 uses UPM=2000, Hack uses UPM=2048. Normalize to a common
   UPM (likely 2000 to match B612, scaling Hack glyphs down by 2000/2048).

### Pipeline Architecture

```
INPUTS (pre-built, downloaded)
┌──────────────────────────────────────────────────────────────────────┐
│ B612MonoLigaNerdFont-{Regular,Bold,Italic,BoldItalic}.ttf           │
│   (from carlosedp/b612 — already has: dotted zero, ligatures, NF)   │
│                                                                      │
│ HackNerdFont-{Regular,Bold,Italic,BoldItalic}.ttf                   │
│   (from Nerd Fonts releases — already has: NF glyphs, clean punct)  │
└──────────────────────────────────┬───────────────────────────────────┘
                                   │
Phase 1: Download + Validate       │       Phase 2: Embolden (FontForge)
┌──────────────────┐               │       ┌──────────────────────────┐
│ Download sources │               │       │ Bold (700) + changeWeight│
│ Verify checksums │───────────────┼──────>│ → ExtraBold (800)        │
│ Check glyph count│               │       │ For both B612 and Hack   │
└──────────────────┘               │       │ Apply ttfautohint        │
                                   │       └────────────┬─────────────┘
                                   │                    │
Phase 3: Merge (fontTools)         │                    │
┌──────────────────────────┐       │                    │
│ For each weight (400,    │<──────┘                    │
│ 700, 800) × style:       │<──────────────────────────┘
│                          │
│  1. Load Hack as base    │    Phase 4: Finalize (fontTools + gftools)
│  2. Normalize UPM to 2000│    ┌──────────────────────────┐
│  3. Copy B612 glyphs for │───>│ Rename to "Planetaire    │
│     letters/digits       │    │   Mono" family           │
│  4. Copy B612 GSUB       │    │ Update name table IDs    │
│     (calt, zero, ezer)   │    │ Set version string       │
│  5. Keep Hack for all    │    │ gftools fix-nonhinting   │
│     other codepoints     │    │ ttfautohint              │
└──────────────────────────┘    │ Validate output          │
                                └────────────┬─────────────┘
                                             │
OUTPUT                                       │
┌────────────────────────────────────────────▼┐
│ PlanetaireMono-Regular.ttf          (400)   │
│ PlanetaireMono-Italic.ttf           (400)   │
│ PlanetaireMono-Bold.ttf             (700)   │
│ PlanetaireMono-BoldItalic.ttf       (700)   │
│ PlanetaireMono-ExtraBold.ttf        (800)   │
│ PlanetaireMono-ExtraBoldItalic.ttf  (800)   │
└─────────────────────────────────────────────┘
```

**What the pipeline does NOT do** (handled by upstream):
- Nerd Fonts patching (already in source fonts — no Docker needed)
- Ligature injection (already in B612MonoLigaNerdFont via Ligaturizer)
- Zero glyph modification (already in B612 via carlosedp's FontLab edits)
- SVG/OTF glyph source management (Nerd Fonts project handles this)

### Components

The Python package (`src/planetaire/`) will contain:

| Module | Purpose |
|--------|---------|
| `cli.py` | CLI entry point (`planetaire build`, `planetaire inspect`, etc.) |
| `pipeline.py` | Orchestrates the full build pipeline |
| `download.py` | Downloads and caches source fonts from GitHub |
| `embolden.py` | Weight generation (port of `embolden_font.py`) |
| `merge.py` | Binary font merging (B612 glyphs into Hack base) |
| `metadata.py` | Font metadata reading/writing and renaming |
| `validate.py` | Output font validation and comparison |
| `config.py` | Pipeline configuration (glyph ranges, weight params, skip lists) |

### Key Design Decisions

1. **Pure Python pipeline (fontTools), no Docker:**
   - `fontTools` (pure Python, pip-installable) for all glyph copying, metadata editing,
     and validation. No system dependency.
   - No Docker containers. No Nerd Fonts patcher invocation. No Ligaturizer. All of these
     are already baked into the pre-built source fonts.
   - FontForge's `changeWeight()` for emboldening only — this is a complex outline
     operation with no pure-Python equivalent. FontForge remains a system dependency for
     this one step (`brew install fontforge` / `apt install fontforge`).
   - Alternative: pre-generate ExtraBold variants and include them as source fonts,
     eliminating the FontForge dependency entirely for most users.

2. **Pre-patched source fonts (no re-patching):**
   Both B612MonoLigaNerdFont and HackNerdFont already include Nerd Font glyphs, ligatures,
   and zero fixes from their respective upstream build processes. We consume these finished
   TTFs as inputs rather than re-running the complex patching infrastructure.

3. **Hack as base font, B612 glyphs overlaid:**
   Start with Hack (full glyph coverage, Nerd Font icons, clean punctuation) and replace
   specific glyph ranges with B612 glyphs. This ensures no missing glyphs.

4. **Zero glyph:** B612 from carlosedp already has a dotted zero by default, with
   slashed zero available via `'zero'` OpenType feature. We preserve these features.

5. **UPM normalization:** B612 (2000) and Hack (2048) have different UPM values. We need
   to scale one font's glyphs to match. Normalizing Hack to UPM=2000 (scaling by
   2000/2048 = 0.9765625) is preferred since B612 is the primary letterform source.

6. **`gftools fix-nonhinting`:** Adopted from carlosedp's pipeline as a final
   post-processing step. Fixes GASP, PREP, and DSIG tables for proper rendering.

7. **ttfautohint:** Continue using ttfautohint for TrueType hinting on all output fonts.

---

## Implementation Plan

### Phase 1: Repository Setup and Font Migration

- [ ] Copy latest B612MonoLigaNerdFont TTFs from `attic/b612-carlosedp/fonts/ligatures_nerd/` into `fonts/source/b612/`
- [ ] Download and copy latest HackNerdFont TTFs (v3.4.0) into `fonts/source/hack/`
- [ ] Copy license files: B612 `OFL.txt`, `EPL-2.0.html`, `edl-v10.html`; Hack license
- [ ] Create `fonts/source/README.md` documenting provenance
- [ ] Add a `fonts/output/` directory (gitignored) for pipeline output
- [ ] Keep `attic/kerm/assets/fonts/` as reference for the older builds

### Phase 2: Implement Download Script

- [ ] Create `src/planetaire/download.py`
  - Download B612MonoLigaNerdFont TTFs from carlosedp/b612 raw.githubusercontent.com
  - Download Hack Nerd Font from Nerd Fonts releases (Hack.tar.xz)
  - Extract only HackNerdFont (non-Mono) TTFs
  - Verify file integrity (checksums)
  - Cache downloads to avoid re-fetching

### Phase 3: Port and Clean Up Scripts

- [ ] Port `embolden_font.py` to `src/planetaire/embolden.py`
  - Keep FontForge dependency but make it a clean, importable module
  - Extract configuration (weight classes, change amounts, skip lists) to `config.py`
  - Add proper error handling and logging
  - Document the glyph skip/half-weight lists with rationale
- [ ] Create `src/planetaire/metadata.py` using fontTools
  - Read/write font metadata (name table, OS/2 weight, version)
  - Structured output (dict/JSON) for programmatic use
  - Human-readable dump for inspection
- [ ] Create `src/planetaire/validate.py`
  - Verify glyph count, weight class, name table entries
  - Compare metrics against reference fonts
  - Check for missing glyphs in expected ranges

### Phase 4: Implement Font Merging

- [ ] Create `src/planetaire/merge.py` using fontTools
  - Load Hack as base font
  - Load B612 as glyph donor
  - Handle UPM normalization (scale Hack glyphs to match B612's UPM=2000)
  - Copy B612 glyphs for configured unicode ranges into Hack base
  - Copy B612's GSUB table entries for `calt`, `zero`, `ezer` features
  - Preserve Hack's Nerd Font glyphs, box-drawing, punctuation
  - Handle glyph name conflicts and mapping
- [ ] Create `src/planetaire/config.py`
  - Unicode ranges for B612 glyph selection (from `fonts.ts`):
    ```
    U+0030-0039  Basic Latin digits
    U+0041-005A  Basic Latin uppercase
    U+0061-007A  Basic Latin lowercase
    U+00C0-00D6  Latin-1 uppercase with diacritics
    U+00D8-00F6  Latin-1 lowercase with diacritics
    U+00F8-00FF  Latin-1 more lowercase with diacritics
    U+0100-024F  Latin Extended-A and B
    U+0370-03FF  Greek and Coptic
    U+0400-04FF  Cyrillic
    U+0500-052F  Cyrillic Supplement
    U+1E00-1EFF  Latin Extended Additional
    U+2C60-2C7F  Latin Extended-C
    U+A720-A7FF  Latin Extended-D
    U+AB30-AB6F  Latin Extended-E
    ```
  - Weight configuration (`{800: 30, 900: 45}`)
  - Glyph skip lists for emboldening
  - Font naming conventions

### Phase 5: Build Pipeline and CLI

- [ ] Create `src/planetaire/pipeline.py`
  - Orchestrate full pipeline: download -> validate -> embolden -> merge -> finalize
  - Support partial runs (`--skip-download`, `--skip-embolden`)
  - Progress reporting
- [ ] Update `src/planetaire/cli.py`
  - `planetaire build` — run full pipeline, producing all 6 font files
  - `planetaire build --step download|embolden|merge|finalize`
  - `planetaire inspect <font.ttf>` — dump font metadata
  - `planetaire validate <font.ttf>` — validate output font
  - `planetaire download` — download source fonts only
- [ ] Update `pyproject.toml` dependencies: `fonttools`, `gftools`
- [ ] System dependencies: `ttfautohint`, `fontforge` (for embolden step only)

### Phase 6: Finalization and Quality

- [ ] Implement font renaming in the pipeline
  - Family: "Planetaire Mono"
  - Subfamily: Regular, Italic, Bold, Bold Italic, ExtraBold, ExtraBold Italic
  - Update all name table IDs (0-6, 16-17)
  - Set OS/2 weight classes (400, 700, 800)
  - Set version string (e.g., "1.0.0; Planetaire build")
- [ ] Post-processing (adopted from carlosedp best practices):
  - Run `gftools fix-nonhinting` on all output fonts (fixes GASP, PREP, DSIG tables)
  - Run `ttfautohint` for screen rendering optimization
- [ ] Visual QA: render test strings at 10-14pt and compare with reference
- [ ] Ensure license compliance: composite `LICENSE` file with all attributions
- [ ] Update README with font samples, installation, and build instructions

---

## Open Questions

### Resolved

1. **~~Nerd Fonts integration approach~~** — **Resolved: Use pre-patched source fonts
   (Option C).** Both B612MonoLigaNerdFont and HackNerdFont already include NF glyphs.
   No need to run the patcher ourselves. No Docker. No FontForge for this step.

2. **~~Nerd Font version pinning~~** — **Resolved: Track upstream releases.** Use the
   latest available versions of both source fonts. The carlosedp B612 has NF 3.4.0; Hack
   from Nerd Fonts releases has NF 3.3.0+. Since NF glyphs primarily come from the Hack
   base (which provides punctuation/symbols/icons), version mismatch is manageable.
   Periodically update source font downloads.

3. **~~gftools post-processing~~** — **Resolved: Yes, adopt from carlosedp.** Run
   `gftools fix-nonhinting` as a final pipeline step. This is standard practice for
   production font builds.

### Still Open

4. **UPM normalization direction:** Scale Hack to 2000 (match B612) or scale B612 to 2048
   (match Hack)? Scaling Hack down preserves B612's original metrics but may affect Hack
   glyph quality. Need to test both approaches.

5. **Which B612 glyphs to keep vs replace with Hack?** The current unicode-range covers
   letters and digits but excludes all punctuation. Should any punctuation glyphs from
   B612 be kept (e.g., parentheses, quotes)? Need visual comparison.

6. **GSUB feature merging:** When overlaying B612 glyphs onto Hack, we need to bring
   B612's GSUB features (`calt` ligatures, `zero`/`ezer` alternates) but not conflict
   with Hack's own GSUB entries. This may require careful feature table merging.

7. **Black (900) weight:** The embolden script has configuration for weight 900 but it
   was disabled. Should we generate Black weight variants?

8. **FontForge dependency:** Should FontForge be required (for emboldening) or optional?
   Alternative: ship pre-generated ExtraBold sources and make FontForge needed only for
   rebuilding from scratch.

9. **Non-Mono vs Mono variant:** Kerm switched from HackNerdFontMono to HackNerdFont
   (non-Mono) for wider Nerd Font glyphs. Should Planetaire support both?

10. **Upstream source font updates:** When carlosedp or Nerd Fonts release new versions,
    how do we detect and incorporate updates? Should we pin to specific commit hashes /
    release tags, or track latest?

---

## Files Inventory

### Scripts to Port (from `attic/kerm/bin/`)

| File | Lines | Purpose | Port Strategy |
|------|-------|---------|---------------|
| `embolden_font.py` | 180 | Generate heavier weights | Port to module, keep FontForge |
| `dump_font_metadata.py` | ~96 | Inspect font metadata | Rewrite with fontTools |
| `otf_to_ttf.py` | 68 | OTF-to-TTF conversion | Skip (sources are TTF) |

### Source Font Files (Latest)

**B612 (from `attic/b612-carlosedp/fonts/ligatures_nerd/`):**

| File | Size | Glyphs | UPM |
|------|------|--------|-----|
| `B612MonoLigaNerdFont-Regular.ttf` | 2.5 MB | 11,357 | 2000 |
| `B612MonoLigaNerdFont-Bold.ttf` | 2.5 MB | 11,357 | 2000 |
| `B612MonoLigaNerdFont-Italic.ttf` | 2.5 MB | 11,357 | 2000 |
| `B612MonoLigaNerdFont-BoldItalic.ttf` | 2.5 MB | 11,357 | 2000 |

**Hack (from Nerd Fonts v3.3.0 in kerm, should update to v3.4.0):**

| File | Size | Glyphs | UPM |
|------|------|--------|-----|
| `HackNerdFont-Regular.ttf` | 2.5 MB | 11,957 | 2048 |
| `HackNerdFont-Bold.ttf` | 2.6 MB | 11,957 | 2048 |
| `HackNerdFont-Italic.ttf` | 2.6 MB | 11,957 | 2048 |
| `HackNerdFont-BoldItalic.ttf` | 2.6 MB | 11,957 | 2048 |

### Key Configuration (from `attic/kerm/lib/utils/fonts.ts`)

- **B612 unicode range:** Letters (Latin, Greek, Cyrillic) + digits only
- **Font stack:** B612 (letters) -> Hack (everything else) -> system fallbacks
- **Bold weight:** 800 (ExtraBold) for terminal bold, not 700
- **Font size:** 12px default

## References

- [B612 — Original by Airbus/PolarSys](https://github.com/polarsys/b612)
- [carlosedp/b612 — Fork with zero fixes, ligatures, Nerd Fonts](https://github.com/carlosedp/b612)
- [Hack font](https://github.com/source-foundry/Hack)
- [Nerd Fonts](https://github.com/ryanoasis/nerd-fonts)
- [Ligaturizer](https://github.com/ToxicFrog/Ligaturizer)
- [fontTools documentation](https://fonttools.readthedocs.io/)
- [ttfautohint](https://freetype.org/ttfautohint/)
- [gftools](https://github.com/googlefonts/gftools)
- Kerm source scripts: `attic/kerm/bin/embolden_font.py`, `dump_font_metadata.py`
- Kerm font config: `attic/kerm/lib/utils/fonts.ts`
- Kerm terminal config: `attic/kerm/app/config/config-default.json`
- carlosedp build script: `attic/b612-carlosedp/scripts/build.sh`
