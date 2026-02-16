// Planetaire Mono - Font Specimen
// Build: planetaire build specimen

#let version = "0.1.0"

#set page(
  paper: "a4",
  margin: (top: 2cm, bottom: 2cm, left: 2.5cm, right: 2.5cm),
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
  v(0.15cm)
}

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
    B612 letterforms\
    Hack infrastructure\
    Nerd Font icons
  ]

  #v(0.8cm)
  #text(size: 10pt, fill: rgb("#999"))[Version #version]
]

#v(1.5cm)

#text(size: 10pt)[
  Planetaire Mono is a composite monospace font that merges the highly legible
  letterforms of B612, a typeface designed by Intactile Design for Airbus cockpit
  displays, with Hack Nerd Font's complete infrastructure: punctuation, symbols,
  and 12,000+ developer icons.
]

#v(0.3cm)

#text(size: 10pt)[
  The result is a font optimized for terminal and editor use that combines
  aviation-grade character clarity with full programming language coverage.
  The name is a nod to asteroid B-612 from _The Little Prince_.
]

#v(1.5cm)

#grid(
  columns: (1fr, 1fr),
  gutter: 1.5cm,
  [
    #text(size: 9pt, fill: rgb("#666"))[
      *Weights*\
      #text(weight: "regular")[Regular] (400)\
      #text(weight: "regular", style: "italic")[Italic] (400)\
      #text(weight: "bold")[Bold] (700)\
      #text(weight: "bold", style: "italic")[Bold Italic] (700)\
      #text(weight: 800)[ExtraBold] (800)\
      #text(weight: 800, style: "italic")[ExtraBold Italic] (800)
    ]
  ],
  [
    #text(size: 9pt, fill: rgb("#666"))[
      *Glyph Sources*\
      Letters A–Z, a–z from B612\
      Digits 1–9 from B612, 0 from Hack\
      Extended Latin, Greek, Cyrillic from B612\
      Punctuation and symbols from Hack\
      12,000+ Nerd Font icons from Hack
    ]
  ],
)

#pagebreak()


// ─── Page 2: Text Showcase ──────────────────────────────────────

#section[Text Showcase]

#text(size: 9pt, fill: rgb("#999"))[
  Planetaire Mono at various sizes, showing B612's distinctive letterforms
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

#text(size: 9pt, fill: rgb("#999"))[FRENCH · GERMAN · SPANISH · TURKISH]
#v(0.15cm)
#text(size: 11pt)[
  Les naïfs ægithales hâtifs pondsjflam au zéphyr joyeux. Falsches Üben von
  Xylophonmusik quält jeden größeren Zwerg. El veloz murciélago hindú comía
  feliz cardillo y kiwi. Pijamalı hasta yağız şoföre çabucak güvendi.
]
#v(0.4cm)

#text(size: 9pt, fill: rgb("#999"))[GREEK]
#v(0.15cm)
#text(size: 11pt)[
  Ξεσκεπάζω τὴν ψυχοφθόρα βδελυγμία.
  Θlongest ελληνική πρόταση που χρησιμοποιεί όλα τα γράμματα.
]
#v(0.4cm)

#text(size: 9pt, fill: rgb("#999"))[CYRILLIC]
#v(0.15cm)
#text(size: 11pt)[
  Съешь же ещё этих мягких французских булок, да выпей чаю.
  Широкая электрификация южных губерний даст мощный толчок подъёму
  сельского хозяйства.
]

#pagebreak()


// ─── Page 3: Code Sample ────────────────────────────────────────

#section[Code Sample]

#text(size: 9pt, fill: rgb("#999"))[
  Syntax highlighting uses the Kerm terminal color palette.
]
#v(0.2cm)

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

#v(0.4cm)

