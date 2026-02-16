// Planetaire Mono — Font Specimen Sheet
// Compile: typst compile planetaire-mono-specimen.typ
// Requires: Planetaire Mono font files in ../../fonts/output/

#let font-dir = "../../fonts/output/"
#let version = "1.0.0"

#set page(
  paper: "a4",
  margin: (top: 2cm, bottom: 2cm, left: 2.5cm, right: 2.5cm),
)

#set text(font: "Planetaire Mono", size: 10pt)

// --- Page 1: Cover ---

#v(4cm)

#align(center)[
  #text(size: 36pt, weight: 800)[Planetaire Mono]

  #v(0.5cm)
  #text(size: 14pt, fill: rgb("#666"))[
    B612 letterforms. Hack infrastructure. Nerd Font icons.
  ]

  #v(1cm)
  #text(size: 11pt, fill: rgb("#999"))[
    Version #version
  ]

  #v(2cm)

  #grid(
    columns: (1fr, 1fr),
    gutter: 1cm,
    align(left)[
      #text(size: 9pt, fill: rgb("#666"))[
        *Weights*\
        Regular (400)\
        Italic (400)\
        Bold (700)\
        Bold Italic (700)\
        ExtraBold (800)\
        ExtraBold Italic (800)
      ]
    ],
    align(left)[
      #text(size: 9pt, fill: rgb("#666"))[
        *Coverage*\
        B612 letters, digits, extended Latin\
        Greek and Coptic, Cyrillic\
        Hack punctuation and symbols\
        12,000+ Nerd Font icons\
        OpenType: calt, zero, ezer
      ]
    ],
  )
]

#pagebreak()

// --- Page 2: Character Set ---

#text(size: 16pt, weight: 800)[Character Set]
#v(0.3cm)
#line(length: 100%, stroke: 0.5pt + rgb("#ccc"))
#v(0.5cm)

#text(size: 9pt, fill: rgb("#666"))[BASIC LATIN UPPERCASE]
#v(0.2cm)
#text(size: 18pt)[A B C D E F G H I J K L M N O P Q R S T U V W X Y Z]
#v(0.5cm)

#text(size: 9pt, fill: rgb("#666"))[BASIC LATIN LOWERCASE]
#v(0.2cm)
#text(size: 18pt)[a b c d e f g h i j k l m n o p q r s t u v w x y z]
#v(0.5cm)

#text(size: 9pt, fill: rgb("#666"))[DIGITS]
#v(0.2cm)
#text(size: 18pt)[0 1 2 3 4 5 6 7 8 9]
#v(0.5cm)

#text(size: 9pt, fill: rgb("#666"))[PUNCTUATION AND SYMBOLS (from Hack)]
#v(0.2cm)
#text(size: 18pt)[! " \# \$ % & ' ( ) \* + , - . / : ; < = > ? \@ \[ \\ \] ^ \_ \` \{ | \} ~]
#v(0.5cm)

#text(size: 9pt, fill: rgb("#666"))[EXTENDED LATIN]
#v(0.2cm)
#text(size: 14pt)[À Á Â Ã Ä Å Æ Ç È É Ê Ë Ì Í Î Ï Ð Ñ Ò Ó Ô Õ Ö Ø Ù Ú Û Ü Ý Þ ß]
#v(0.2cm)
#text(size: 14pt)[à á â ã ä å æ ç è é ê ë ì í î ï ð ñ ò ó ô õ ö ø ù ú û ü ý þ ÿ]
#v(0.2cm)
#text(size: 14pt)[Ā ā Ă ă Ą ą Ć ć Ĉ ĉ Ċ ċ Č č Ď ď Đ đ Ē ē Ĕ ĕ Ė ė Ę ę Ě ě]
#v(0.5cm)

#text(size: 9pt, fill: rgb("#666"))[GREEK]
#v(0.2cm)
#text(size: 14pt)[Α Β Γ Δ Ε Ζ Η Θ Ι Κ Λ Μ Ν Ξ Ο Π Ρ Σ Τ Υ Φ Χ Ψ Ω]
#v(0.2cm)
#text(size: 14pt)[α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ τ υ φ χ ψ ω]
#v(0.5cm)

