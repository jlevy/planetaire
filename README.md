<p align="center"> <img src="docs/images/header.png" alt="Planetaire Mono" width="100%">
</p>

Planetaire Mono is a beautiful, highly legible monospace font for terminals, editors,
and agentic work.

It is a lightly adapted fork of [B612 Mono](https://github.com/polarsys/b612) with added
weights, symbols from [Hack](https://sourcefoundry.org/hack/), and extensive icons from
[Nerd Fonts](https://www.nerdfonts.com/). It is [licensed freely](#license) for
personal, commercial, and open source use.

**[Read the Type Specimen (PDF)](https://cdn.jsdelivr.net/gh/jlevy/planetaire@main/docs/specimen/planetaire-mono-specimen.pdf)**

**[Download the Fonts (TTF, WOFF2)](https://github.com/jlevy/planetaire/releases/latest)**

## Why

### About B612

B612 began not as a typeface but as an aviation research program.
In 2010 Airbus, [ENAC](https://www.enac.fr/en) (the French civil aviation university),
and the Université de Toulouse III set out to define and validate an “aeronautical font”
for cockpit screens: text a pilot can read correctly while fatigued, at oblique angles,
or under vibration, glare, or near-darkness.

The shapes were derived experimentally before they were drawn.
Jean-Luc Vinot (ENAC) and Sylvie Athènes (Toulouse III) built confusion matrices of when
and how characters get misread
(“[Legible, are you sure?](https://dl.acm.org/doi/10.1145/2207676.2208387)” at CHI
2012). In their controlled study, the prototype that became B612 drew slightly more
correct reads than Verdana and clearly outperformed the legacy avionics font.
Airbus then commissioned the Montpellier interface studio
[Intactile Design](https://intactile.com/) (Nicolas Chauveau, Thomas Paillot, and
Jonathan Favre-Lamarine) to draw the full family of eight variants.

B612 is named for the asteroid home of the
[Little Prince](https://en.wikipedia.org/wiki/The_Little_Prince) by Antoine de
Saint-Exupéry, who was
[himself an aviator](https://en.wikipedia.org/wiki/Wind,_Sand_and_Stars).

B612’s unusual character is a humanist answer to an instrument-panel problem.
Where earlier cockpit fonts went monolinear and rigid, B612 keeps stroke contrast, opens
counters, and lengthens ascenders and descenders.
Each word’s silhouette resolves quickly.
At stroke junctions it carries small notches (light traps) that keep joins from filling
in on bright, low-contrast displays.
The result has quietly human character quirks that are grounded in measured legibility
gains rather than style.
In 2017, B612 was released as open source through the Eclipse
[Polarsys](https://github.com/polarsys/b612) project.

### About Planetaire Mono

By historical accident, B612 alone is not a usable document or application font.
The versions in circulation, including the one
[on Google Fonts](https://fonts.google.com/specimen/B612+Mono), have oddities and uneven
symbol coverage that make them awkward for use in modern applications and terminals.
For example, some of the punctuation and symbols are a bit too thin for programming
legibility, and the published versions have an undotted zero that is easy to confuse
with a capital `O`.

Planetaire Mono arises from this need.
It merges B612’s letters and digits into Hack Nerd Font’s base.
It also adds more weights and a dotted zero:

- **B612 letterforms** for letters, digits, and extended Latin, Greek, and Cyrillic.
- **Hack punctuation and symbols** for `{}[]()<>` and the rest.
- **Ten variants across five weights** (400/500/600/700/800), including added **SemiBold
  (600)** and **ExtraBold (800)** weights, the latter especially useful as boldface in
  the terminal.
- **12,000+ Nerd Font icons** (Powerline, Font Awesome, Devicons) in the Extended
  package.
- **A dotted zero:** B612’s zero with a center dot for clear `0` vs `O`, in circle
  (default) and rectangle (`ss01`) variants.

### A Personal Note

Like architecture, typography is a functional art form.
A design may initially appear attractive, but you can’t know its true qualities until
you live close to it.
Or work within it.

A couple of years ago, I was building a terminal and surveyed monospace fonts to find
the best ones. B612 wasn’t my obvious first choice, but after trying many of the classic
modern options available as Nerd Fonts, I came to realize it still just *felt* better
over time. But I was disappointed with the technical flaws that made it hard to use as a
full replacement for a modern, high-quality workhorse typeface such as Hack or JetBrains
Mono. I made an adapted hybrid of B612 that I was quite happy with, but it wasn’t in a
clean enough form to publish.

Now, Claude Code and Opus 4.8 have made it a pleasure to consolidate this work as
Planetaire Mono. I’ve used dozens of terminal fonts over the years, and it is now what I
use every day.

Thanks to agentic coding, monospace fonts are now in greater use than anyone could ever
have imagined. I hope Planetaire Mono’s aesthetics lighten the hours you spend with your
agents, editors, and terminals.

## Specimens

<p align="center">
<img src="docs/images/text-dark.png" width="100%" alt="A prose passage set in Planetaire Mono on a dark background, showing body-text legibility">
<br>
<img src="docs/images/text-light.png" width="100%" alt="The same prose passage in Planetaire Mono on a light background">
</p>

<p align="center">
<img src="docs/images/rfc-dark.png" width="100%" alt="RFC 1 (1969) set in Planetaire Mono, on a dark background">
<br>
<img src="docs/images/rfc-light.png" width="100%" alt="The same RFC 1 document on a light background">
</p>

<p align="center">
<img src="docs/images/sample-dark.png" width="100%" alt="Multi-size body text plus French, German, Spanish, Turkish, Greek, and Cyrillic samples in Planetaire Mono, on a dark background">
<br>
<img src="docs/images/sample-light.png" width="100%" alt="The same multi-language text sample on a light background">
</p>

<p align="center">
<img src="docs/images/waterfall-dark.png" width="100%" alt="Planetaire Mono from 8pt to 44pt with a large legibility line, on a dark background">
<br>
<img src="docs/images/waterfall-light.png" width="100%" alt="The same size waterfall on a light background">
</p>

<p align="center">
<img src="docs/images/code-dark.png" width="100%" alt="A syntax-highlighted analyze_trajectory() Python function in Planetaire Mono on a dark background">
<br>
<img src="docs/images/code-light.png" width="100%" alt="The same Python function in Planetaire Mono on a light background">
</p>

<p align="center">
<img src="docs/images/terminal-dark.png" width="100%" alt="A terminal session in Planetaire Mono on a dark background: a colored eza listing, a Python one-liner, and a git log">
<br>
<img src="docs/images/terminal-light.png" width="100%" alt="The same terminal session in Planetaire Mono on a light background">
</p>

<p align="center">
<img src="docs/images/weights-dark.png" width="100%" alt="Planetaire Mono weight ladder from Regular to ExtraBold, upright and italic, on a dark background">
<br>
<img src="docs/images/weights-light.png" width="100%" alt="The same weight ladder on a light background">
</p>

<p align="center">
<img src="docs/images/features-dark.png" width="100%" alt="Confusable-character pairs and the dotted-zero variants in Planetaire Mono, on a dark background">
<br>
<img src="docs/images/features-light.png" width="100%" alt="The same confusable-character pairs and dotted-zero variants on a light background">
</p>

## High Legibility

B612’s letterforms keep commonly confused characters distinct: `Il1|`, `O0o`, `rn` vs
`m`, `5S`, `8B`, `2Z`. Coverage spans Latin Extended A/B, Greek and Coptic, Cyrillic,
and Latin Extended Additional: over 12,000 glyphs in the Extended package.

## Weights

### Additional Weights

Each package ships 10 variants across 5 weights.

Planetaire Mono adds an **ExtraBold (800)** weight for terminal bold: the jump from
Regular (400) to Bold (700) is often too subtle at terminal sizes, and ExtraBold gives
bold text (prompts, headings, highlighted output) the contrast to stand out.

| Variant | Weight | Recommended Use |
| --- | --- | --- |
| Regular | 400 | Normal terminal text |
| Italic | 400 | Emphasized text |
| Medium | 500 | UI labels, intermediate weight |
| Medium Italic | 500 | UI labels italic |
| SemiBold | 600 | UI emphasis, intermediate weight |
| SemiBold Italic | 600 | UI emphasis italic |
| Bold | 700 | Standard bold |
| Bold Italic | 700 | Standard bold italic |
| **ExtraBold** | **800** | **Terminal bold text** |
| **ExtraBold Italic** | **800** | **Terminal bold italic** |

### ExtraBold for Terminals

For best results, map your terminal’s **bold** to **ExtraBold (800)** rather than Bold
(700): the heavier stroke gives bold output (prompts, headings, highlighted text) clear
contrast at terminal sizes, which is how the font is designed to be used.
Per-terminal setup for Terminal.app, Ghostty, Alacritty, WezTerm, iTerm2, Kitty, and VS
Code is under [Install → Terminal Configuration](#terminal-configuration).

## Two Packages: Text and Extended

Both packages share the same letterforms and the same 10 variants, and both ship in two
formats: **TTF** (in `ttf/`) for local install and **WOFF2** (in `web/`, with a ready
`@font-face` stylesheet) for the web.
They differ only in glyph coverage:

- **Planetaire Mono Extended** is the full font: everything in Text **plus** the ~12,000
  Nerd Font icons and Powerline glyphs that terminals and CLIs draw, so it is a superset
  of Text. **Recommended for local and terminal use**, where TTF is the standard option.
- **Planetaire Mono Text** is a lightweight subset (no icons), so it is far smaller.
  **Recommended for the web**, where the WOFF2 stylesheet is the standard option.

Either package works for either purpose; the recommendations are just the common,
size-conscious defaults.
See [Download](#download) for the archives and sizes.

## Download

Planetaire Mono is available in two packages, built from the same letterforms.
Get the latest from
[**GitHub Releases**](https://github.com/jlevy/planetaire/releases/latest):

| Package | Best for | Includes | Download |
| --- | --- | --- | --- |
| **Planetaire Mono Text** *(standard)* | Websites, documents, reading | Letters, punctuation, Greek/Cyrillic, box-drawing. No icons. TTF + WOFF2 (~67 KB/weight WOFF2). | [`.tar.xz`](https://github.com/jlevy/planetaire/releases/latest/download/PlanetaireMono-Text.tar.xz) **~1 MB** · [`.zip`](https://github.com/jlevy/planetaire/releases/latest/download/PlanetaireMono-Text.zip) ~1.3 MB |
| **Planetaire Mono Extended** *(full)* | Terminals, coding, icon-rich CLIs | Everything in Text plus all ~12,000 Nerd Font icons and Powerline. TTF + WOFF2. | [`.tar.xz`](https://github.com/jlevy/planetaire/releases/latest/download/PlanetaireMono-Extended.tar.xz) **~19 MB** · [`.zip`](https://github.com/jlevy/planetaire/releases/latest/download/PlanetaireMono-Extended.zip) ~24 MB |

Both packages ship the same 10 variants, each archive laid out as `ttf/` (for local
install) and `web/` (WOFF2 plus an `@font-face` stylesheet).
To install locally: unzip and double-click the `ttf/*.ttf` files (macOS Font Book or
Windows), or on Linux copy them to `~/.local/share/fonts/` and run `fc-cache -fv`.
Per-OS and web details are under [Install](#install).

## Install

> The **fonts** are distributed via
> [GitHub Releases](https://github.com/jlevy/planetaire/releases).
> This repo is the **build tooling**, not the font itself; you only need it to build
> from source.

### macOS

```bash
curl -L https://github.com/jlevy/planetaire/releases/latest/download/PlanetaireMono-Extended.tar.xz | tar xJ
cp ttf/*.ttf ~/Library/Fonts/
```

### Linux

```bash
curl -L https://github.com/jlevy/planetaire/releases/latest/download/PlanetaireMono-Extended.tar.xz | tar xJ
mkdir -p ~/.local/share/fonts/PlanetaireMono
cp ttf/*.ttf ~/.local/share/fonts/PlanetaireMono/
fc-cache -fv
```

### Terminal Configuration

After installing the font, point your terminal at **Planetaire Mono Extended**. For best
results, map **bold** text to **ExtraBold (800)** rather than Bold (700): the heavier
stroke gives bold output (prompts, headings, highlighted text) clear contrast at
terminal sizes (12–16px), which is how the font is designed to be used.

**macOS Terminal.app.** Open **Terminal → Settings… → Profiles**, pick your profile,
open the **Text** tab, and in the **Font** section click **Change** to select Planetaire
Mono Extended at 14 pt.
Check **Use bold fonts** so bold output renders in bold.
Terminal.app uses the family’s Bold (700) and has no per-weight bold mapping, so it
can’t route bold to ExtraBold; use Ghostty (below) if you want ExtraBold bold.

**Ghostty** — in `~/.config/ghostty/config`:

```
font-family = "Planetaire Mono Extended"
font-size = 14
font-style-bold = "ExtraBold"
font-style-bold-italic = "ExtraBold Italic"
```

Run `ghostty +list-fonts` if a style name does not resolve.

**Alacritty** — in `~/.config/alacritty/alacritty.toml`:

```toml
[font]
size = 14.0

[font.normal]
family = "Planetaire Mono Extended"
style = "Regular"

[font.bold]
family = "Planetaire Mono Extended"
style = "ExtraBold"

[font.italic]
family = "Planetaire Mono Extended"
style = "Italic"

[font.bold_italic]
family = "Planetaire Mono Extended"
style = "ExtraBold Italic"
```

**WezTerm** — in `~/.wezterm.lua`:

```lua
local wezterm = require 'wezterm'
local config = wezterm.config_builder()

config.font = wezterm.font('Planetaire Mono Extended')
config.font_size = 14.0

-- Map bold to ExtraBold for maximum contrast
config.font_rules = {
  {
    intensity = 'Bold',
    font = wezterm.font('Planetaire Mono Extended', { weight = 'ExtraBold' }),
  },
  {
    intensity = 'Bold',
    italic = true,
    font = wezterm.font('Planetaire Mono Extended', { weight = 'ExtraBold', style = 'Italic' }),
  },
}

return config
```

**iTerm2.** Open **Preferences → Profiles → Text**, set **Font** to Planetaire Mono
Extended at 14 pt, and check **Draw bold text in bold font** so bold renders in the
family’s bold member.
iTerm2 has no separate bold-font field, so it can’t target the ExtraBold face
specifically; use Ghostty, Kitty, or the VS Code terminal if you want ExtraBold bold.

**Kitty** — in `~/.config/kitty/kitty.conf`:

```
font_family      family="Planetaire Mono Extended"
bold_font        family="Planetaire Mono Extended" style="ExtraBold"
italic_font      family="Planetaire Mono Extended" style="Italic"
bold_italic_font family="Planetaire Mono Extended" style="ExtraBold Italic"
font_size        14.0
```

**VS Code terminal** — in `settings.json`:

```json
{
  "terminal.integrated.fontFamily": "Planetaire Mono Extended",
  "terminal.integrated.fontSize": 14,
  "terminal.integrated.fontWeight": "normal",
  "terminal.integrated.fontWeightBold": "800"
}
```

### Web (CSS `@font-face`)

Both packages include WOFF2 web fonts and a ready stylesheet in `web/`. The **Text**
package is recommended for the web (much smaller, no icons); use **Extended** only if
you need the Nerd Font icons in the browser.
From the Text archive’s `web/`:

```html
<link rel="stylesheet" href="planetaire-mono-text.css">
<style>
  body { font-family: "Planetaire Mono Text", ui-monospace, monospace; }
  /* rectangle zero instead of the dotted circle: */
  .code { font-feature-settings: "ss01" 1; }
</style>
```

Each weight and style is declared (400/500/600/700/800, upright and italic) with
`font-display: swap`.

## Build from Source

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --all-extras
make fonts        # download (verify) -> build Extended + Text -> validate
```

The pipeline merges B612 glyphs into the Hack Nerd Font base (normalizing UPM 2048 to
2000), adds the dotted zero, sets family and version metadata, applies fixes, and
validates coverage and style linking.
Full build, specimen, and release steps are in
[fonts-build-and-release.md](docs/fonts-build-and-release.md); regenerating the specimen
and these images is in [build-assets.runbook.md](docs/build-assets.runbook.md).

## Credits

- [**B612**](https://github.com/polarsys/b612): Intactile Design for Airbus.
  The letterforms.
- [**Hack**](https://sourcefoundry.org/hack/): Chris Simpkins.
  The base providing punctuation, symbols, and metrics.
- [**Nerd Fonts**](https://www.nerdfonts.com/): Ryan McIntyre.
  12,000+ developer icons.
- [**carlosedp**](https://github.com/carlosedp/b612): Carlos Eduardo de Paula’s B612
  Nerd Font fork, which inspired the dotted zero.
  Not a build dependency.

## License

Planetaire Mono is released under the
[SIL Open Font License 1.1](https://openfontlicense.org/) (OFL-1.1), the standard
license for open fonts.
In practical terms:

- **Use it for anything, free.** Set text in Planetaire Mono in documents, books,
  websites, apps, videos, and commercial products, with no fee and no permission needed.
- **No credit required for use.** Setting text in the font does not obligate you to
  attribute Planetaire Mono or B612 anywhere, including in publications, commercial
  work, or open source software.
  Credit is welcome but optional.
- **Bundle and redistribute freely, but keep the license with the files.** If you ship
  the font files themselves (embedding web fonts, packaging them in an app or OS),
  include the OFL license and copyright notices alongside them.
  You may not sell the font files on their own.
- **Don’t reuse the B612 name for modified versions.** OFL lets an author reserve font
  names, and “B612” is reserved, so a derivative cannot be distributed under that name.
  That rule is why this fork is called Planetaire Mono.

This is a summary, not legal advice; the [full OFL text](https://openfontlicense.org/)
is binding. The upstream sources carry their own licenses: **B612** under OFL-1.1 and
EPL-2.0; **Hack** under MIT; **Nerd Fonts** patches under MIT. The build tooling in this
repo is [MIT](LICENSE).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
