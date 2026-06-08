// Planetaire Mono - Font Specimen
// Build: planetaire build specimen

// Version is injected by `planetaire build specimen` via `--input version=...`
// (sys.inputs); falls back to a dev default for direct `typst compile`.
#let version = sys.inputs.at("version", default: "0.0.0-dev")
#let build-date = sys.inputs.at("build-date", default: "")

#let page-count = counter(page)

#set page(
  paper: "a4",
  margin: (top: 2cm, bottom: 2cm, left: 2.5cm, right: 2.5cm),
  footer: context {
    if page-count.get().first() > 1 {
      align(center)[
        #text(size: 7pt, fill: rgb("#bbb"))[
          Planetaire Mono \u{00B7} github.com/jlevy/planetaire \u{00B7} OFL-1.1
        ]
      ]
    }
  },
)

#set text(font: "Planetaire Mono Extended", size: 10pt)

// Palette, helpers, and reusable content blocks shared with the README image
// cards (card.typ) so the home-page images stay in sync with this PDF.
#import "content.typ": *


// ─── Page 1: Cover ──────────────────────────────────────────────

#v(0.2cm)

// Shared header block (same source as the README banner) so the cover and the
// home-page header stay in sync. The cover passes smaller padding than the banner
// default since the page margin already gives the title breathing room.
#header-card(p: pal-light, pad-top: 1.5cm, pad-bottom: 0.7cm)

#v(0.25cm)

#align(center)[
  #text(size: 10pt, weight: "bold", fill: black)[
    Version #version#if build-date != "" [ · #build-date]\
    github.com/jlevy/planetaire
  ]
]

// Even spacing below the title block, matching the section gaps, while keeping the
// full credits list on the page.
#v(0.65cm)

// The three cover sections share one centered, all-black style: a bold all-caps
// heading over centered black items. Paragraph spacing is zeroed so the gap after
// each heading is exactly the explicit v() below (~0.6 of a line) for balance.
#let cover-heading(t) = {
  text(size: 9.5pt, weight: "bold", fill: black)[#t]
  v(0.4cm)
}
#let b(t) = text(weight: "bold")[#t]

#align(center)[
  #set par(spacing: 0pt)
  #cover-heading("FEATURES")
  #text(size: 9.5pt, fill: black)[
    B612 base for letterforms\
    (extended Latin, Greek, Cyrillic)\
    Punctuation and symbols from Hack\
    12,000+ icons from Nerd Fonts\
    Modified zero (0) for legibility
  ]

  #v(0.65cm)
  #cover-heading("WEIGHTS")
  #text(size: 9.5pt, fill: black)[
    #text(weight: "regular")[Regular] (400)\
    #text(weight: "regular", style: "italic")[Italic] (400)\
    #text(weight: 500)[Medium] (500)\
    #text(weight: 500, style: "italic")[Medium Italic] (500)\
    #text(weight: 600)[SemiBold] (600)\
    #text(weight: 600, style: "italic")[SemiBold Italic] (600)\
    #text(weight: "bold")[Bold] (700)\
    #text(weight: "bold", style: "italic")[Bold Italic] (700)\
    #text(weight: 800)[ExtraBold] (800)\
    #text(weight: 800, style: "italic")[ExtraBold Italic] (800)
  ]

  #v(0.65cm)
  #cover-heading("CREDITS")
  #text(size: 9.5pt, fill: black)[
    #b[Planetaire Mono] packaged and maintained by #b[Joshua Levy]\
    #b[B612 Mono] letterforms by #b[Intactile Design] for #b[Airbus]\
    #b[Hack] base punctuation, symbols, and metrics by #b[Chris Simpkins]\
    #b[Nerd Fonts] 12,000+ icons by #b[Ryan McIntyre]\
    Dotted zero inspired by the #b[B612] fork by #b[Carlos Eduardo de Paula]
  ]
]

#pagebreak()


// ─── Page 2: About ──────────────────────────────────────────────

