// Planetaire Mono - Font Specimen
// Build: planetaire build specimen

// Version is injected by `planetaire build specimen` via `--input version=...`
// (sys.inputs); falls back to a dev default for direct `typst compile`.
#let version = sys.inputs.at("version", default: "0.0.0-dev")
#let build-date = sys.inputs.at("build-date", default: "")

#let page-count = counter(page)

// Palette, helpers, and reusable content blocks shared with the README image cards
// (card.typ), so the home-page images stay in sync with this PDF. Imported early so the
// page footer below can use the shared `muted` gray.
#import "content.typ": *

// ─── DESIGN SYSTEM (read before editing) ────────────────────────────────────────
// Keep this specimen visually simple and consistent. Only the roles below exist.
//
// COLOR — exactly three roles, nothing else:
//   • Main text        → black             (all prose, headings, samples, spec values)
//   • Labels / footers → muted = #6e7781   one single gray: captions, sublabels, the
//                                           page footer, gray descriptive lines
//   • Hairline rules   → rgb("#ccc")       table/box borders and divider lines
//   Syntax highlighting and terminal/colorized text keep their own hues (the dark/
//   light palettes in content.typ). Never add another dark gray or another light gray.
//
// VERTICAL RHYTHM — one line-height system everywhere:
//   • Line height        → leading 0.8em   (~1.5x; one comfortable line)
//   • Between paragraphs → one blank line  (par spacing 2.3em ≈ 2x the line height)
//   • List items         → single line     (row-gutter / list spacing 0.8em)
//   • Around lists/headings → one blank line (block spacing 2.3em)
//   Dense reproductions (terminal, RFC, code) pin their own tighter leading locally.
//
// LAYOUT: never crunch spacing to fit. If content overflows, split across pages (the
//   About spans two pages). The cover uses flexible `fr` spacers for vertical rhythm,
//   intentionally weighted (a larger spacer above the version line) so the version +
//   credits read as a footer set apart from the title cluster.
// ────────────────────────────────────────────────────────────────────────────────

#set page(
  paper: "a4",
  margin: (top: 2cm, bottom: 2cm, left: 2.5cm, right: 2.5cm),
  footer: context {
    if page-count.get().first() > 1 {
      align(center)[
        #text(size: 7pt, fill: muted)[
          Planetaire Mono \u{00B7} github.com/jlevy/planetaire \u{00B7} OFL-1.1
        ]
      ]
    }
  },
)

#set text(font: "Planetaire Mono Extended", size: 10pt)
// Code/raw uses Planetaire too. Typst's built-in `raw` font is DejaVu Sans Mono,
// so without this every code block and inline span would silently fall back to
// DejaVu. Per-block rules below may still override the size or switch to the Text
// family for the web-subset demo.
#show raw: set text(font: "Planetaire Mono Extended")

// Prose line-height: aim for ~1.5x for comfortable reading. On Planetaire Mono
// (long B612 ascenders/descenders), leading 0.8em ≈ 1.49em baseline-to-baseline —
// matching the HTML specimen and the 1.4–1.5 readability norm. Dense terminal, RFC,
// and code blocks (and the cover banner) pin their own tighter leading locally.
// Prose blocks set paragraph spacing to one blank line (2.3em ≈ 2x line height) locally;
// list items sit at the standard single line height (0.8em). Structured pages (spec,
// character set, icons, legibility) keep their own explicit per-element spacing.
#set par(leading: 0.8em)
#set list(spacing: 0.8em)

// Smart quotes OFF document-wide. We author quotes literally -- oriented ‘ ’ “ ” in
// prose, straight ASCII ' " in code/terminal -- exactly as flowmark normalizes the
// README, so the source is WYSIWYG and stays consistent with it. With smart quotes
// ON, Typst re-curls straight quotes and (worse) turns an apostrophe after a digit
// like "B612's" into a U+2032 PRIME. The only escapes left are the glyph-showcase
// rows, which intentionally display exact codepoints.
#set smartquote(enabled: false)

// ─── Page 1: Cover ──────────────────────────────────────────────

// A clean, generous cover: the planet banner, the version line, and the credits, with
// flexible (fr) spacers giving big, even breathing room around each. The star field
// carries its own top whitespace; the spacer above adds plenty more above the image.
#v(1.2fr)

