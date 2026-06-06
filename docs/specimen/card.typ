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
  width: if which == "header" { 68em } else { 46em },
  height: auto,
  // More vertical breathing room. The boxy cards (terminal/code) fill the page with
  // the block background so each image reads as uniformly all-light or all-dark.
  margin: if which == "header" { 1.6em } else if boxy { (x: 1.3em, y: 1.8em) } else {
    (x: 1.8em, y: 2.4em)
  },
  fill: if boxy { p.term-bg } else { p.page },
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
} else if which == "header" {
  header-card(p: p)
}