#[
  #set text(size: 10pt, hyphenate: false)
  #set par(justify: false, leading: 0.62em, spacing: 1.2em)
  #show raw: set text(font: "Planetaire Mono Extended", size: 10pt)
  #show link: underline
  #let about-heading(t) = {
    text(size: 10pt, weight: "bold", fill: black)[#t]
    v(0.38cm)
  }
  // Monospace-grid bullet: the marker sits in a 2-cell box (1.204em = 2 cells) so the
  // body and its wrapped lines hang on the cell grid, not at an arbitrary indent.
  #let mb(body) = grid(columns: (1.204em, 1fr), [•], body)

  #about-heading("ABOUT B612")
  B612 began not as a typeface but as an aviation research program. In 2010 Airbus,
  ENAC (the French civil aviation university), and the Université de Toulouse III set
  out to define and validate an "aeronautical font" for cockpit screens: text a pilot
  can read correctly while fatigued, at oblique angles, or under vibration, glare, or
  near-darkness.

  The shapes were derived experimentally before they were drawn. Jean-Luc Vinot (ENAC)
  and Sylvie Athènes (Toulouse III) built confusion matrices of when and how characters
  get misread ("Legible, are you sure?" at CHI 2012). In their controlled study, the
  prototype that became B612 drew slightly more correct reads than Verdana and clearly
  outperformed the legacy avionics font. Airbus then commissioned the Montpellier
  interface studio Intactile Design (Nicolas Chauveau, Thomas Paillot, and Jonathan
  Favre-Lamarine) to draw the full family of eight variants.

  B612 is named for the asteroid home of the
  #link("https://en.wikipedia.org/wiki/The_Little_Prince")[Little Prince], a nod to
  Saint-Exupéry, #link("https://en.wikipedia.org/wiki/Wind,_Sand_and_Stars")[himself an
  aviator].

  B612's unusual character is a humanist answer to an instrument-panel problem. Where
  earlier cockpit fonts went monolinear and rigid, B612 keeps stroke contrast, opens
  counters, and lengthens ascenders and descenders. Each word's silhouette resolves
  quickly. At stroke junctions it carries small notches (light traps) that keep joins
  from filling in on bright, low-contrast displays. The result has quietly human
  character quirks that are grounded in measured legibility gains rather than style. In
  2017, B612 was released as open source through the Eclipse Polarsys project.

  However, B612 alone is not a fully usable document or application font. The versions
  in circulation, including the one on Google Fonts, have uneven symbol coverage that
  is awkward for terminal and programming use. And the published version has an
  undotted zero that is easy to confuse with a capital O.

  #v(0.6cm)
  #about-heading("ABOUT PLANETAIRE MONO")
  Planetaire Mono arises from this need. It merges B612's letters and digits into Hack
  Nerd Font's base. It also adds more weights and a dotted zero:

  #block(spacing: 1.2em)[
    #set par(spacing: 0.55em)
    #mb[*B612 letterforms* for letters, digits, and extended Latin, Greek, and Cyrillic.]
    #mb[*Hack punctuation and symbols* for `{}[]()<>` and the rest.]
    #mb[*Ten variants across five weights* (400/500/600/700/800), including added SemiBold (600) and ExtraBold (800) weights, the latter for terminal bold (see Weights).]
    #mb[*12,000+ Nerd Font icons* (Powerline, Font Awesome, Devicons) in the Extended family.]
    #mb[*A dotted zero:* B612's zero with a center dot for clear 0 vs O, in circle (default) and rectangle (ss01) variants.]
  ]

  With these changes it has become one of the most beautiful and genuinely functional
  monospace fonts I've seen. I've used dozens of terminal fonts over the years, and
  Planetaire Mono is now what I use every day.
]

#pagebreak()


// ─── Page 3: Typeface Specification ─────────────────────────────

#section[Planetaire Typeface Specification]

#v(0.4cm)