// Shared header block (same artwork as the README banner): full-bleed star field out
// to the page edges, with title/lineage/tagline in solid black for a crisp cover.
#header-card(
  p: pal-light,
  fg: black,
  pad-top: 0cm,
  pad-bottom: 0cm,
  planet-width: 20cm,
  title-size: 44pt,
  sub-size: 15pt,
  tag-size: 15pt,
  planet-gap: 0.85cm,
  sub-gap: 0.1cm,
  tag-gap: 0.95cm,
)

#let b(t) = text(weight: "bold")[#t]

// Extra-generous space above the version line: a weighted spacer (vs the 1.2fr top
// and 1.4fr above credits) drops the version + credits low on the page as a footer.
#v(3.55fr)

#align(center)[
  #text(size: 10pt, weight: "bold", fill: black)[
    Version #version#if build-date != "" [ · #build-date]\
    github.com/jlevy/planetaire
  ]
]

// A healthy amount of space around the credits, lower on the page.
#v(1.4fr)

#align(center)[
  #set par(spacing: 0pt, leading: 0.8em)
  #text(size: 9.5pt, fill: black)[
    #b[Planetaire Mono] assembled and maintained by #b[Joshua Levy]\
    #b[B612 Mono] letterforms by #b[Intactile Design] for #b[Airbus]\
    #b[Hack] base punctuation, symbols, and metrics by #b[Chris Simpkins]\
    #b[Nerd Fonts] 12,000+ icons by #b[Ryan McIntyre]\
    Dotted zero inspired by the B612 fork by #b[Carlos Eduardo de Paula]
  ]
]

// No trailing spacer: the weighting above pushes the credits down to rest at the
// bottom margin, closing the cover as a footer.

#pagebreak()


// ─── Page 2: About ──────────────────────────────────────────────

#[
  #set text(size: 10pt, hyphenate: false)
  // Clean monospace rhythm: 0.8em leading (single line height), one blank line between
  // paragraphs and around the list (2.3em ≈ 2x line height), and single-line bullets.
  // The About splits across two pages rather than crunching the spacing to fit.
  #set par(justify: false, leading: 0.8em, spacing: 2.3em)
  #set block(spacing: 2.3em)
  #show raw: set text(font: "Planetaire Mono Extended", size: 10pt)
  #show link: underline
  #let about-heading(t) = block(text(size: 10pt, weight: "bold")[#t])

  #about-heading("ABOUT B612")
  B612 began not as a typeface but as an aviation research program. In 2010 Airbus,
  ENAC (the French civil aviation university), and the Université de Toulouse III set
  out to define and validate an “aeronautical font” for cockpit screens: text a pilot
  can read correctly while fatigued, at oblique angles, or under vibration, glare, or
  near-darkness.

  The shapes were derived experimentally before they were drawn. Jean-Luc Vinot (ENAC)
  and Sylvie Athènes (Toulouse III) built confusion matrices of when and how characters
  get misread (“Legible, are you sure?” at CHI 2012). In their controlled study, the
  prototype that became B612 drew slightly more correct reads than Verdana and clearly
  outperformed the legacy avionics font. Airbus then commissioned the Montpellier
  interface studio Intactile Design (Nicolas Chauveau, Thomas Paillot, and Jonathan
  Favre-Lamarine) to draw the full family of eight variants.

  B612 is named for the asteroid home of the
  #link("https://en.wikipedia.org/wiki/The_Little_Prince")[Little Prince] by Antoine de
  Saint-Exupéry, who was #link("https://en.wikipedia.org/wiki/Wind,_Sand_and_Stars")[himself an
  aviator].

  B612’s unusual character is a humanist answer to an instrument-panel problem. Where
  earlier cockpit fonts went monolinear and rigid, B612 keeps stroke contrast, opens
  counters, and lengthens ascenders and descenders. Each word’s silhouette resolves
  quickly. At stroke junctions it carries small notches (light traps) that keep joins
  from filling in on bright, low-contrast displays. The result has quietly human
  character quirks that are grounded in measured legibility gains rather than style. In
  2017, B612 was released as open source through the Eclipse Polarsys project.

  #pagebreak()

  #about-heading("ABOUT PLANETAIRE MONO")
  By historical accident, B612 alone is not a usable document or application font. The
  versions in circulation, including the one on Google Fonts, have uneven symbol
  coverage and oddities that make them awkward for modern applications and terminals.
  Some punctuation and symbols are a bit too thin for programming legibility, and the
  published versions have an undotted zero easy to confuse with a capital O.

  Planetaire Mono arises from this need. It merges B612’s letters and digits into Hack
  Nerd Font’s base. It also adds more weights and a dotted zero:

  #grid(
    columns: (1.204em, 1fr),
    row-gutter: 0.8em,
    [•], [*B612 letterforms* for letters, digits, and extended Latin, Greek, and Cyrillic.],
    [•], [*Hack punctuation and symbols* for `{}[]()<>` and the rest.],
    [•], [*Ten variants across five weights* (400/500/600/700/800), including added SemiBold (600) and ExtraBold (800) weights, the latter for terminal bold (see Weights).],
    [•], [*12,000+ Nerd Font icons* (Powerline, Font Awesome, Devicons) in the Extended package.],
    [•], [*A dotted zero:* B612’s zero with a center dot for clear 0 vs O, in circle (default) and rectangle (ss01) variants.],
  )

  Hack has its own lineage: Bitstream Vera Mono (2003) became DejaVu Mono, which Chris
  Simpkins reworked in 2015 into a face tuned for source code at small sizes. Its
  signature is functional punctuation: brackets, braces, parentheses, and operators are
  drawn at a heavier weight and given extra spacing next to letters, so they stay
  distinct in dense code. B612’s own punctuation lacks that weight, which is why
  Planetaire borrows these heavier symbols from Hack.

  #about-heading("A PERSONAL NOTE")
  Like architecture, typography is a functional art form. A design may initially appear
  attractive, but you can’t know its true qualities until you live close to it. Or work
  within it.

  A couple of years ago, while building a terminal, I surveyed monospace fonts to find
  the best ones. B612 wasn’t my obvious first choice, but after trying many of the
  classic modern options available as Nerd Fonts, I came to realize it still just felt
  better over time. I was disappointed with the technical flaws that made it hard to use
  as a full replacement for a workhorse like Hack or JetBrains Mono, so I made an adapted
  hybrid of B612 — happy with it, but never in clean enough form to publish.

  Now, Claude Code and Opus 4.8 have made it a pleasure to consolidate this work as
  Planetaire Mono. I’ve used dozens of terminal fonts over the years, and it is now what
  I use every day. Thanks to agentic coding, monospace fonts are in greater use than
  anyone could have imagined; I hope Planetaire Mono’s aesthetics lighten the hours you
  spend with your agents, editors, and terminals.
]

