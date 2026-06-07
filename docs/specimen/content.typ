// Shared specimen content: palettes, helpers, and the reusable blocks used by both
// the PDF specimen (planetaire-mono-specimen.typ) and the README image cards (card.typ).
// Defining them once keeps the home-page images in sync with the PDF.
//
// Every content block takes a palette `p` (pal-dark or pal-light) so the same source
// renders a matched dark/light pair. Defaults match the PDF: terminal and code are
// dark; prose, weights, and legibility sit on the light page.

#let font-family = "Planetaire Mono Extended"

// Paired palettes. Syntax colors are the Kerm terminal theme (dark) and a darkened
// Kerm variant tuned for light backgrounds (light).
#let pal-dark = (
  page:         rgb("#0d1117"),
  term-bg:      rgb("#000000"),
  fg:           rgb("#ffffff"),
  muted:        rgb("#8b949e"),
  comment:      rgb("#6e7681"),
  red:          rgb("#eb8f83"),
  green:        rgb("#6dc481"),
  yellow:       rgb("#caa94e"),
  blue:         rgb("#96aced"),
  magenta:      rgb("#dc8dd6"),
  cyan:         rgb("#55bdcd"),
  bright-black: rgb("#bababa"),
)
#let pal-light = (
  page:         white,
  term-bg:      rgb("#f6f8fa"),
  fg:           rgb("#24292f"),
  muted:        rgb("#6e7781"),
  comment:      rgb("#6e7781"),
  red:          rgb("#a8342a"),
  green:        rgb("#1a7f37"),
  yellow:       rgb("#7d5e00"),
  blue:         rgb("#0550ae"),
  magenta:      rgb("#8250df"),
  cyan:         rgb("#0e6b7a"),
  bright-black: rgb("#57606a"),
)

// Section heading (used on the white specimen pages).
#let section(title) = {
  text(size: 16pt, weight: 700)[#title]
  v(0.3cm)
  line(length: 100%, stroke: 0.5pt + rgb("#ccc"))
  v(0.5cm)
}

// Small gray label (white specimen pages).
#let label(body) = {
  text(size: 8pt, fill: rgb("#999"))[#body]
  v(0.1cm)
}

// Spaced character display: inserts thin gaps between characters.
#let spaced(s, gap: 0.25em) = s.clusters().join(h(gap))

// Colored / bold span helpers.
#let t(body, color) = text(fill: color)[#body]
#let tb(body, color) = text(fill: color, weight: "bold")[#body]

// Syntax-highlighted code block. `tokens` is a list of (text, color) pairs;
// use none for the default foreground.
#let code-block(p, tokens) = block(
  fill: p.term-bg,
  inset: (x: 1.2em, y: 1em),
  radius: 4pt,
  width: 100%,
)[
  #set text(size: 9.5pt, fill: p.fg)
  #for tok in tokens {
    let (s, c) = tok
    if c == none { s } else { text(fill: c)[#s] }
  }
]

// Shell prompt helper.
#let prompt(p, cmd) = {
  tb("planetaire", p.blue)
  text(weight: "bold")[ \$ ]
  cmd
}

// Nerd Font icon helper.
#let icon(cp) = str.from-unicode(cp)

