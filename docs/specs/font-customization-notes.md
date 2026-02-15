# Font Customization Notes

**Date:** 2025-01 (original evaluation), 2026-02 (documented)

**Author:** jlevy

**Context:** Complete record of all font evaluations, customizations, weight experiments,
and glyph modifications performed during development of
[kerm](https://github.com/jlevy/kerm), now extracted into the Planetaire Mono project.

---

## Part 1: Nerd Font Base Comparison

Several high-quality monospace Nerd Font families were evaluated for terminal use. All are
credible, well-crafted fonts with distinct personalities.

### B612 Mono Liga Nerd Font

**Source:** [carlosedp/b612](https://github.com/carlosedp/b612) fork of
[polarsys/b612](https://github.com/polarsys/b612)

**Assessment:** Nicest letters and figures. Best letterforms of any font evaluated.
Designed by Airbus/Intactile DESIGN for aircraft cockpit displays — maximizes distance
between character forms for disambiguation. Exceptionally legible at small sizes.

**Strengths:**
- Superior letter and digit design — optimized for readability in adverse conditions
- Dotted zero (default), with slashed zero and empty zero via OpenType features
- Ligatures from FiraCode available (via Ligaturizer)

**Weaknesses:**
- Punctuation and special characters are inconsistent — uneven sizing and visual weight
- Not ideal as a standalone terminal font due to punctuation issues

**Decision:** Use B612 for letters and figures only (restricted unicode-range), with
another font providing punctuation and everything else.

### Hack Nerd Font

**Source:** [source-foundry/Hack](https://github.com/source-foundry/Hack), patched by
[Nerd Fonts](https://github.com/ryanoasis/nerd-fonts)

**Assessment:** The very good modern standard option. Less style but very clean and nice.
Best punctuation and glyphs. Can be used standalone or as a fill-in for better punctuation
in B612.

**Strengths:**
- Very clean punctuation — consistent sizing and weight across all special characters
- Comprehensive glyph coverage
- Solid, professional, reliable
- Non-Mono variant uses double-wide glyphs for Nerd Font icons, which is much better than
  Mono variants

**Weaknesses:**
- Letterforms are good but not as distinctive as B612

**Decision:** Use as the base font for punctuation, symbols, box-drawing, and Nerd Font
icons. Switched from Mono to non-Mono variant for wider (double-width) Nerd Font glyphs.

### Monaspace Ne (MonaspiceNe Nerd Font Mono)

**Source:** [githubnext/monaspace](https://github.com/githubnext/monaspace) "Neon"
variant, patched by Nerd Fonts

**Assessment:** Another attractive option. Stylish, not quite as clear as Hack. I also
found I preferred Hack punctuation.

**Strengths:**
- Visually distinctive and modern
- Good ligature support
- Attractive at typical terminal sizes

**Weaknesses:**
- Less clear than Hack at small sizes
- Punctuation not as clean as Hack
- Style can be distracting for extended coding sessions

**Decision:** Tested as the fallback font (B612 letters + Monaspace Ne for rest) but
ultimately replaced by Hack, which had cleaner punctuation.

### Monaspace Xe (MonaspiceXe Nerd Font Mono)

**Source:** [githubnext/monaspace](https://github.com/githubnext/monaspace) "Xenon"
variant

**Assessment:** Interesting but quirkier option. A different Monaspace axis with its own
character.

**Decision:** Evaluated but not selected. More quirky than Ne variant.

### GoMono Nerd Font Mono

**Source:** Go project's monospace font, patched by Nerd Fonts

**Assessment:** Interesting but quirkier option.

**Decision:** Evaluated but not selected. Has character but not the best fit for
terminal use.

### iMWritingMono Nerd Font Mono

**Source:** iA Writer's monospace font, patched by Nerd Fonts

**Assessment:** Interesting but quirkier option.

**Decision:** Evaluated but not selected. Designed more for prose than code.

### RecMonoLinear Nerd Font Mono

**Source:** Recursive Mono (Linear static variant), patched by Nerd Fonts

**Assessment:** Interesting but quirkier option.

**Decision:** Evaluated but not selected.

---

## Part 2: Font Selection Timeline

| Date | Commit | Decision |
|------|--------|----------|
| 2025-01-11 | `a3b21ca1` | Switch to Hack Nerd Font Mono as primary font |
| 2025-01-13 | `e0ced10b` | Generate bolder Hack font (ExtraBold 800, Black 900 weights) |
| 2025-01-13 | `68a38693` | More font options. Switch to Monaspace Ne |
| 2025-01-13 | `8c72d3a8` | Experimenting with B612 font as well |
| 2025-01-14 | `bea2cfc1` | Fonts: B612 for letters+figures, Monaspace Ne for rest |
| 2025-01-14 | `f2a13c27` | Fonts: B612 letters+figures and Hack for rest |
| 2025-01-23 | `63125cfd` | Wider glyph Hack Nerd Font (switched from Mono to non-Mono) |

Key transitions:
1. Started with Hack Mono as the sole font
2. Explored Monaspace Ne — attractive but found Hack's punctuation cleaner
3. Discovered B612's superior letterforms, tried composite approach
4. Settled on B612 (letters/digits) + Hack (everything else) as the optimal combination
5. Final refinement: switched Hack from Mono to non-Mono for better icon rendering

---

## Part 3: Weight Customization

### The Problem

Standard Bold (weight 700) is too subtle at 12px terminal size. Bold text in a terminal
needs to be visually *obvious* — for prompts, headings, highlighted output. The jump from
Regular (400) to Bold (700) wasn't enough.

### The Solution: ExtraBold (800)

Generated ExtraBold (800) weight variants using FontForge's `changeWeight()` API.

**Script:** `attic/kerm/bin/embolden_font.py`
**Tool:** FontForge (run as `fontforge -script embolden_font.py <input.ttf>`)

**Weight change parameters** (trial-and-error tuned):

```python
WEIGHT_CHANGES = {800: 30, 900: 45}
# 30 units for ExtraBold — seems better for B612
# Earlier: {800: 36, 900: 54} — seemed good for Hack
```

The `changeWeight` parameter is somewhat trial-and-error and depends on the font's UPM
and desired boldness. Small increments (10, 14, 20) for subtle differences; bigger for
heavier outlines.

### Glyph-Specific Handling

Not all glyphs survive emboldening equally. Some complex Nerd Font icons break or look
wrong when strokes are thickened:

```python
# Skip entirely (would break or look wrong if emboldened):
SKIP_GLYPHS = {"fae-gut", "dev-ohmyzsh", "uniE24B"}

# Half-weight (lighter emboldening to preserve detail):
HALF_WEIGHT_GLYPHS = {"dev-babel", "dev-postcss"}
```

### Weight Variants Generated

**B612MonoLigaNerdFont:**

| Variant | Weight | Source |
|---------|--------|--------|
| Regular | 400 | From carlosedp (as-is) |
| Bold | 700 | From carlosedp (as-is) |
| Italic | 400 | From carlosedp (as-is) |
| BoldItalic | 700 | From carlosedp (as-is) |
| ExtraBold | 800 | Generated from Bold via `embolden_font.py` (change=30) |
| ExtraBoldItalic | 800 | Generated from BoldItalic via `embolden_font.py` (change=30) |

**Hack Nerd Font:**

| Variant | Weight | Source |
|---------|--------|--------|
| Regular | 400 | From Nerd Fonts release (as-is) |
| Bold | 700 | From Nerd Fonts release (as-is) |
| Italic | 400 | From Nerd Fonts release (as-is) |
| BoldItalic | 700 | From Nerd Fonts release (as-is) |
| ExtraBold | 800 | Generated from Bold via `embolden_font.py` (change=30) |
| ExtraBoldItalic | 800 | Generated from BoldItalic via `embolden_font.py` (change=30) |
| Black | 900 | Generated from Bold via `embolden_font.py` (change=45) |
| BlackItalic | 900 | Generated from BoldItalic via `embolden_font.py` (change=45) |

### Black (900) Weight

Also generated but ultimately not used in the final kerm configuration. Available in the
Hack Nerd Font variant only. The configuration for 900 weight is preserved in the
embolden script but was disabled (`WEIGHT_CLASSES = [800]`, not `[800, 900]`).

### Post-Emboldening: ttfautohint

All emboldened fonts are run through `ttfautohint` for screen rendering optimization.
The embolden script generates an unhinted TTF first, then runs ttfautohint, then removes
the intermediate file.

---

## Part 4: Zero Glyph Customization

### The Problem

The original B612 zero (`0`) is an empty oval — ambiguous with uppercase `O`, which is
unacceptable for code.

### The Dotted Zero

The carlosedp fork of B612 modified the zero glyph to include a **center dot** (a small
filled rectangle inside the zero). This is the default rendering.

**Technical detail (confirmed via fontTools inspection):**
- Original B612 zero: **2 contours**, 56 points (outer oval + inner counter)
- Carlosedp/kerm dotted zero: **3 contours**, 60 points (outer oval + inner counter +
  center dot)
- The center dot is the 3rd contour (4 additional points forming a small rectangle,
  approximately at coordinates 544,545 to 765,893 in a UPM=2000 font)
- Glyph width: 1300 units, left side bearing: 141 units
- Bounding box: xMin=141, yMin=-17, xMax=1161, yMax=1517

### Kerm vs. Carlosedp Zero Comparison

The zero glyphs are **byte-for-byte identical** between the kerm fonts (version 1.010)
and the current carlosedp fonts (version 1.009):
- Same coordinates, same flags, same contour endpoints, same bounding box
- Both have 3 contours, 60 points
- The dotted zero design originated in carlosedp's FontLab edits

The dotted zero has been working well in kerm — it's clear, unambiguous, and doesn't
distract from reading code.

### OpenType Feature Alternates

The carlosedp fork also provides two alternate zero styles via OpenType features:

| Feature | Zero Style | Description |
|---------|-----------|-------------|
| (default) | Dotted zero | Center dot inside the zero — best for code |
| `'zero'` | Slashed zero | Diagonal slash through the zero |
| `'ezer'` | Empty zero | Original B612 empty oval (ambiguous) |

**GSUB feature counts:**
- Kerm fonts (older NF patcher): 22 feature records each for `zero`, `ezer`, `calt`
- Carlosedp fonts (NF 3.4.0): 1 feature record each (different GSUB table structure,
  same functionality)

These features let users choose their preferred zero style in their editor. Example
VSCode config:
```json
"editor.fontLigatures": "'zero' on"
```

### Version Discrepancy

The kerm B612 fonts show version `1.010; ttfautohint (v1.8.4)` while the current
carlosedp repo shows `1.009; Nerd Fonts 3.4.0`. Despite the higher version number, the
kerm fonts have fewer glyphs (5,144 vs 11,357). This indicates the kerm fonts are from
an **earlier carlosedp build** (patched with an older Nerd Fonts version), while
carlosedp later rebuilt with NF 3.4.0 which added ~6,200 more glyphs but changed the
version string.

For Planetaire, we use the **latest carlosedp fonts** (1.009, NF 3.4.0, 11,357 glyphs)
as source.

---

## Part 5: Font Compositing Strategy

### CSS-Level Compositing (Kerm's Approach)

Kerm used CSS `unicode-range` to composite B612 and Hack at the browser level:

**B612 covers** (letters and digits only):
```
U+0030-0039   Basic Latin digits
U+0041-005A   Basic Latin uppercase
U+0061-007A   Basic Latin lowercase
U+00C0-00D6   Latin-1 uppercase with diacritics
U+00D8-00F6   Latin-1 lowercase with diacritics
U+00F8-00FF   Latin-1 more lowercase with diacritics
U+0100-024F   Latin Extended-A and B
U+0370-03FF   Greek and Coptic
U+0400-04FF   Cyrillic
U+0500-052F   Cyrillic Supplement
U+1E00-1EFF   Latin Extended Additional
U+2C60-2C7F   Latin Extended-C
U+A720-A7FF   Latin Extended-D
U+AB30-AB6F   Latin Extended-E
```

**Hack covers** (everything else — no unicode-range restriction):
- All ASCII punctuation: `! @ # $ % ^ & * ( ) - = + [ ] { } | \ ; : ' " , . < > / ?`
- Box-drawing characters (U+2500-259F)
- Nerd Font icons (powerline, devicons, Font Awesome, etc.)
- Any missing glyphs from B612's range

**Punctuation ranges that were tested but excluded from B612** (commented out in
`fonts.ts`):
```
// U+0020-0029  ASCII punctuation — rejected (Hack's are more consistent)
// U+003A-0040  ASCII punctuation — rejected
// U+007B-007E  ASCII punctuation — rejected
// U+0028-0029  Parentheses — rejected
// U+003A-003B  Colon and semicolon — rejected
// U+003C-003E  Less than, greater than — rejected
// U+003F-0040  Question mark and at sign — rejected
// U+005B-005D  Square brackets — rejected
// U+007B-007E  Curly braces — rejected
```

All punctuation was tested from B612 and rejected — Hack's punctuation is more consistent
in sizing and visual weight.

### Limitation of CSS Compositing

CSS `unicode-range` only works in browser/Electron contexts. Does not work in native
terminals, IDEs, or general font distribution. This is exactly what Planetaire Mono solves
— binary font merging to produce a standalone TTF.

---

## Part 6: Terminal Configuration Tuning

### Final Kerm Configuration

```json
{
  "fontSize": 12,
  "fontFamily": "\"B612Mono Liga NerdFont\", \"Hack Nerd Font\", Menlo, ...",
  "fontWeight": "400",
  "fontWeightBold": "800",
  "lineHeight": 1.04,
  "disableLigatures": true
}
```

### Line Height

Tuned through experimentation:
- Started at **1.15** — too airy
- Tried **1.0** — too tight
- Settled at **1.04** — optimal balance

### Ligatures

**Disabled** (`disableLigatures: true`), even though the B612 Liga font has FiraCode
ligatures baked in via the `calt` OpenType feature. The ligatures are available but
turned off. This is a per-user preference — some people love code ligatures, others find
them distracting.

### Non-Mono Nerd Font Variant

Kerm specifically switched from `Hack Nerd Font Mono` to `Hack Nerd Font` (non-Mono).
The non-Mono variant uses **double-wide glyphs** for Nerd Font icons, which render much
better than single-cell-width Mono glyphs. Most modern terminals support double-width
characters.

### Font Stack Fallback Chain

```
B612Mono Liga NerdFont    → Best letters and figures (unicode-range restricted)
Hack Nerd Font            → Best punctuation and glyphs (full fallback)
Menlo                     → macOS system monospace
DejaVu Sans Mono          → Linux system monospace
Lucida Console            → Windows system monospace
monospace                 → Generic fallback
```

---

## Part 7: Design Principles

Derived from the evaluation process:

1. **Legibility over style.** B612's cockpit-optimized letterforms beat stylish alternatives
   at small sizes and in extended use.
2. **Composite is better than compromise.** No single font excelled at everything. Combining
   B612's letters with Hack's punctuation gives the best of both.
3. **Non-Mono for icons.** Double-width Nerd Font glyphs render much better than
   single-cell-width Mono variants. Most modern terminals support this.
4. **ExtraBold for terminal bold.** Standard Bold (700) is too subtle at 12px. ExtraBold
   (800) provides the visual distinction needed for terminal bold text.
5. **Punctuation quality matters.** Hack was chosen over Monaspace Ne specifically because
   of cleaner, more consistent punctuation — a detail that matters for code readability.
6. **Dotted zero is non-negotiable.** Empty zeros are ambiguous with `O`. The dotted zero
   from carlosedp's fork is clear and unobtrusive.

---

## References

- Font stack: `attic/kerm/lib/utils/fonts.ts`
- Terminal config: `attic/kerm/app/config/config-default.json`
- Embolden script: `attic/kerm/bin/embolden_font.py`
- Font metadata inspector: `attic/kerm/bin/dump_font_metadata.py`
- B612 source README: `attic/kerm/assets-extras/fonts/B612MonoLigaNerdFont-README.md`
- Hack source README: `attic/kerm/assets-extras/fonts/HackNerdFontMono-README.md`
- Active fonts: `attic/kerm/assets/fonts/`
- Evaluated fonts: `attic/kerm/assets-extras/fonts/`