#pagebreak()


// ─── Page 3: Typeface Specification ─────────────────────────────

#section[Planetaire Typeface Specification]

#v(0.4cm)

#let spec-group(title) = {
  text(size: 8.5pt, weight: "bold", fill: muted)[#title]
  v(0.12cm)
  line(length: 100%, stroke: 0.5pt + rgb("#ccc"))
  v(0.15cm)
}
#let spec-row(label, value) = {
  grid(
    columns: (1fr, auto),
    column-gutter: 0.5cm,
    text(size: 9.5pt, fill: muted)[#label],
    text(size: 9.5pt, fill: black)[#value],
  )
  v(0.14cm)
}

#grid(
  columns: (1fr, 1fr),
  column-gutter: 1.2cm,
  [
    #spec-group("DESIGN")
    #spec-row("Classification", "Monospace (fixed)")
    #spec-row("Letterforms", "B612 Mono (humanist)")
    #spec-row("Packages", "Extended, Text")
    #spec-row("Styles", "10 (5 weights × 2)")
    #spec-row("Units per em", "2000")
    #spec-row("Advance width", "1204 (0.602 em)")
    #spec-row("Italic angle", "0°, true italics")

    #v(0.5cm)
    #spec-group("WEIGHTS")
    #spec-row("Regular", "400")
    #spec-row("Medium", "500")
    #spec-row("SemiBold", "600")
    #spec-row("Bold", "700")
    #spec-row("ExtraBold", "800")
  ],
  [
    #spec-group("VERTICAL METRICS (per 2000 em)")
    #spec-row("Cap height", "1458")
    #spec-row("x-height", "1094")
    #spec-row("Ascender", "1856")
    #spec-row("Descender", "-472")
    #spec-row("Line gap", "0")

    #v(0.5cm)
    #spec-group("GLYPH COVERAGE")
    #spec-row("Extended", "12,138 glyphs")
    #spec-row("Text", "1,317 glyphs")

    #v(0.5cm)
    #spec-group("FORMATS")
    #spec-row("Local install", "TTF")
    #spec-row("Web", "WOFF2 + @font-face CSS")

    #v(0.5cm)
    #spec-group("OPENTYPE")
    #spec-row("default", "circle-dot zero")
    #spec-row("ss01 / zero", "rectangle-dot zero")

    #v(0.5cm)
    #spec-group("LICENSE")
    #spec-row("All packages", "SIL OFL 1.1")
  ],
)

