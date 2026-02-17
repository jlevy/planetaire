// Planetaire Mono - Font Specimen
// Build: planetaire build specimen

#let version = "0.1.0"

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

#set text(font: "Planetaire Mono", size: 10pt)

// Kerm terminal theme colors (dark palette).
#let kerm = (
  bg:      rgb("#000000"),
  fg:      rgb("#ffffff"),
  black:   rgb("#4d4d4d"),
  red:     rgb("#eb8f83"),
  green:   rgb("#6dc481"),
  yellow:  rgb("#caa94e"),
  blue:    rgb("#96aced"),
  magenta: rgb("#dc8dd6"),
  cyan:    rgb("#55bdcd"),
  white:   rgb("#dbdbdf"),
  bright-black: rgb("#bababa"),
)

// Kerm-derived palette, darkened for light/white backgrounds.
#let kerm-light = (
  bg:      rgb("#f6f8fa"),
  fg:      rgb("#24292f"),
  comment: rgb("#6e7781"),
  red:     rgb("#a8342a"),
  green:   rgb("#1a7f37"),
  yellow:  rgb("#7d5e00"),
  blue:    rgb("#0550ae"),
  magenta: rgb("#8250df"),
  cyan:    rgb("#0e6b7a"),
)

// Section heading helper.
#let section(title) = {
  text(size: 16pt, weight: 700)[#title]
  v(0.3cm)
  line(length: 100%, stroke: 0.5pt + rgb("#ccc"))
  v(0.5cm)
}

// Label for character set sections.
#let label(body) = {
  text(size: 8pt, fill: rgb("#999"))[#body]
  v(0.1cm)
}

// Spaced character display: inserts thin gaps between characters.
#let spaced(s, gap: 0.25em) = s.clusters().join(h(gap))

// Syntax-highlighted code block with Kerm colors.
// Each token is a (text, color) pair. Use none for default fg.
#let code-block(tokens) = {
  block(
    fill: kerm.bg,
    inset: (x: 1.2em, y: 1em),
    radius: 4pt,
    width: 100%,
  )[
    #set text(size: 9.5pt, fill: kerm.fg)
    #for tok in tokens {
      let (s, c) = tok
      if c == none { s } else { text(fill: c)[#s] }
    }
  ]
}


// ─── Page 1: Cover ──────────────────────────────────────────────

#v(3cm)

#align(center)[
  #text(size: 36pt, weight: 700)[Planetaire Mono]

  #v(0.5cm)
  #text(size: 13pt, fill: rgb("#666"))[
    B612 base for letterforms\
    (A\u{2013}Z, a\u{2013}z, 0\u{2013}9, extended Latin, Greek, Cyrillic)\
    Modified zero (0) for legibility\
    Punctuation and symbols from Hack\
    12,000+ icons from Nerd Fonts
  ]

  #v(0.8cm)
  #text(size: 10pt, fill: rgb("#666"))[
    Joshua Levy\
    github.com/jlevy/planetaire\
    Version #version
  ]
]

#v(1.5cm)

#text(size: 10pt)[
  Planetaire Mono is a composite monospace font that merges the highly legible
  letterforms of B612, a typeface designed by Intactile Design for Airbus cockpit
  displays, with Hack Nerd Font\u{2019}s complete infrastructure: punctuation,
  symbols, and 12,000+ developer icons.
]

#v(0.3cm)

#text(size: 10pt)[
  The result is a font optimized for terminal and editor use that combines
  aviation-grade character clarity with full programming language coverage.
  The name is a nod to asteroid B-612 from _The Little Prince_.
]

#v(1.5cm)

#text(size: 9pt, fill: rgb("#666"))[
  *Weights*\
  #text(weight: "regular")[Regular] (400) #h(1em)
  #text(weight: "regular", style: "italic")[Italic] (400) #h(1em)
  #text(weight: 500)[Medium] (500) #h(1em)
  #text(weight: 500, style: "italic")[Medium Italic] (500)\
  #text(weight: "bold")[Bold] (700) #h(1em)
  #text(weight: "bold", style: "italic")[Bold Italic] (700) #h(1em)
  #text(weight: 800)[ExtraBold] (800) #h(1em)
  #text(weight: 800, style: "italic")[ExtraBold Italic] (800)
]