#text(size: 9pt, fill: rgb("#666"))[CYRILLIC]
#v(0.2cm)
#text(size: 14pt)[А Б В Г Д Е Ж З И Й К Л М Н О П Р С Т У Ф Х Ц Ч Ш Щ Ъ Ы Ь Э Ю Я]
#v(0.2cm)
#text(size: 14pt)[а б в г д е ж з и й к л м н о п р с т у ф х ц ч ш щ ъ ы ь э ю я]

#pagebreak()

// --- Page 3: Weight Comparison ---

#text(size: 16pt, weight: 800)[Weight Comparison]
#v(0.3cm)
#line(length: 100%, stroke: 0.5pt + rgb("#ccc"))
#v(0.5cm)

#let sample = "The quick brown fox jumps over the lazy dog"
#let digits = "0123456789 AaBbCcDd {[(>)]} !@#$%"

#text(size: 9pt, fill: rgb("#666"))[REGULAR (400)]
#v(0.2cm)
#text(size: 14pt, weight: 400)[#sample]
#v(0.1cm)
#text(size: 14pt, weight: 400)[#digits]
#v(0.5cm)

#text(size: 9pt, fill: rgb("#666"))[ITALIC (400)]
#v(0.2cm)
#text(size: 14pt, weight: 400, style: "italic")[#sample]
#v(0.1cm)
#text(size: 14pt, weight: 400, style: "italic")[#digits]
#v(0.5cm)

#text(size: 9pt, fill: rgb("#666"))[BOLD (700)]
#v(0.2cm)
#text(size: 14pt, weight: 700)[#sample]
#v(0.1cm)
#text(size: 14pt, weight: 700)[#digits]
#v(0.5cm)

#text(size: 9pt, fill: rgb("#666"))[BOLD ITALIC (700)]
#v(0.2cm)
#text(size: 14pt, weight: 700, style: "italic")[#sample]
#v(0.1cm)
#text(size: 14pt, weight: 700, style: "italic")[#digits]
#v(0.5cm)

#text(size: 9pt, fill: rgb("#666"))[EXTRABOLD (800) — RECOMMENDED FOR TERMINAL BOLD]
#v(0.2cm)
#text(size: 14pt, weight: 800)[#sample]
#v(0.1cm)
#text(size: 14pt, weight: 800)[#digits]
#v(0.5cm)

#text(size: 9pt, fill: rgb("#666"))[EXTRABOLD ITALIC (800)]
#v(0.2cm)
#text(size: 14pt, weight: 800, style: "italic")[#sample]
#v(0.1cm)
#text(size: 14pt, weight: 800, style: "italic")[#digits]

#v(1cm)

#text(size: 9pt, fill: rgb("#666"))[SIZE COMPARISON — EXTRABOLD AT VARIOUS SIZES]
#v(0.3cm)
#for size in (8, 10, 12, 14, 16, 18, 22) {
  text(size: eval(repr(size) + "pt"), weight: 800)[#sample]
  v(0.3cm)
}

#pagebreak()

// --- Page 4: Code Sample ---

#text(size: 16pt, weight: 800)[Code Sample]
#v(0.3cm)
#line(length: 100%, stroke: 0.5pt + rgb("#ccc"))
#v(0.5cm)

#block(
  fill: rgb("#16161c"),
  inset: 1.5em,
  radius: 4pt,
  width: 100%,
)[
  #set text(size: 10pt, fill: rgb("#dcdcdc"))
  ```python
  def analyze_trajectory(altitude: float, velocity: float) -> dict:
      """Calculate orbital parameters from trajectory data."""

      G = 6.674e-11  # gravitational constant
      mass_earth = 5.972e24

      if altitude > 400_000:
          orbit_type = "LEO"  # Low Earth Orbit
      elif altitude > 35_786_000:
          orbit_type = "GEO"  # Geostationary

      period = 2 * math.pi * math.sqrt(altitude**3 / (G * mass_earth))

      return {"type": orbit_type, "period": period, "v": velocity}
  ```
]

#v(0.5cm)

#block(
  fill: rgb("#16161c"),
  inset: 1.5em,
  radius: 4pt,
  width: 100%,
)[
  #set text(size: 10pt, fill: rgb("#dcdcdc"))
  ```rust
  fn fibonacci(n: u64) -> u64 {
      match n {
          0 => 0,
          1 => 1,
          _ => fibonacci(n - 1) + fibonacci(n - 2),
      }
  }

  fn main() {
      let values: Vec<u64> = (0..20).map(fibonacci).collect();
      println!("Fibonacci: {:?}", values);
  }
  ```
]

