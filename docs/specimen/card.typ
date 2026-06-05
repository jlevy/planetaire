// README image cards, rendered to PNG from the SAME content as the PDF specimen.
// Choose with `--input card=<name>` and `--input theme=dark|light`; rendered in
// matched dark/light pairs by `planetaire build images`.
//   terminal  - the mock terminal session (eza/python/git)
//   code      - the syntax-highlighted Python sample
//   text      - the Turing prose excerpt (legible body text)
//   weights   - the weight ladder (Regular..ExtraBold, upright + italic)
//   features  - confusable-character legibility + dotted-zero variants

#import "content.typ": *

#let which = sys.inputs.at("card", default: "terminal")
#let p = if sys.inputs.at("theme", default: "dark") == "light" { pal-light } else { pal-dark }
#let boxy = which in ("terminal", "code")  // self-contained dark/light block

#set page(
  width: 46em,
  height: auto,
  margin: if boxy { 1.1em } else { 1.6em },
  fill: p.page,
)
#set text(font: font-family, size: 11pt, fill: p.fg)

#if which == "terminal" {
  terminal-mockup(p: p)
} else if which == "code" {
  orbit-code(p: p)
} else if which == "text" {
  text(size: 9pt, fill: p.muted)[ALAN TURING \u{00B7} \u{201C}COMPUTING MACHINERY AND INTELLIGENCE\u{201D} (1950)]
  v(0.3cm)
  turing-passage(p: p, size: 13pt)
} else if which == "weights" {
  weight-ladder(p: p)
} else if which == "features" {
  legibility-pairs(p: p)
}