// Rust sample with manual Kerm-colored tokens.
#code-block((
  (text(weight: "bold")[use], kerm.magenta), (" std::collections::", none),
  ("HashMap", kerm.cyan), (";\n\n", none),

  (text(weight: "bold")[fn], kerm.magenta), (" fibonacci", kerm.yellow),
  ("(n: ", none), ("u64", kerm.cyan), (") -> ", none),
  ("u64", kerm.cyan), (" {\n", none),
  ("    ", none), (text(weight: "bold")[match], kerm.magenta), (" n {\n", none),
  ("        ", none), ("0", kerm.cyan), (" => ", none), ("0", kerm.cyan), (",\n", none),
  ("        ", none), ("1", kerm.cyan), (" => ", none), ("1", kerm.cyan), (",\n", none),
  ("        _ => fibonacci(n - ", none), ("1", kerm.cyan),
  (") + fibonacci(n - ", none), ("2", kerm.cyan), ("),\n", none),
  ("    }\n}\n\n", none),

  (text(weight: "bold")[fn], kerm.magenta), (" main", kerm.yellow), ("() {\n", none),
  ("    ", none), (text(weight: "bold")[let], kerm.magenta),
  (" values: ", none), ("Vec", kerm.cyan), ("<", none),
  ("u64", kerm.cyan), ("> = (", none), ("0", kerm.cyan),
  ("..", none), ("20", kerm.cyan), (").map(fibonacci).collect();\n", none),
  ("    println!(", none), ("\"Fibonacci: {:?}\"", kerm.green),
  (", values);\n}\n", none),
))

#pagebreak()


// ─── Page 4: Terminal ───────────────────────────────────────────

#section[Terminal]

#text(size: 9pt, fill: rgb("#999"))[
  Simulated terminal output using the Kerm color palette,
  showing how Planetaire Mono renders a typical `eza` directory listing.
]
#v(0.2cm)

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

// eza directory entry helpers.
#let dir-entry(perms, size, user, date, ic, name, bold-name: false) = {
  t(perms, kerm.bright-black)
  t(" ", kerm.fg)
  tb(size, kerm.green)
  t(" ", kerm.fg)
  tb(user, kerm.yellow)
  t(" ", kerm.fg)
  t(date, kerm.blue)
  t(" ", kerm.fg)
  t(ic, kerm.cyan)
  t(" ", kerm.fg)
  if bold-name { tb(name, kerm.fg) } else { t(name, kerm.fg) }
}

#block(
  fill: kerm.bg,
  inset: (x: 1.2em, y: 1em),
  radius: 4pt,
  width: 100%,
)[
  #set text(size: 8.5pt, fill: kerm.fg)
  #set par(leading: 0.4em)

  #prompt[eza -l --icons=always . ./docs/images ./docs/specimen/]\
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
  ./docs/images:\
  #dir-entry(".rw-r--r--@", " 50k", "levy", "15 Feb 23:07", icon(0xE64A), "features.png")\
  #dir-entry(".rw-r--r--@", " 59k", "levy", "15 Feb 23:07", icon(0xE64A), "hero.png")\
  #dir-entry(".rw-r--r--@", " 59k", "levy", "15 Feb 23:07", icon(0xE64A), "terminal-bold.png")\
  #dir-entry(".rw-r--r--@", "105k", "levy", "15 Feb 23:07", icon(0xE64A), "weights.png")\
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


// ─── Page 5: Character Set ──────────────────────────────────────

#section[Character Set]

#label[BASIC LATIN UPPERCASE: from B612]
#text(size: 16pt)[A B C D E F G H I J K L M N O P Q R S T U V W X Y Z]
#v(0.3cm)

#label[BASIC LATIN LOWERCASE: from B612]
#text(size: 16pt)[a b c d e f g h i j k l m n o p q r s t u v w x y z]
#v(0.3cm)

#label[DIGITS: 1–9 from B612, 0 from Hack (slashed for disambiguation)]
#text(size: 16pt)[0 1 2 3 4 5 6 7 8 9]
#v(0.3cm)

#label[PUNCTUATION AND SYMBOLS: from Hack]
#text(size: 14pt)[! " \# \$ % & ' ( ) \* \+ , \- . / : ; < = > ? \@ \[ \\ \] ^ \_ \` \{ | \} \~]
#v(0.3cm)

#label[EXTENDED LATIN: from B612]
#text(size: 12pt)[À Á Â Ã Ä Å Æ Ç È É Ê Ë Ì Í Î Ï Ð Ñ Ò Ó Ô Õ Ö Ø Ù Ú Û Ü Ý Þ ß à á â ã ä å æ ç è é ê ë ì í î ï ð ñ ò ó ô õ ö ø ù ú û ü ý þ ÿ]
#v(0.15cm)
#text(size: 12pt)[Ā ā Ă ă Ą ą Ć ć Ĉ ĉ Ċ ċ Č č Ď ď Đ đ Ē ē Ĕ ĕ Ė ė Ę ę Ě ě Ğ ğ Ġ ġ Ģ ģ Ĥ ĥ Ħ ħ Ĩ ĩ Ī ī Ĭ ĭ Į į İ ı Ĳ ĳ Ĵ ĵ Ķ ķ]
#v(0.3cm)

#label[GREEK: from B612]
#text(size: 12pt)[Α Β Γ Δ Ε Ζ Η Θ Ι Κ Λ Μ Ν Ξ Ο Π Ρ Σ Τ Υ Φ Χ Ψ Ω]
#v(0.1cm)
#text(size: 12pt)[α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ τ υ φ χ ψ ω]
#v(0.3cm)

#label[CYRILLIC: from B612]
#text(size: 12pt)[А Б В Г Д Е Ж З И Й К Л М Н О П Р С Т У Ф Х Ц Ч Ш Щ Ъ Ы Ь Э Ю Я]
#v(0.1cm)
#text(size: 12pt)[а б в г д е ж з и й к л м н о п р с т у ф х ц ч ш щ ъ ы ь э ю я]

#pagebreak()


// ─── Page 6: Weight Comparison ──────────────────────────────────

#section[Weight Comparison]

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


// ─── Page 7: Feature Showcase ───────────────────────────────────

#section[Feature Showcase]

#label[CHARACTER DISAMBIGUATION]
#v(0.1cm)

// Large character pairs with gray labels.
#let disambig(chars, desc) = {
  grid(
    columns: (auto, 1fr),
    column-gutter: 1cm,
    align: horizon,
    text(size: 28pt)[#chars],
    text(size: 9pt, fill: rgb("#999"))[#desc],
  )
  v(0.2cm)
}

#disambig[I l 1 |][uppercase I · lowercase l · digit 1 · pipe]
#disambig[O 0 o][uppercase O · digit 0 · lowercase o]
#disambig[r n m][r · n · m (clearly distinct in B612)]
#disambig[5 S 8 B][digit 5 vs S · digit 8 vs B]
#disambig[2 Z 6 G][digit 2 vs Z · digit 6 vs G]

#v(0.5cm)

#label[BRACKET AND DELIMITER PAIRS]
#v(0.1cm)
#text(size: 20pt)[
  ( ) \{ \} \[ \] < > « » ‹ ›
]

#v(0.5cm)

#label[MATHEMATICAL AND PROGRAMMING OPERATORS]
#v(0.1cm)
#text(size: 20pt)[\+ \- \* / = ≠ ≤ ≥ ± × ÷ → ← ↑ ↓]

#v(0.5cm)

#label[BOX DRAWING AND BLOCK ELEMENTS]
#v(0.1cm)
#text(size: 16pt)[
  ─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼ ═ ║ ╔ ╗ ╚ ╝ ╠ ╣ ╦ ╩ ╬ ▀ ▄ █ ▌ ▐ ░ ▒ ▓
]