#pagebreak()


// ─── Page 4: Text Showcase ──────────────────────────────────────

#section[Planetaire Text Sample]

#text-sample()

#pagebreak()


// ─── Page 3: Iconic Texts ───────────────────────────────────────

#section[Planetaire Iconic Texts]

// Alan Turing, "Computing Machinery and Intelligence" (1950)
#text(size: 9pt, fill: muted)[
  ALAN TURING \u{00B7} “COMPUTING MACHINERY AND INTELLIGENCE” (1950)
]
#v(0.2cm)

#turing-passage()

#pagebreak()

// RFC 1 - Steve Crocker, 7 April 1969
#rfc-excerpt()

#pagebreak()


// ─── Pages 4–5: microGPT ────────────────────────────────────────

#section[Planetaire Code Specimen: microGPT]

#text(size: 9pt, fill: muted)[
  Andrej Karpathy’s microGPT: a complete GPT training loop and
  inference engine in 200 lines of pure Python.
]
#v(0.2cm)

#block(
  stroke: 0.5pt + rgb("#ccc"),
  inset: (x: 1.2em, y: 1em),
  width: 100%,
)[
  #set text(size: 7.5pt)
  #set par(leading: 0.65em)
  #{
    set raw(theme: "kerm-light.tmTheme")
    raw(read("microgpt.py"), lang: "python", block: true)
  }
]

#pagebreak()


// ─── Terminal ───────────────────────────────────────────────────

#section[Planetaire Terminal]

// The Python example and the terminal session, each shown dark then light,
// matching the two image pairs in the README.
#orbit-code(p: pal-dark)

#v(0.3cm)

#orbit-code(p: pal-light)

// Break so the terminal-session pair (dark + light) sits together on the next page.
#pagebreak()

#terminal-mockup(p: pal-dark)

#v(0.3cm)

#terminal-mockup(p: pal-light)

#pagebreak()


// ─── Character Set ──────────────────────────────────────────────

#section[Planetaire Character Set]

#label[BASIC LATIN UPPERCASE: from B612]
#text(size: 14pt)[#spaced("ABCDEFGHIJKLMNOPQRSTUVWXYZ")]
#v(0.25cm)

#label[BASIC LATIN LOWERCASE: from B612]
#text(size: 14pt)[#spaced("abcdefghijklmnopqrstuvwxyz")]
#v(0.25cm)

#label[DIGITS: 0\u{2013}9 from B612 (zero modified with center dot for O/0 disambiguation)]
#text(size: 14pt)[#spaced("0123456789")]
#v(0.25cm)

#label[PUNCTUATION AND SYMBOLS: from Hack]
#text(size: 14pt)[! " \# \$ % & ' ( ) \* \+ , \- . / : ; < = > ? \@ \[ \\ \] ^ \_ \` \{ | \} \~]
#v(0.25cm)

#label[EXTENDED LATIN: from B612]
#text(size: 14pt)[#spaced("ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞß")]
#v(0.1cm)
#text(size: 14pt)[#spaced("àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ")]
#v(0.1cm)
#text(size: 14pt)[#spaced("ĀāĂăĄąĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚě")]
#v(0.1cm)
#text(size: 14pt)[#spaced("ĞğĠġĢģĤĥĦħĨĩĪīĬĭĮįİıĲĳĴĵĶķ")]
#v(0.25cm)

#label[GREEK: from B612]
#text(size: 14pt)[#spaced("ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ")]
#v(0.1cm)
#text(size: 14pt)[#spaced("αβγδεζηθικλμνξοπρστυφχψω")]
#v(0.25cm)