#let spec-group(title) = {
  text(size: 8.5pt, weight: "bold", fill: rgb("#888"))[#title]
  v(0.12cm)
  line(length: 100%, stroke: 0.5pt + rgb("#dddddd"))
  v(0.15cm)
}
#let spec-row(label, value) = {
  grid(
    columns: (1fr, auto),
    column-gutter: 0.5cm,
    text(size: 9.5pt, fill: rgb("#666"))[#label],
    text(size: 9.5pt, fill: rgb("#222"))[#value],
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
    #spec-row("Families", "Extended, Text")
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
    #spec-row("All families", "SIL OFL 1.1")
  ],
)

#pagebreak()


// ─── Page 4: Text Showcase ──────────────────────────────────────

#section[Planetaire Text Sample]

#text(size: 9pt, fill: rgb("#999"))[
  Planetaire Mono at various sizes, showing B612\u{2019}s distinctive letterforms
  optimized for readability at small sizes and on low-resolution displays.
]
#v(0.3cm)

#text(size: 14pt)[
  The quick brown fox jumps over the lazy dog. Pack my box with
  five dozen liquor jugs. How vexingly quick daft zebras jump!
]
#v(0.4cm)

#text(size: 11pt)[
  In the great void between stars, instruments must be read without error.
  Every glyph must be unambiguous: the digit 0 distinct from the letter O,
  the numeral 1 clearly not a lowercase l or uppercase I. B612 was born
  from this requirement. Originally designed for cockpit displays at Airbus,
  where a misread character could mean the difference between FL350 and FL850.
  Planetaire Mono inherits that precision and pairs it with the full symbol
  coverage a programmer needs: braces, brackets, pipes, arrows, and 12,000
  icons ready for a modern terminal.
]
#v(0.4cm)

#text(size: 9pt, fill: rgb("#999"))[FRENCH \u{00B7} GERMAN \u{00B7} SPANISH \u{00B7} TURKISH]
#v(0.15cm)
#text(size: 11pt)[
  Les na\u{00EF}fs \u{00E6}githales h\u{00E2}tifs pondent au z\u{00E9}phyr joyeux. Falsches \u{00DC}ben von
  Xylophonmusik qu\u{00E4}lt jeden gr\u{00F6}\u{00DF}eren Zwerg. El veloz murci\u{00E9}lago hind\u{00FA} com\u{00ED}a
  feliz cardillo y kiwi. Pijamal\u{0131} hasta ya\u{011F}\u{0131}z \u{015F}of\u{00F6}re \u{00E7}abucak g\u{00FC}vendi.
]
#v(0.4cm)

#text(size: 9pt, fill: rgb("#999"))[GREEK]
#v(0.15cm)
#text(size: 11pt)[
  \u{039E}\u{03B5}\u{03C3}\u{03BA}\u{03B5}\u{03C0}\u{03AC}\u{03B6}\u{03C9} \u{03C4}\u{1F74}\u{03BD} \u{03C8}\u{03C5}\u{03C7}\u{03BF}\u{03C6}\u{03B8}\u{03CC}\u{03C1}\u{03B1} \u{03B2}\u{03B4}\u{03B5}\u{03BB}\u{03C5}\u{03B3}\u{03BC}\u{03AF}\u{03B1}.
]
#v(0.4cm)