#pagebreak()


// ─── Page 2: Text Showcase ──────────────────────────────────────

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
  Les na\u{00EF}fs \u{00E6}githales h\u{00E2}tifs pondsjflam au z\u{00E9}phyr joyeux. Falsches \u{00DC}ben von
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

#text(size: 10.5pt)[
  I propose to consider the question, \u{201C}Can machines think?\u{201D} This should
  begin with definitions of the meaning of the terms \u{201C}machine\u{201D} and
  \u{201C}think.\u{201D} The definitions might be framed so as to reflect so far as
  possible the normal use of the words, but this attitude is dangerous.
  If the meaning of the words \u{201C}machine\u{201D} and \u{201C}think\u{201D} are to be found
  by examining how they are commonly used it is difficult to escape the
  conclusion that the meaning and the answer to the question, \u{201C}Can
  machines think?\u{201D} is to be sought in a statistical survey such as a
  Gallup poll. But this is absurd. Instead of attempting such a definition
  I shall replace the question by another, which is closely related to it
  and is expressed in relatively unambiguous words.
]

#v(0.6cm)

// RFC 1 - Steve Crocker, 7 April 1969
#text(size: 9pt, fill: rgb("#999"))[
  RFC 1 \u{00B7} STEVE CROCKER, UCLA \u{00B7} 7 APRIL 1969
]
#v(0.2cm)

#block[
  #set text(size: 8pt)
  #set par(leading: 0.55em, spacing: 0.8em)

  #grid(
    columns: (1fr, auto),
    row-gutter: 0.2em,
    [Network Working Group], [Steve Crocker],
    [Request for Comments: 1], [UCLA],
    [], [7 April 1969],
  )
  #v(0.2cm)
  #align(center)[#text(size: 9pt, weight: 700)[Host Software]]
  #v(0.3cm)

  #text(weight: 700)[Introduction]
  #v(0.1cm)

  #h(1.5em)The software for the ARPA Network exists partly in the IMPs and
  partly in the respective HOSTs. BB&N has specified the software of
  the IMPs and it is the responsibility of the HOST groups to agree on
  HOST software.

  #h(1.5em)During the summer of 1968, representatives from the initial four
  sites met several times to discuss the HOST software and initial
  experiments on the network. There emerged from these meetings a
  working group of three, Steve Carr from Utah, Jeff Rulifson from SRI,
  and Steve Crocker of UCLA, who met during the fall and winter. The
  most recent meeting was in the last week of March in Utah. Also
  present was Bill Duvall of SRI who has recently started working with
  Jeff Rulifson.

  #h(1.5em)I present here some of the tentative agreements reached and some of
  the open questions encountered. Very little of what is here is firm
  and reactions are expected.

  #v(0.2cm)
  #text(weight: 700)[I. #h(0.5em) A Summary of the IMP Software]
  #v(0.1cm)
  #text(weight: 700)[Messages]
  #v(0.05cm)

  #h(1.5em)Information is transmitted from HOST to HOST in bundles called
  messages. A message is any stream of not more than 8080 bits,
  together with its header. The header is 16 bits and contains the
  following information:

  #v(0.1cm)
  #h(4em)Destination #h(2em) 5 bits\
  #h(4em)Link #h(4.6em) 8 bits\
  #h(4em)Trace #h(3.9em) 1 bit\
  #h(4em)Spare #h(3.9em) 2 bits

  #v(0.1cm)
  #h(1.5em)The destination is the numerical code for the HOST to which the
  message should be sent. The trace bit signals the IMPs to record
  status information about the message and send the information back to
  the NMC (Network Measurement Center, i.e., UCLA). The spare bits are
  unused.
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
  radius: 4pt,
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

// Helper for colored spans in the terminal block.
#let t(body, color) = text(fill: color)[#body]
#let tb(body, color) = text(fill: color, weight: "bold")[#body]

// Shell prompt helper.
#let prompt(cmd) = {
  tb("planetaire", kerm.blue)
  text(weight: "bold")[ \$ ]
  cmd
}