#pagebreak()

// --- Page 5: Feature Showcase ---

#text(size: 16pt, weight: 800)[Feature Showcase]
#v(0.3cm)
#line(length: 100%, stroke: 0.5pt + rgb("#ccc"))
#v(0.5cm)

#text(size: 9pt, fill: rgb("#666"))[CHARACTER DISAMBIGUATION]
#v(0.3cm)
#text(size: 16pt)[
  Il1|  — uppercase I, lowercase l, digit 1, pipe\
  O0Oo — uppercase O, digit 0, uppercase O, lowercase o\
  rn m — r+n vs m (clearly distinct in B612)\
  5S   — digit 5 vs uppercase S\
  8B   — digit 8 vs uppercase B\
  2Z   — digit 2 vs uppercase Z\
]

#v(0.5cm)
#text(size: 9pt, fill: rgb("#666"))[OPENTYPE FEATURES]
#v(0.3cm)
#grid(
  columns: (1fr, 1fr),
  gutter: 1cm,
  [
    #text(size: 10pt, fill: rgb("#666"))[Default zero (dotted):]\
    #text(size: 20pt)[0 10 100 1000]
  ],
  [
    #text(size: 10pt, fill: rgb("#666"))[With `zero` feature (slashed):]\
    #set text(features: ("zero",))
    #text(size: 20pt)[0 10 100 1000]
  ],
)

#v(0.5cm)
#text(size: 9pt, fill: rgb("#666"))[BRACKET AND DELIMITER PAIRS]
#v(0.2cm)
#text(size: 16pt)[
  ( ) \{ \} \[ \] < > « » ‹ ›
]

#v(0.5cm)
#text(size: 9pt, fill: rgb("#666"))[MATHEMATICAL AND PROGRAMMING OPERATORS]
#v(0.2cm)
#text(size: 16pt)[
  + - \* / = ≠ ≤ ≥ ± × ÷ → ← ↑ ↓
]

#pagebreak()

// --- Page 6: Provenance and License ---

#text(size: 16pt, weight: 800)[Provenance & License]
#v(0.3cm)
#line(length: 100%, stroke: 0.5pt + rgb("#ccc"))
#v(0.5cm)

#text(size: 11pt, weight: 700)[What is Planetaire Mono?]
#v(0.2cm)
#text(size: 10pt)[
  Planetaire Mono is a composite monospace font that merges B612's highly legible
  letterforms with Hack Nerd Font's complete infrastructure — punctuation, symbols,
  and 12,000+ developer icons. The result is a font optimized for terminal use that
  combines aviation-grade character clarity with full programming language coverage.
]

#v(0.5cm)
#text(size: 11pt, weight: 700)[Source Fonts]
#v(0.2cm)

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt + rgb("#ccc"),
  inset: 8pt,
  [*B612 Mono*], [Designed by Intactile Design for Airbus. Optimized for legibility in cockpit displays. Letters, digits, and extended Latin come from this font.],
  [*carlosedp fork*], [Carlos Eduardo de Paula's fork adding ligatures (calt), dotted zero (zero), empty zero (ezer), and Nerd Font patching.],
  [*Hack*], [Chris Simpkins' Hack — a typeface designed for source code. Provides the base font: punctuation, symbols, and overall metrics.],
  [*Nerd Fonts*], [Ryan McIntyre's icon patching project. 12,000+ developer icons including Powerline, Font Awesome, Devicons, and more.],
)

#v(0.5cm)
#text(size: 11pt, weight: 700)[License]
#v(0.2cm)
#text(size: 10pt)[
  Planetaire Mono is released under the *SIL Open Font License 1.1 (OFL-1.1)*.

  The OFL allows free use, modification, and redistribution of the font, including
  in commercial products, provided that modified versions are not sold by themselves
  and carry a different name.

  The constituent fonts carry the following licenses:
  - *B612*: SIL Open Font License 1.1 + Eclipse Public License 2.0
  - *Hack*: MIT License
  - *Nerd Fonts* patches: MIT License
]

#v(1cm)
#align(center)[
  #text(size: 9pt, fill: rgb("#999"))[
    Planetaire Mono · github.com/jlevy/planetaire · OFL-1.1
  ]
]