#text(size: 9pt, fill: rgb("#999"))[CYRILLIC]
#v(0.15cm)
#text(size: 11pt)[
  \u{0421}\u{044A}\u{0435}\u{0448}\u{044C} \u{0436}\u{0435} \u{0435}\u{0449}\u{0451} \u{044D}\u{0442}\u{0438}\u{0445} \u{043C}\u{044F}\u{0433}\u{043A}\u{0438}\u{0445} \u{0444}\u{0440}\u{0430}\u{043D}\u{0446}\u{0443}\u{0437}\u{0441}\u{043A}\u{0438}\u{0445} \u{0431}\u{0443}\u{043B}\u{043E}\u{043A}, \u{0434}\u{0430} \u{0432}\u{044B}\u{043F}\u{0435}\u{0439} \u{0447}\u{0430}\u{044E}.
  \u{0428}\u{0438}\u{0440}\u{043E}\u{043A}\u{0430}\u{044F} \u{044D}\u{043B}\u{0435}\u{043A}\u{0442}\u{0440}\u{0438}\u{0444}\u{0438}\u{043A}\u{0430}\u{0446}\u{0438}\u{044F} \u{044E}\u{0436}\u{043D}\u{044B}\u{0445} \u{0433}\u{0443}\u{0431}\u{0435}\u{0440}\u{043D}\u{0438}\u{0439} \u{0434}\u{0430}\u{0441}\u{0442} \u{043C}\u{043E}\u{0449}\u{043D}\u{044B}\u{0439} \u{0442}\u{043E}\u{043B}\u{0447}\u{043E}\u{043A} \u{043F}\u{043E}\u{0434}\u{044A}\u{0451}\u{043C}\u{0443}
  \u{0441}\u{0435}\u{043B}\u{044C}\u{0441}\u{043A}\u{043E}\u{0433}\u{043E} \u{0445}\u{043E}\u{0437}\u{044F}\u{0439}\u{0441}\u{0442}\u{0432}\u{0430}.
]

#pagebreak()


// ─── Page 3: Iconic Texts ───────────────────────────────────────

#section[Planetaire Iconic Texts]

// Alan Turing, "Computing Machinery and Intelligence" (1950)
#text(size: 9pt, fill: rgb("#999"))[
  ALAN TURING \u{00B7} \u{201C}COMPUTING MACHINERY AND INTELLIGENCE\u{201D} (1950)
]
#v(0.2cm)

#turing-passage()

#pagebreak()

// RFC 1 - Steve Crocker, 7 April 1969
#text(size: 9pt, fill: rgb("#999"))[
  RFC 1 \u{00B7} STEVE CROCKER, UCLA \u{00B7} 7 APRIL 1969
]
#v(0.2cm)

#block[
  #set text(size: 8pt)
  #set par(leading: 0.45em, spacing: 0em)
  #show raw: set text(font: "Planetaire Mono Extended", size: 8pt)
  #show raw.where(block: true): it => block(width: 100%, fill: none, inset: 0pt, stroke: none, it)
  #show "Host Software": text.with(weight: 700)
  #show "Steve Crocker": text.with(weight: 700)
  #raw(read("rfc1-excerpt.txt"), block: true)
]

#pagebreak()


// ─── Pages 4–5: microGPT ────────────────────────────────────────

#section[Planetaire Code Specimen: microGPT]

#text(size: 9pt, fill: rgb("#999"))[
  Andrej Karpathy\u{2019}s microGPT: a complete GPT training loop and
  inference engine in 200 lines of pure Python.
]
#v(0.2cm)

#block(
  stroke: 0.5pt + rgb("#ccc"),
  inset: (x: 1.2em, y: 1em),
  width: 100%,
)[
  #set text(size: 7.5pt)
  #{
    set raw(theme: "kerm-light.tmTheme")
    raw(read("microgpt.py"), lang: "python", block: true)
  }
]

#pagebreak()


// ─── Terminal ───────────────────────────────────────────────────

#section[Planetaire Terminal]

#orbit-code()

#v(0.3cm)

#terminal-mockup()

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
#text(size: 9pt, fill: rgb("#999"))[
  Planetaire Mono from caption to display size, holding its proportions throughout.
]
#v(0.5cm)

#let waterfall-line(sz) = {
  grid(
    columns: (1cm, 1fr),
    column-gutter: 0.5cm,
    align: (right + bottom, left + bottom),
    text(size: 7pt, fill: rgb("#bbbbbb"))[#sz],
    text(size: sz * 1pt)[Planetaire Mono],
  )
  v(0.2cm)
}
#for s in (8, 9, 10, 11, 12, 14, 16, 20, 24, 30, 36, 44) {
  waterfall-line(s)
}