// Nerd Font icon helper.
#let icon(cp) = str.from-unicode(cp)

// eza directory entry helper with box-wrapped spans for precise alignment.
#let dir-entry(perms, size, user, date, ic, name, bold-name: false) = {
  box[#t(perms, kerm.bright-black)]
  box[#t(" ", kerm.fg)]
  box[#tb(size, kerm.green)]
  box[#t(" ", kerm.fg)]
  box[#tb(user, kerm.yellow)]
  box[#t(" ", kerm.fg)]
  box[#t(date, kerm.blue)]
  box[#t(" ", kerm.fg)]
  box[#t(ic, kerm.cyan)]
  box[#t(" ", kerm.fg)]
  if bold-name { box[#tb(name, kerm.fg)] } else { box[#t(name, kerm.fg)] }
}

// Python sample with manual Kerm-colored tokens.
#code-block((
  // def analyze_trajectory(...)
  (text(weight: "bold")[def], kerm.magenta), (" analyze_trajectory", none),
  ("(", none), ("altitude", none), (": ", none),
  ("float", kerm.cyan), (", ", none), ("velocity", none), (": ", none),
  ("float", kerm.cyan), (") -> ", none), ("dict", kerm.cyan), (":\n", none),

  // docstring
  ("    ", none), ("\"\"\"Calculate orbital parameters.\"\"\"", kerm.green), ("\n\n", none),

  // constants
  ("    G ", none), ("= ", none), ("6.674e-11", kerm.cyan),
  ("  ", none), ("# gravitational constant", kerm.black), ("\n", none),
  ("    M ", none), ("= ", none), ("5.972e24", kerm.cyan), ("\n\n", none),

  // if/elif
  ("    ", none), (text(weight: "bold")[if], kerm.magenta),
  (" altitude > ", none), ("400_000", kerm.cyan), (":\n", none),
  ("        orbit_type ", none), ("= ", none),
  ("\"LEO\"", kerm.green), ("\n", none),
  ("    ", none), (text(weight: "bold")[elif], kerm.magenta),
  (" altitude > ", none), ("35_786_000", kerm.cyan), (":\n", none),
  ("        orbit_type ", none), ("= ", none),
  ("\"GEO\"", kerm.green), ("\n\n", none),

  // period calculation
  ("    period ", none), ("= ", none), ("2", kerm.cyan),
  (" * math.pi * math.sqrt(altitude**", none), ("3", kerm.cyan),
  (" / (G * M))\n\n", none),

  // return
  ("    ", none), (text(weight: "bold")[return], kerm.magenta),
  (" {", none), ("\"type\"", kerm.green), (": orbit_type, ", none),
  ("\"period\"", kerm.green), (": period, ", none),
  ("\"v\"", kerm.green), (": velocity}\n", none),
))

#v(0.3cm)

#block(
  fill: kerm.bg,
  inset: (x: 1.2em, y: 1em),
  radius: 4pt,
  width: 100%,
)[
  #set text(size: 8.5pt, fill: kerm.fg)
  #set par(leading: 0.4em, justify: false)

  #prompt[eza -l --icons=always . ./docs/specimen/]\
  .:\
  #dir-entry("drwxr-xr-x@", "   -", "levy", "15 Feb 23:07", icon(0xF07B), "devtools", bold-name: true)\
  #dir-entry("drwxr-xr-x@", "   -", "levy", "15 Feb 23:07", icon(0xF07B), "docs", bold-name: true)\
  #dir-entry("drwxr-xr-x@", "   -", "levy", "15 Feb 23:07", icon(0xF07B), "fonts", bold-name: true)\
  #dir-entry(".rw-r--r--@", "7.6k", "levy", "16 Feb 09:14", icon(0xE60A), "LICENSE")\
  #dir-entry(".rw-r--r--@", "1.3k", "levy", "16 Feb 09:14", icon(0xE612), "Makefile")\
  #dir-entry(".rw-r--r--@", "6.2k", "levy", "16 Feb 09:14", icon(0xE697), "pyproject.toml")\
  #dir-entry(".rw-r--r--@", "6.4k", "levy", "15 Feb 23:07", icon(0xE706), "README.md")\
  #dir-entry("drwxr-xr-x@", "   -", "levy", "15 Feb 23:07", icon(0xF07B), "scripts", bold-name: true)\
  #dir-entry("drwxr-xr-x@", "   -", "levy", "15 Feb 23:07", icon(0xF07B), "src", bold-name: true)\
  #dir-entry("drwxr-xr-x@", "   -", "levy", "15 Feb 23:07", icon(0xF07B), "tests", bold-name: true)\
  #dir-entry(".rw-r--r--@", " 63k", "levy", "16 Feb 09:14", icon(0xF023), "uv.lock")\
  ./docs/specimen/:\
  #dir-entry(".rw-r--r--@", "188k", "levy", "16 Feb 09:14", icon(0xE635), "planetaire-mono-specimen.pdf")\
  #dir-entry(".rw-r--r--@", "9.1k", "levy", "15 Feb 23:07", icon(0xE621), "planetaire-mono-specimen.typ")\

  #v(0.15cm)
  #prompt[python -c "print('Hello from Planetaire Mono!')"]\
  Hello from Planetaire Mono!\

  #v(0.15cm)
  #prompt[git log --oneline -3]\
  #t("5bd69c5", kerm.yellow) Switch B612 source to original polarsys/b612\
  #t("a1c8e3f", kerm.yellow) Add font comparison and regression detection\
  #t("e927d01", kerm.yellow) Refactor merge pipeline for original B612\
]

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

#let sample = "The quick brown fox jumps over the lazy dog"
#let digits = "0123456789 AaBbCcDd {[(>)]} !@#$%"

// Weight helper: label, sample, digits on consecutive lines.
#let weight-row(lbl, wt, it: false) = {
  label[#lbl]
  let st = if it { "italic" } else { "normal" }
  text(size: 12pt, weight: wt, style: st)[#sample]
  v(0.05cm)
  text(size: 12pt, weight: wt, style: st)[#digits]
  v(0.25cm)
}

#weight-row("REGULAR (400)", 400)
#weight-row("ITALIC (400)", 400, it: true)
#weight-row("MEDIUM (500)", 500)
#weight-row("MEDIUM ITALIC (500)", 500, it: true)
#weight-row("BOLD (700)", 700)
#weight-row("BOLD ITALIC (700)", 700, it: true)
#weight-row("EXTRABOLD (800)", 800)
#weight-row("EXTRABOLD ITALIC (800)", 800, it: true)

#v(0.3cm)

#label[SIZE COMPARISON: REGULAR AT VARIOUS SIZES]
#for size in (8, 9, 10, 11, 12) {
  text(size: eval(repr(size) + "pt"))[#sample]
  v(0.08cm)
}

#pagebreak()


// ─── Legibility ─────────────────────────────────────────────────

#section[Planetaire Legibility]

#label[CHARACTER DISAMBIGUATION]

// Large character pairs with gray labels.
#let disambig(chars, desc) = {
  grid(
    columns: (auto, 1fr),
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
  radius: 4pt,
  width: 100%,
)[
  #set text(size: 7.5pt)
  #set par(leading: 0.5em, justify: false)

  #text(weight: 700)[NAME]\
  #h(2.5em)#text(weight: 700)[ascii] -- octal, hexadecimal and decimal ASCII character sets\
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

#section[Planetaire Provenance & License]

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
  post-processing fixes. Medium weights are generated from
  Regular, and ExtraBold from Bold, via FontForge emboldening.
]

#v(0.5cm)
#text(size: 11pt, weight: 700)[License]
#v(0.2cm)
#text(size: 10pt)[
  Planetaire Mono is released under the *SIL Open Font License 1.1 (OFL-1.1)*.

  The OFL allows free use, modification, and redistribution of the font, including
  in commercial products, provided that modified versions are not sold by themselves
  and carry a different name.

  The constituent fonts carry the following licenses:
  - *B612 Mono*: SIL Open Font License 1.1 + Eclipse Public License 2.0
  - *Hack*: MIT License
  - *Nerd Fonts* patches: MIT License
]

// Footer is now on every page via the page footer setting.