#label[CYRILLIC: from B612]
#text(size: 14pt)[#spaced("АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ", gap: 0.15em)]
#v(0.1cm)
#text(size: 14pt)[#spaced("абвгдежзийклмнопрстуфхцчшщъыьэюя", gap: 0.15em)]

#pagebreak()


// ─── Weight Comparison ──────────────────────────────────────────

#section[Planetaire Weight Comparison]

#weight-ladder(compact: true)

#pagebreak()


// ─── Size Waterfall ─────────────────────────────────────────────

#section[Planetaire Size Waterfall]

#v(0.2cm)
#size-waterfall()

#pagebreak()


// ─── Legibility ─────────────────────────────────────────────────

#section[Planetaire Legibility]

#label[CHARACTER DISAMBIGUATION]

// Large character pairs with gray labels.
// Fixed-width glyph column so every gray label starts at the same x
// (wide enough for the longest group, the brackets row).
#let disambig(chars, desc) = {
  grid(
    columns: (7cm, 1fr),
    column-gutter: 1cm,
    align: horizon,
    text(size: 28pt)[#chars],
    text(size: 9pt, fill: muted)[#desc],
  )
  v(0.15cm)
}

#disambig[I l 1 |][uppercase I \u{00B7} lowercase l \u{00B7} digit 1 \u{00B7} pipe]
#disambig[O 0 o][uppercase O \u{00B7} digit 0 \u{00B7} lowercase o]
#disambig[r n m][r \u{00B7} n \u{00B7} m \u{2014} clearly distinct in B612]
#disambig[5 S 8 B][digit 5 vs S \u{00B7} digit 8 vs B]
#disambig[2 Z 6 G][digit 2 vs Z \u{00B7} digit 6 vs G]
#disambig[; :][semicolon vs colon \u{2014} distinct dot size and spacing]
#disambig[( ) \{ \} \[ \]][parens vs braces vs brackets]
#disambig[\- \u{2013} \u{2014}][hyphen-minus vs en dash vs em dash]
#disambig[\u{201C} \u{201D} \u{0022}][left double quote vs right double quote vs straight double quote]
#disambig[\u{2018} \u{2019} \u{0027} \u{0060}][left single quote vs right single quote/apostrophe vs straight quote vs backtick]

#v(0.3cm)

#label[ZERO DOT VARIANTS (OpenType)]

#grid(
  columns: (1fr, 1fr),
  gutter: 1cm,
  [
    #text(size: 9pt, fill: muted, weight: "bold")[Default (circle dot)]
    #v(0.1cm)
    #text(size: 36pt)[0]
    #h(0.5cm)
    #text(size: 18pt)[0 O o]
    #v(0.1cm)
    #text(size: 11pt)[FL350 FL850 10.0.0.1]
  ],
  [
    #text(size: 9pt, fill: muted, weight: "bold")[ss01 / zero (rectangle dot)]
    #v(0.1cm)
    #set text(features: ("ss01",))
    #text(size: 36pt)[0]
    #h(0.5cm)
    #text(size: 18pt)[0 O o]
    #v(0.1cm)
    #text(size: 11pt)[FL350 FL850 10.0.0.1]
  ],
)

#v(0.3cm)

#label[BRACKET AND DELIMITER PAIRS]
#text(size: 20pt)[
  ( ) \{ \} \[ \] < > \u{00AB} \u{00BB} \u{2039} \u{203A}
]

#v(0.3cm)

#label[MATHEMATICAL AND PROGRAMMING OPERATORS]
#text(size: 20pt)[\+ \- \* / = \u{2260} \u{2264} \u{2265} \u{00B1} \u{00D7} \u{00F7} \u{2192} \u{2190} \u{2191} \u{2193}]

#pagebreak()


// ─── Symbols and Special Characters ─────────────────────────────

#section[Planetaire Symbols and Special Characters]

#label[STANDARD PUNCTUATION]
#text(size: 16pt)[. , ; : ! ? \- \u{2013} \u{2014} ( ) \[ \] \{ \} / \\ \@ \# \$ % ^ & \* \_ \+ = \~ \`]
#v(0.25cm)