#v(0.6cm)
#text(size: 8.5pt, weight: "bold", fill: rgb("#888"))[LEGIBILITY AT DISPLAY SIZE]
#v(0.25cm)
#text(size: 38pt)[Il1| O0o 0123]

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
    text(size: 9pt, fill: rgb("#999"))[#desc],
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
    #text(size: 9pt, fill: rgb("#666"), weight: "bold")[Default (circle dot)]
    #v(0.1cm)
    #text(size: 36pt)[0]
    #h(0.5cm)
    #text(size: 18pt)[0 O o]
    #v(0.1cm)
    #text(size: 11pt)[FL350 FL850 10.0.0.1]
  ],
  [
    #text(size: 9pt, fill: rgb("#666"), weight: "bold")[ss01 / zero (rectangle dot)]
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
#text(size: 9pt, fill: rgb("#999"))[
  straight double \u{00B7} straight single \u{00B7} backtick \u{00B7} left double \u{00B7} right double \u{00B7} left single \u{00B7} right single/apostrophe \u{00B7} guillemets \u{00B7} single guillemets
]
#v(0.25cm)

#label[TYPOGRAPHIC AND SPECIAL CHARACTERS]
#text(size: 16pt)[
  \u{00A7} \u{00B6} \u{00A9} \u{00AE} \u{2122} \u{00B0} \u{00B7} \u{2026} \u{2020} \u{2021} \u{00A4} \u{00A2} \u{00A3} \u{00A5} \u{20AC} \u{00AC} \u{00A6}
]
#v(0.1cm)
#text(size: 9pt, fill: rgb("#999"))[
  section \u{00B7} pilcrow \u{00B7} copyright \u{00B7} registered \u{00B7} trademark \u{00B7} degree \u{00B7} middle dot \u{00B7} ellipsis \u{00B7} dagger \u{00B7} double dagger \u{00B7} currency \u{00B7} cent \u{00B7} pound \u{00B7} yen \u{00B7} euro \u{00B7} not \u{00B7} broken bar
]
#v(0.25cm)

#label[SLASHES AND STROKES]
#text(size: 16pt)[
  \u{002F} \\ | \u{00A6} \u{2044} \u{2215}
]
#v(0.1cm)
#text(size: 9pt, fill: rgb("#999"))[
  solidus \u{00B7} reverse solidus \u{00B7} vertical bar \u{00B7} broken bar \u{00B7} fraction slash \u{00B7} division slash
]
#v(0.25cm)

#label[BOX DRAWING AND BLOCK ELEMENTS]
#text(size: 14pt)[
  \u{2500} \u{2502} \u{250C} \u{2510} \u{2514} \u{2518} \u{251C} \u{2524} \u{252C} \u{2534} \u{253C} \u{2550} \u{2551} \u{2554} \u{2557} \u{255A} \u{255D} \u{2560} \u{2563} \u{2566} \u{2569} \u{256C} \u{2580} \u{2584} \u{2588} \u{258C} \u{2590} \u{2591} \u{2592} \u{2593}
]

#v(0.3cm)

#label[ASCII CHARACTER TABLE (HEXADECIMAL)]
#v(0.1cm)

