// README image cards, rendered to PNG from the SAME content as the PDF specimen.
// Pick one with `--input card=<name>`; render via `planetaire build images`.
//   terminal  - the Kerm mock terminal session (eza/python/git)
//   code      - the syntax-highlighted Python sample
//   text      - the Turing prose excerpt (legible body text)
//   weights   - the weight ladder (Regular..ExtraBold, upright + italic)
//   features  - confusable-character legibility + dotted-zero variants

#import "content.typ": *

#let which = sys.inputs.at("card", default: "terminal")

// Dark cards (terminal/code) get the Kerm background and tight padding; the
// light cards (text/weights/features) get a clean white card with a header.
#let dark = which in ("terminal", "code")

#set page(
  width: 46em,
  height: auto,
  margin: if dark { 1.1em } else { 1.6em },
  fill: if dark { kerm.bg } else { white },
)
#set text(font: font-family, size: 11pt, fill: if dark { kerm.fg } else { rgb("#24292f") })

#if which == "terminal" {
  terminal-mockup()
} else if which == "code" {
  orbit-code()
} else if which == "text" {
  text(size: 9pt, fill: rgb("#999"))[ALAN TURING \u{00B7} \u{201C}COMPUTING MACHINERY AND INTELLIGENCE\u{201D} (1950)]
  v(0.3cm)
  turing-passage(size: 13pt)
} else if which == "weights" {
  weight-ladder()
} else if which == "features" {
  legibility-pairs()
}