#label[QUOTES AND APOSTROPHES]
#text(size: 16pt)[
  \u{0022} \u{0027} \u{0060} \u{201C} \u{201D} \u{2018} \u{2019} \u{00AB} \u{00BB} \u{2039} \u{203A}
]
#v(0.1cm)
#text(size: 9pt, fill: muted)[
  straight double \u{00B7} straight single \u{00B7} backtick \u{00B7} left double \u{00B7} right double \u{00B7} left single \u{00B7} right single/apostrophe \u{00B7} guillemets \u{00B7} single guillemets
]
#v(0.25cm)

#label[TYPOGRAPHIC AND SPECIAL CHARACTERS]
#text(size: 16pt)[
  \u{00A7} \u{00B6} \u{00A9} \u{00AE} \u{2122} \u{00B0} \u{00B7} \u{2026} \u{2020} \u{2021} \u{00A4} \u{00A2} \u{00A3} \u{00A5} \u{20AC} \u{00AC} \u{00A6}
]
#v(0.1cm)
#text(size: 9pt, fill: muted)[
  section \u{00B7} pilcrow \u{00B7} copyright \u{00B7} registered \u{00B7} trademark \u{00B7} degree \u{00B7} middle dot \u{00B7} ellipsis \u{00B7} dagger \u{00B7} double dagger \u{00B7} currency \u{00B7} cent \u{00B7} pound \u{00B7} yen \u{00B7} euro \u{00B7} not \u{00B7} broken bar
]
#v(0.25cm)

#label[SLASHES AND STROKES]
#text(size: 16pt)[
  \u{002F} \\ | \u{00A6} \u{2044} \u{2215}
]
#v(0.1cm)
#text(size: 9pt, fill: muted)[
  solidus \u{00B7} reverse solidus \u{00B7} vertical bar \u{00B7} broken bar \u{00B7} fraction slash \u{00B7} division slash
]
#v(0.25cm)

#label[BOX DRAWING AND BLOCK ELEMENTS]
#text(size: 14pt)[
  \u{2500} \u{2502} \u{250C} \u{2510} \u{2514} \u{2518} \u{251C} \u{2524} \u{252C} \u{2534} \u{253C} \u{2550} \u{2551} \u{2554} \u{2557} \u{255A} \u{255D} \u{2560} \u{2563} \u{2566} \u{2569} \u{256C} \u{2580} \u{2584} \u{2588} \u{258C} \u{2590} \u{2591} \u{2592} \u{2593}
]


#pagebreak()


// ─── Nerd Font Icons ────────────────────────────────────────────

#section[Nerd Font Icons]

#text(size: 9pt, fill: muted)[
  A selection of the 12,000+ Nerd Font icons included via Hack Nerd Font.
  Each icon shown with its Unicode codepoint.
]
#v(0.3cm)

// Render an icon grid: glyph on top, hex code below, in a compact grid.
#let icon-grid(icons) = {
  let cells = ()
  for (cp, name) in icons {
    cells.push(
      align(center)[
        #text(size: 16pt)[#str.from-unicode(cp)]
        #v(-0.1cm)
        #text(size: 5.5pt, fill: muted)[#upper(str(cp, base: 16))]
      ]
    )
  }
  grid(
    columns: (1fr,) * 14,
    row-gutter: 0.3cm,
    ..cells,
  )
}

#label[UI AND COMMON]
#icon-grid((
  (0xF002, "search"), (0xF005, "star"), (0xF007, "user"),
  (0xF008, "film"), (0xF009, "grid"), (0xF013, "gear"),
  (0xF015, "home"), (0xF017, "clock"), (0xF019, "download"),
  (0xF021, "refresh"), (0xF023, "lock"), (0xF024, "flag"),
  (0xF025, "headphones"), (0xF026, "volume-off"), (0xF028, "volume-up"),
  (0xF02B, "tag"), (0xF02D, "bookmark"), (0xF030, "camera"),
  (0xF03D, "video"), (0xF040, "edit"), (0xF05B, "crosshairs"),
  (0xF06C, "leaf"), (0xF071, "warning"), (0xF073, "calendar"),
  (0xF074, "shuffle"), (0xF07B, "folder"), (0xF07C, "folder-open"),
  (0xF080, "chart"), (0xF085, "gears"), (0xF0C5, "copy"),
  (0xF0C7, "save"), (0xF0C9, "menu"), (0xF0D0, "magic"),
  (0xF0E7, "bolt"), (0xF0EB, "lightbulb"), (0xF0F3, "bell"),
  (0xF0FE, "plus-square"), (0xF11C, "keyboard"), (0xF120, "terminal"),
  (0xF121, "code"), (0xF126, "fork"), (0xF130, "microphone"),
  (0xF15B, "file"), (0xF15C, "file-text"), (0xF187, "archive"),
  (0xF188, "bug"), (0xF1B2, "cube"), (0xF1B3, "cubes"),
  (0xF1C0, "database"), (0xF1D3, "history"), (0xF1DE, "sliders"),
  (0xF1E0, "share"), (0xF1EB, "wifi"), (0xF233, "server"),
  (0xF27A, "comment"), (0xF296, "usb"),
))

