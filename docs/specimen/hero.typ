// Planetaire Mono — README hero image.
// Rendered to PNG by `planetaire build hero` (single Typst render path,
// shared font setup with the PDF specimen).

#let version = sys.inputs.at("version", default: "0.0.0-dev")

#set page(width: 42em, height: auto, margin: 1.6em, fill: rgb("#0d1117"))
#set text(font: "Planetaire Mono Extended", size: 12pt, fill: rgb("#e6edf3"))
#set par(leading: 0.62em)

// Palette (GitHub dark-ish).
#let dim = rgb("#7d8590")
#let kw = rgb("#ff7b72")
#let fn = rgb("#d2a8ff")
#let str = rgb("#a5d6ff")
#let num = rgb("#79c0ff")
#let com = rgb("#8b949e")
#let ac = rgb("#58a6ff")

#text(size: 22pt, weight: 800)[Planetaire Mono]
#h(0.6em)
#text(fill: dim, size: 11pt)[legible monospace · B612 + Hack · v#version]

#v(0.7em)
#line(length: 100%, stroke: 0.5pt + rgb("#30363d"))
#v(0.7em)

// A small, syntax-coloured code sample showing real letterforms + dotted zero.
#text(fill: com)[\# Il1| O0o rn/m 5S 8B 2Z — easy to tell apart]\
#text(fill: kw)[def] #text(fill: fn)[planetaire]#text(fill: dim)[(]zero#text(fill: dim)[=]#text(fill: num)[0]#text(fill: dim)[) ->] #text(fill: kw)[bool]#text(fill: dim)[:]\
#h(2em)items #text(fill: dim)[=] #text(fill: dim)[\{]#text(fill: str)["a"]#text(fill: dim)[: \[]#text(fill: num)[1]#text(fill: dim)[, ]#text(fill: num)[2]#text(fill: dim)[, ]#text(fill: num)[3]#text(fill: dim)[\], ]#text(fill: str)["b"]#text(fill: dim)[: (]#text(fill: num)[4]#text(fill: dim)[, ]#text(fill: num)[5]#text(fill: dim)[)\}]\
#h(2em)#text(fill: kw)[return] #text(fill: fn)[all]#text(fill: dim)[(]x #text(fill: dim)[>=] #text(fill: num)[0] #text(fill: kw)[for] x #text(fill: kw)[in] items#text(fill: dim)[\[]#text(fill: str)["a"]#text(fill: dim)[\]) !=] zero

#v(0.8em)
#text(fill: ac, weight: 700, size: 9.5pt)[THE QUICK BROWN FOX] #h(0.5em) #text(fill: dim, size: 9.5pt)[0123456789 {[()]} →]