#pagebreak()


// ─── Page 8: Nerd Font Icons ────────────────────────────────────

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
#label[WEATHER]
#icon-grid((
  (0xE30D, "sun"), (0xE312, "cloud"), (0xE318, "rain"),
  (0xE31A, "snow"), (0xE320, "fog"), (0xE335, "lightning"),
  (0xE33D, "wind"), (0xE342, "hot"), (0xE343, "cold"),
  (0xE344, "windy"), (0xE366, "moon"), (0xE36E, "sunrise"),
  (0xE370, "sunset"), (0xE3A9, "humidity"),
))

#pagebreak()


// ─── Page 9: Provenance & License ───────────────────────────────

#section[Provenance & License]

#text(size: 11pt, weight: 700)[Source Fonts]
#v(0.2cm)

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt + rgb("#ccc"),
  inset: 8pt,
  [*B612 Mono*], [
    Designed by Intactile Design for Airbus. Optimized for legibility in
    cockpit displays. Planetaire Mono takes its letters (A–Z, a–z),
    digits 1–9, and extended Latin/Greek/Cyrillic glyphs from B612.
  ],
  [*Hack*], [
    Chris Simpkins' typeface designed for source code. Provides the
    base font structure: punctuation, symbols, digit 0, and overall metrics.
  ],
  [*Nerd Fonts*], [
    Ryan McIntyre's icon patching project. 12,000+ developer icons
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
  merges B612 letter glyphs by Unicode range, renames the result, and
  applies post-processing fixes. ExtraBold weights are generated from Bold
  via FontForge emboldening.
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

#v(1cm)
#align(center)[
  #text(size: 9pt, fill: rgb("#999"))[
    Planetaire Mono · github.com/jlevy/planetaire · OFL-1.1
  ]
]