#v(0.15cm)
#label[FILE TYPES]
#icon-grid((
  (0xE60A, "conf"), (0xE60E, "font"), (0xE612, "gear"),
  (0xE621, "text"), (0xE622, "todo"), (0xE623, "twig"),
  (0xE624, "typescript"), (0xE635, "pdf"), (0xE63A, "json"),
  (0xE640, "xml"), (0xE648, "zip"), (0xE64A, "image"),
  (0xE64B, "javascript"), (0xE656, "lock"), (0xE657, "makefile"),
  (0xE65E, "sass"), (0xE661, "sql"), (0xE667, "test"),
  (0xE668, "license"), (0xE6A8, "graphql"), (0xE697, "toml"),
  (0xE69B, "shell"), (0xE6A0, "readme"), (0xE6B2, "yaml"),
  (0xE6A1, "changelog"), (0xE6B4, "terraform"), (0xE6A7, "env"),
  (0xE6B7, "log"),
))

#v(0.15cm)
#label[DEVELOPMENT]
#icon-grid((
  (0xE702, "cpp"), (0xE718, "csharp"), (0xE73C, "python"),
  (0xE74E, "ruby"), (0xE781, "perl"), (0xE791, "elm"),
  (0xE7A8, "rust"), (0xE749, "java"), (0xE781, "go"),
  (0xE606, "terminal"), (0xE615, "database"), (0xE796, "swift"),
  (0xE60B, "docker"), (0xE617, "npm"), (0xE73E, "react"),
  (0xE753, "erlang"), (0xE70C, "html"), (0xE749, "java"),
  (0xE755, "haskell"), (0xE706, "markdown"), (0xE628, "vim"),
  (0xE614, "git"), (0xE70E, "css"), (0xE711, "clojure"),
  (0xE718, "csharp"), (0xE62A, "linux"), (0xE629, "windows"),
  (0xE711, "apple"),
))

#v(0.15cm)
#label[WEATHER]
#icon-grid((
  (0xE30D, "sun"), (0xE312, "cloud"), (0xE318, "rain"),
  (0xE31A, "snow"), (0xE320, "fog"), (0xE335, "lightning"),
  (0xE33D, "wind"), (0xE342, "hot"), (0xE343, "cold"),
  (0xE344, "windy"), (0xE366, "moon"), (0xE36E, "sunrise"),
  (0xE370, "sunset"), (0xE3A9, "humidity"),
))

#v(0.15cm)
#label[POWERLINE]
#icon-grid((
  (0xE0A0, "branch"), (0xE0A1, "ln"), (0xE0A2, "lock"),
  (0xE0B0, "right"), (0xE0B1, "right-thin"), (0xE0B2, "left"),
  (0xE0B3, "left-thin"), (0xE0B4, "right-round"), (0xE0B6, "left-round"),
  (0xE0B8, "right-bottom"), (0xE0BA, "left-bottom"),
  (0xE0BC, "right-top"), (0xE0BE, "left-top"),
  (0xE0C0, "flame-thick"), (0xE0C2, "flame-thin"),
  (0xE0C4, "pixel-right"), (0xE0C6, "pixel-left"),
  (0xE0C8, "waveform"), (0xE0CA, "trapezoid"),
  (0xE0CC, "honeycomb"), (0xE0CE, "honeycomb-out"),
  (0xE0D0, "ice"), (0xE0D2, "lego-right"), (0xE0D4, "lego-left"),
))

#pagebreak()


// ─── Provenance & License ───────────────────────────────────────

#section[Planetaire Provenance and License]