#block(
  stroke: 0.5pt + rgb("#ccc"),
  inset: (x: 1.2em, y: 1em),
  width: 100%,
)[
  #set text(size: 7.5pt)
  #set par(leading: 0.5em, justify: false)

  #text(weight: 700)[NAME]\
  #h(2.5em)#text(weight: 700)[ascii] - octal, hexadecimal and decimal ASCII character sets\
  \
  #text(weight: 700)[DESCRIPTION]\
  \
  #h(2.5em)The #text(weight: 700)[hexadecimal] set:\
  #h(2.5em)00 nul   01 soh   02 stx   03 etx   04 eot   05 enq   06 ack   07 bel\
  #h(2.5em)08 bs    09 ht    0a nl    0b vt    0c np    0d cr    0e so    0f si\
  #h(2.5em)10 dle   11 dc1   12 dc2   13 dc3   14 dc4   15 nak   16 syn   17 etb\
  #h(2.5em)18 can   19 em    1a sub   1b esc   1c fs    1d gs    1e rs    1f us\
  #h(2.5em)20 sp    21  !    22  "    23  \#    24  \$    25  %    26  &    27  '\
  #h(2.5em)28  (    29  )    2a  \*    2b  \+    2c  ,    2d  \-    2e  .    2f  /\
  #h(2.5em)30  0    31  1    32  2    33  3    34  4    35  5    36  6    37  7\
  #h(2.5em)38  8    39  9    3a  :    3b  ;    3c  <    3d  =    3e  >    3f  ?\
  #h(2.5em)40  \@    41  A    42  B    43  C    44  D    45  E    46  F    47  G\
  #h(2.5em)48  H    49  I    4a  J    4b  K    4c  L    4d  M    4e  N    4f  O\
  #h(2.5em)50  P    51  Q    52  R    53  S    54  T    55  U    56  V    57  W\
  #h(2.5em)58  X    59  Y    5a  Z    5b  \[    5c  \\    5d  \]    5e  ^    5f  \_\
  #h(2.5em)60  \`    61  a    62  b    63  c    64  d    65  e    66  f    67  g\
  #h(2.5em)68  h    69  i    6a  j    6b  k    6c  l    6d  m    6e  n    6f  o\
  #h(2.5em)70  p    71  q    72  r    73  s    74  t    75  u    76  v    77  w\
  #h(2.5em)78  x    79  y    7a  z    7b  \{    7c  |    7d  \}    7e  \~    7f del
]

#pagebreak()


// ─── Nerd Font Icons ────────────────────────────────────────────

#section[Nerd Font Icons]

#text(size: 9pt, fill: rgb("#999"))[
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
        #text(size: 5.5pt, fill: rgb("#999"))[#upper(str(cp, base: 16))]
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
    Chris Simpkins\u{2019} typeface designed for source code. Provides the
    base font structure: punctuation, symbols, metrics, and Nerd Font integration.
  ],
  [*Nerd Fonts*], [
    Ryan McIntyre\u{2019}s icon patching project. 12,000+ developer icons
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
  to B612\u{2019}s zero for O/0 disambiguation, renames the result, and applies
  post-processing fixes. Medium and SemiBold weights are generated from
  Regular, and ExtraBold from Bold, via FontForge emboldening.
]

#pagebreak()

#section[Two Families: Extended and Text]

#text(size: 10pt)[
  Planetaire Mono ships in two families built from the same letterforms:

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
  #show raw: set text(font: "Planetaire Mono Text", size: 11pt)
  ```
  The quick brown fox jumps over the lazy dog
  ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz
  0123456789 !@#$%^&*()[]{} <>=+ — Il1| O0o
  Greek ΑΒΓ αβγ · Cyrillic АБВ абв · Box ┌─┬─┐ │ ├─┼─┤ └─┴─┘ ▓▒░
  ```
]
#v(0.2cm)
#text(size: 9pt, fill: rgb("#666"))[
  For the web: `<link rel="stylesheet" href="planetaire-mono-text.css">` then
  `font-family: "Planetaire Mono Text"`.
]

#v(0.6cm)
#text(size: 11pt, weight: 700)[License]
#v(0.2cm)
#text(size: 10pt)[
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

#text(size: 9.5pt, fill: rgb("#444"))[
  // Disable smart quotes so the straight Hack apostrophe (U+0027) is shown, rather
  // than Typst's curly U+2019, which reads as a prime in this monospace context.
  #set smartquote(enabled: false)
  Planetaire Mono is built to a single cell width: every glyph (and intentional
  double-width glyphs at exactly 2x) shares one advance. B612's letters and the
  FontForge-emboldened weights are normalized to that cell, recentered, and
  condensed only where ink would otherwise bleed. The two panels below are the
  visual proof. Review them to confirm no glyph is trimmed and all weights align.
]

#v(0.5cm)
#coding-width-grid(p: pal-light)

#v(0.8cm)
#weight-alignment(p: pal-light)

// Footer is now on every page via the page footer setting.