// eza directory entry with box-wrapped spans for precise alignment.
// The permissions field is a fixed-width box (it is the only column whose
// leading glyph varies: "." for files vs "d" for dirs). Pinning its width
// keeps every following column aligned even if "." and "d" differ in advance.
#let dir-entry(p, perms, size, user, date, ic, name, bold-name: false) = {
  box(width: 7em)[#t(perms, p.bright-black)]
  box[#t(" ", p.fg)]
  box[#tb(size, p.green)]
  box[#t(" ", p.fg)]
  box[#tb(user, p.yellow)]
  box[#t(" ", p.fg)]
  box[#t(date, p.blue)]
  box[#t(" ", p.fg)]
  box[#t(ic, p.cyan)]
  box[#t(" ", p.fg)]
  if bold-name { box[#tb(name, p.fg)] } else { box[#t(name, p.fg)] }
}

// ── Reusable content blocks ─────────────────────────────────────

// Home-page header banner (white background): the font name and lineage set in
// Planetaire Mono itself. Rendered to docs/images/header.png by `build images`.
#let header-card(p: pal-light) = align(center)[
  #v(1.5cm)
  #text(size: 48pt, weight: 500, fill: p.fg)[Planetaire Mono]
  #v(0.1cm)
  #text(size: 13pt, weight: 700, fill: p.fg)[
    B612 LETTERFORMS \u{00B7} HACK INFRASTRUCTURE \u{00B7} NERD FONT ICONS
  ]
  #v(0.4cm)
  #text(size: 13pt, weight: 500, style: "italic", fill: p.fg)[
    A beautiful, highly legible monospace font for terminals, editors, and agentic work
  ]
  #v(1.1cm)
]

// Syntax-highlighted Python sample.
#let orbit-code(p: pal-dark) = code-block(p, (
  (text(weight: "bold")[import], p.magenta), (" math", none), ("\n\n", none),
  (text(weight: "bold")[def], p.magenta), (" analyze_trajectory", none),
  ("(", none), ("altitude", none), (": ", none),
  ("float", p.cyan), (", ", none), ("velocity", none), (": ", none),
  ("float", p.cyan), (") -> ", none), ("dict", p.cyan), (":\n", none),
  ("    ", none), ("\"\"\"Calculate orbital parameters.\"\"\"", p.green), ("\n\n", none),
  ("    G ", none), ("= ", none), ("6.674e-11", p.cyan),
  ("  ", none), ("# gravitational constant", p.comment), ("\n", none),
  ("    M ", none), ("= ", none), ("5.972e24", p.cyan), ("\n\n", none),
  ("    ", none), (text(weight: "bold")[if], p.magenta),
  (" altitude > ", none), ("400_000", p.cyan), (":\n", none),
  ("        orbit_type ", none), ("= ", none),
  ("\"LEO\"", p.green), ("\n", none),
  ("    ", none), (text(weight: "bold")[elif], p.magenta),
  (" altitude > ", none), ("35_786_000", p.cyan), (":\n", none),
  ("        orbit_type ", none), ("= ", none),
  ("\"GEO\"", p.green), ("\n\n", none),
  ("    period ", none), ("= ", none), ("2", p.cyan),
  (" * math.pi * math.sqrt(altitude**", none), ("3", p.cyan),
  (" / (G * M))\n\n", none),
  ("    ", none), (text(weight: "bold")[return], p.magenta),
  (" {", none), ("\"type\"", p.green), (": orbit_type, ", none),
  ("\"period\"", p.green), (": period, ", none),
  ("\"v\"", p.green), (": velocity}\n", none),
))

// Mock terminal session (eza --icons, python, git log).
#let terminal-mockup(p: pal-dark) = block(
  fill: p.term-bg,
  inset: (x: 1.2em, y: 1em),
  radius: 4pt,
  width: 100%,
)[
  #set text(size: 8.5pt, fill: p.fg)
  #set par(leading: 0.4em, justify: false)
  // Terminal output is literal: keep straight quotes (no smart curly quotes).
  #set smartquote(enabled: false)

  #prompt(p)[eza -l \-\-icons=always . ./docs/specimen/]\
  .:\
  #dir-entry(p, "drwxr-xr-x@", "   -", "levy", "15 Feb 23:07", icon(0xF07B), "devtools", bold-name: true)\
  #dir-entry(p, "drwxr-xr-x@", "   -", "levy", "15 Feb 23:07", icon(0xF07B), "docs", bold-name: true)\
  #dir-entry(p, "drwxr-xr-x@", "   -", "levy", "15 Feb 23:07", icon(0xF07B), "fonts", bold-name: true)\
  #dir-entry(p, ".rw-r--r--@", "7.6k", "levy", "16 Feb 09:14", icon(0xE60A), "LICENSE")\
  #dir-entry(p, ".rw-r--r--@", "1.3k", "levy", "16 Feb 09:14", icon(0xE612), "Makefile")\
  #dir-entry(p, ".rw-r--r--@", "6.2k", "levy", "16 Feb 09:14", icon(0xE697), "pyproject.toml")\
  #dir-entry(p, ".rw-r--r--@", "6.4k", "levy", "15 Feb 23:07", icon(0xE706), "README.md")\
  #dir-entry(p, "drwxr-xr-x@", "   -", "levy", "15 Feb 23:07", icon(0xF07B), "src", bold-name: true)\
  #dir-entry(p, ".rw-r--r--@", " 63k", "levy", "16 Feb 09:14", icon(0xF023), "uv.lock")\
  ./docs/specimen/:\
  #dir-entry(p, ".rw-r--r--@", "188k", "levy", "16 Feb 09:14", icon(0xE635), "planetaire-mono-specimen.pdf")\
  #dir-entry(p, ".rw-r--r--@", "9.1k", "levy", "15 Feb 23:07", icon(0xE621), "planetaire-mono-specimen.typ")\

  #v(0.15cm)
  #prompt(p)[python -c "print('Hello from Planetaire Mono!')"]\
  Hello from Planetaire Mono!\

  #v(0.15cm)
  #prompt(p)[git log \-\-oneline -3]\
  #t("5bd69c5", p.yellow) Switch B612 source to original polarsys/b612\
  #t("a1c8e3f", p.yellow) Add font comparison and regression detection\
  #t("e927d01", p.yellow) Refactor merge pipeline for original B612\
]

// Alan Turing, "Computing Machinery and Intelligence" (1950).
#let turing-passage(p: pal-light, size: 10.5pt) = text(size: size, fill: p.fg)[
  I propose to consider the question, \u{201C}Can machines think?\u{201D} This should
  begin with definitions of the meaning of the terms \u{201C}machine\u{201D} and
  \u{201C}think.\u{201D} The definitions might be framed so as to reflect so far as
  possible the normal use of the words, but this attitude is dangerous.
  If the meaning of the words \u{201C}machine\u{201D} and \u{201C}think\u{201D} are to be found
  by examining how they are commonly used it is difficult to escape the
  conclusion that the meaning and the answer to the question, \u{201C}Can
  machines think?\u{201D} is to be sought in a statistical survey such as a
  Gallup poll. But this is absurd.
]

// Weight ladder: every variant on a sample line plus a digits/symbols line.
#let weight-ladder(p: pal-light) = {
  let sample = "The quick brown fox jumps over the lazy dog"
  let digits = "0123456789 AaBbCcDd {[(>)]} !@#$%"
  let row(lbl, wt, it: false) = {
    text(size: 8pt, fill: p.muted)[#lbl]
    v(0.1cm)
    let st = if it { "italic" } else { "normal" }
    text(size: 12pt, weight: wt, style: st, fill: p.fg)[#sample]
    v(0.05cm)
    text(size: 12pt, weight: wt, style: st, fill: p.fg)[#digits]
    v(0.25cm)
  }
  row("REGULAR (400)", 400)
  row("ITALIC (400)", 400, it: true)
  row("MEDIUM (500)", 500)
  row("MEDIUM ITALIC (500)", 500, it: true)
  row("BOLD (700)", 700)
  row("BOLD ITALIC (700)", 700, it: true)
  row("EXTRABOLD (800)", 800)
  row("EXTRABOLD ITALIC (800)", 800, it: true)
}

// Legibility: confusable-character disambiguation plus the dotted-zero variants.
#let legibility-pairs(p: pal-light) = {
  // Fixed-width glyph column so every gray label starts at the same x.
  let disambig(chars, desc) = {
    grid(
      columns: (4.5cm, 1fr),
      column-gutter: 1cm,
      align: horizon,
      text(size: 28pt, fill: p.fg)[#chars],
      text(size: 9pt, fill: p.muted)[#desc],
    )
    v(0.15cm)
  }
  text(size: 8pt, fill: p.muted, weight: "bold")[KEY GLYPH COMPARISONS]
  v(0.1cm)
  disambig[I l 1 |][uppercase I \u{00B7} lowercase l \u{00B7} digit 1 \u{00B7} pipe]
  disambig[O 0 o][uppercase O \u{00B7} digit 0 \u{00B7} lowercase o]
  disambig[r n m][r \u{00B7} n \u{00B7} m, distinct in B612]
  disambig[5 S 8 B][digit 5 vs S \u{00B7} digit 8 vs B]
  disambig[2 Z 6 G][digit 2 vs Z \u{00B7} digit 6 vs G]

  v(0.3cm)
  text(size: 8pt, fill: p.muted, weight: "bold")[ZERO DOT VARIANTS (OpenType)]
  v(0.1cm)
  grid(
    columns: (1fr, 1fr),
    gutter: 1cm,
    [
      #text(size: 9pt, fill: p.muted, weight: "bold")[Default (circle dot)]
      #v(0.1cm)
      #text(size: 36pt, fill: p.fg)[0] #h(0.5cm) #text(size: 18pt, fill: p.fg)[0 O o]
      #v(0.1cm)
      #text(size: 11pt, fill: p.fg)[FL350 FL850 10.0.0.1]
    ],
    [
      #text(size: 9pt, fill: p.muted, weight: "bold")[ss01 / zero (rectangle dot)]
      #v(0.1cm)
      #set text(features: ("ss01",))
      #text(size: 36pt, fill: p.fg)[0] #h(0.5cm) #text(size: 18pt, fill: p.fg)[0 O o]
      #v(0.1cm)
      #text(size: 11pt, fill: p.fg)[FL350 FL850 10.0.0.1]
    ],
  )
}

// ── QA surface ──────────────────────────────────────────────────
// A visual proof of the monospace invariant. Each glyph sits in a box drawn at
// its own advance width (the red rules mark the true cell edges). Because the
// font is monospace, every cell is the same width; because nothing is trimmed,
// all ink sits between its rules. Box-drawing and powerline glyphs are meant to
// FILL the cell (they tile), so they reach -- and touch -- the rules by design.

#let _qa_rule = 0.4pt + rgb("#d83933")

// One glyph in a box drawn at its advance width, with cell-edge rules.
#let qa-cell(p, ch, size: 26pt) = box(
  stroke: (left: _qa_rule, right: _qa_rule),
  inset: (x: 0pt, y: 2pt),
)[#text(size: size, fill: p.fg)[#ch]]

#let coding-width-grid(p: pal-light) = {
  let row(s) = {
    s.clusters().map(c => qa-cell(p, c)).join(h(5pt))
    v(0.2cm)
  }
  text(size: 8pt, fill: p.muted, weight: "bold")[
    STANDARD CODING CHARACTERS: TRUE CELL WIDTHS
  ]
  v(0.05cm)
  text(size: 7.5pt, fill: p.muted)[
    Red rules mark each glyph's advance. Equal-width cells with ink inside mean a
    clean monospace grid, nothing trimmed.
  ]
  v(0.2cm)
  row("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
  row("abcdefghijklmnopqrstuvwxyz")
  row("0123456789")
  row("!\"#$%&'()*+,-./:;<=>?@")
  row("[\\]^_`{|}~")
  v(0.1cm)
  text(size: 7.5pt, fill: p.muted)[Cell-filling glyphs (box-drawing, powerline) reach the rules by design:]
  v(0.15cm)
  row("\u{2500}\u{2502}\u{250C}\u{2510}\u{2514}\u{2518}\u{251C}\u{2524}\u{252C}\u{2534}\u{253C}\u{2588}\u{2593}\u{2592}\u{2591}\u{E0B0}\u{E0B2}")
}

// Same coding string in every weight, each capped by a rule at its right edge.
// Monospace => every line is the same width => the right rules line up.
#let weight-alignment(p: pal-light) = {
  let sample = "if (x == 0) { i = l1|O; }"
  let row(lbl, wt, it: false) = {
    let st = if it { "italic" } else { "normal" }
    grid(
      columns: (3cm, auto),
      align: (left + horizon, left + horizon),
      text(size: 7.5pt, fill: p.muted)[#lbl],
      box(stroke: (right: _qa_rule), inset: (right: 0pt, y: 2.5pt))[
        #text(size: 13pt, weight: wt, style: st, fill: p.fg)[#sample]
      ],
    )
    v(0.12cm)
  }
  text(size: 8pt, fill: p.muted, weight: "bold")[WEIGHT ALIGNMENT: EVERY WEIGHT IS THE SAME WIDTH]
  v(0.05cm)
  text(size: 7.5pt, fill: p.muted)[
    The same string in all eight variants; the red rule marks each line's right
    edge. A single vertical line means identical width across every weight.
  ]
  v(0.25cm)
  row("REGULAR (400)", 400)
  row("ITALIC (400)", 400, it: true)
  row("MEDIUM (500)", 500)
  row("MEDIUM ITALIC (500)", 500, it: true)
  row("BOLD (700)", 700)
  row("BOLD ITALIC (700)", 700, it: true)
  row("EXTRABOLD (800)", 800)
  row("EXTRABOLD ITALIC (800)", 800, it: true)
}