#text(size: 11pt, weight: 700)[Source Fonts]
#v(0.2cm)

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt + rgb("#ccc"),
  inset: 8pt,
  [*B612 Mono*], [
    Designed by Intactile Design for Airbus. Optimized for legibility in
    cockpit displays. Planetaire Mono takes its letters (A\u{2013}Z, a\u{2013}z),
    digits 0\u{2013}9, and extended Latin/Greek/Cyrillic glyphs from B612.
    The zero glyph receives a center dot in post-processing for O/0
    disambiguation, with circle (default) and rectangle (ss01) variants.
  ],
  [*Hack*], [
    Chris Simpkins’ typeface designed for source code. Provides the
    base font structure: punctuation, symbols, metrics, and Nerd Font integration.
  ],
  [*Nerd Fonts*], [
    Ryan McIntyre’s icon patching project. 12,000+ developer icons
    including Powerline, Font Awesome, Devicons, Material Design,
    and more, all included via the Hack Nerd Font base.
  ],
)

#v(0.5cm)
#text(size: 11pt, weight: 700)[Build Pipeline]
#v(0.2cm)
#text(size: 10pt)[
  Planetaire Mono is built with a custom Python pipeline using fontTools.
  For each weight variant, the pipeline loads Hack Nerd Font as the base,
  merges B612 letter and digit glyphs by Unicode range, adds a center dot
  to B612’s zero for O/0 disambiguation, renames the result, and applies
  post-processing fixes. Medium and SemiBold weights are generated from
  Regular, and ExtraBold from Bold, via FontForge emboldening.
]

#pagebreak()

#section[Two Packages: Extended and Text]

// Inline raw (e.g. `@font-face`) inherits the surrounding text size via 1em.
#show raw.where(block: false): set text(size: 1em)

#text(size: 10pt)[
  #set par(spacing: 2.3em)
  #set block(spacing: 2.3em)
  Planetaire Mono ships in two packages built from the same letterforms:

  - *Planetaire Mono Extended*: the full build with all \~12,000 Nerd Font icons
    and Powerline, for terminals and coding.
  - *Planetaire Mono Text*: a lightweight web subset (letters, punctuation,
    box-drawing, block elements, geometric shapes) that drops the Private-Use icons.
    About *55 KB per weight* in WOFF2, roughly 18× smaller, and shipped with a ready
    `@font-face` stylesheet.
]

#v(0.5cm)
#text(size: 11pt, weight: 700)[Planetaire Mono Text]
#v(0.2cm)
#block(fill: rgb("#f5f5f5"), inset: 12pt, radius: 4pt, width: 100%)[
  #set par(leading: 0.65em)
  #show raw: set text(font: "Planetaire Mono Text", size: 11pt)
  ```
  The quick brown fox jumps over the lazy dog
  ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz
  0123456789 !@#$%^&*()[]{} <>=+ — Il1| O0o
  Greek ΑΒΓ αβγ · Cyrillic АБВ абв · Box ┌─┬─┐ │ ├─┼─┤ └─┴─┘ ▓▒░
  ```
]

#v(0.6cm)
#text(size: 11pt, weight: 700)[License]
#v(0.2cm)
#text(size: 10pt)[
  #set par(spacing: 2.3em)
  #set block(spacing: 2.3em)
  Planetaire Mono is released under the *SIL Open Font License 1.1 (OFL-1.1)*.

  The OFL allows free use, modification, and redistribution of the font, including
  in commercial products, provided that modified versions are not sold by themselves
  and carry a different name.

  The constituent fonts carry the following licenses:
  - *B612 Mono*: SIL Open Font License 1.1 and Eclipse Public License 2.0
  - *Hack*: MIT License
  - *Nerd Fonts* patches: MIT License
]

// ─── QA page: monospace invariants ──────────────────────────────

#pagebreak()

#section("Spacing Review")

#text(size: 9.5pt, fill: muted)[
  Planetaire Mono is built to a single cell width: every glyph (and intentional
  double-width glyphs at exactly 2x) shares one advance. B612’s letters and the
  FontForge-emboldened weights are normalized to that cell, recentered, and
  condensed only where ink would otherwise bleed. The two panels below are the
  visual proof. Review them to confirm no glyph is trimmed and all weights align.
]

#v(0.5cm)
#coding-width-grid(p: pal-light)

#v(0.8cm)
#coding-width-grid(p: pal-light, italic: true)

#v(0.8cm)
#weight-alignment(p: pal-light)

// Footer is now on every page via the page footer setting.
