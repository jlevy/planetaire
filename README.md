# Planetaire Mono

A monospace font for terminals and code that pairs [B612](https://b612-font.com/)’s
highly legible letterforms with [Hack](https://sourcefoundry.org/hack/)’s programming
symbols and [Nerd Font](https://www.nerdfonts.com/) icons.

**[Read the type specimen (PDF)](docs/specimen/planetaire-mono-specimen.pdf)** ·
**[Download the fonts](https://github.com/jlevy/planetaire/releases/latest)**

<p>
<img src="docs/images/terminal-dark.png" width="680" alt="A terminal session in Planetaire Mono on a dark background: a colored eza listing with Nerd Font icons, a Python one-liner, and a git log">
<br>
<img src="docs/images/terminal-light.png" width="680" alt="The same terminal session in Planetaire Mono on a light background">
</p>

## Why

B612 was designed by Intactile Design for Airbus cockpit displays, optimized for reading
under stress, at odd angles, and in poor lighting.
Its letterforms are among the most legible drawn for monospace text.

But B612 alone is not a complete programming font, and the versions in circulation,
including the one on [Google Fonts](https://fonts.google.com/specimen/B612+Mono), have
quirks that make them awkward for code and terminals: most notably an undotted zero that
is easy to confuse with a capital `O`, plus no symbols or icons for programming.

Planetaire Mono fixes that.
It merges B612’s letters and digits into Hack Nerd Font’s base and adds a dotted zero:

- **B612 letterforms** for letters, digits, and extended Latin, Greek, and Cyrillic.
- **A dotted zero:** B612’s zero with a center dot for clear `0` vs `O`, in circle
  (default) and rectangle (`ss01`) variants.
- **Hack punctuation and symbols** for `{}[]()<>` and the rest.
- **12,000+ Nerd Font icons** (Powerline, Font Awesome, Devicons) in the Extended
  family.

With these changes it has become one of the most beautiful and genuinely functional
monospace fonts I’ve seen; it’s what I use every day.
It carries a new name to avoid confusion with the original B612, to comply with the
font’s license terms on naming, and to be a little more memorable.

<p>
<img src="docs/images/text-dark.png" width="680" alt="A prose passage set in Planetaire Mono on a dark background, showing body-text legibility">
<br>
<img src="docs/images/text-light.png" width="680" alt="The same prose passage in Planetaire Mono on a light background">
</p>

## Download

Two families, built from the same letterforms.
Get the latest from
[**GitHub Releases**](https://github.com/jlevy/planetaire/releases/latest):

| Family | Best for | Includes | Download |
| --- | --- | --- | --- |
| **Planetaire Mono Text** *(standard)* | Websites, documents, reading | Letters, punctuation, Greek/Cyrillic, box-drawing. No icons (~67 KB/weight WOFF2). | [`.tar.xz`](https://github.com/jlevy/planetaire/releases/latest/download/PlanetaireMono-Text.tar.xz) **1.6 MB** · [`.zip`](https://github.com/jlevy/planetaire/releases/latest/download/PlanetaireMono-Text.zip) 1.9 MB |
| **Planetaire Mono Extended** *(full)* | Terminals, coding, icon-rich CLIs | Everything in Text plus all ~12,000 Nerd Font icons and Powerline (~2.6–4.4 MB/weight TTF). | [`.tar.xz`](https://github.com/jlevy/planetaire/releases/latest/download/PlanetaireMono-Extended.tar.xz) **5.4 MB** · [`.zip`](https://github.com/jlevy/planetaire/releases/latest/download/PlanetaireMono-Extended.zip) 13 MB |

Both ship the same 8 variants.
To install: unzip and double-click the `.ttf` files (macOS Font Book or Windows), or on
Linux copy them to `~/.local/share/fonts/` and run `fc-cache -fv`. The Text archive also
includes WOFF2/WOFF and an `@font-face` stylesheet for the web.
Per-OS and web details are under [Install](#install).

## Weights

Each family ships 8 variants across 4 weights.

<p>
<img src="docs/images/weights-dark.png" width="680" alt="Planetaire Mono weight ladder from Regular to ExtraBold, upright and italic, on a dark background">
<br>
<img src="docs/images/weights-light.png" width="680" alt="The same weight ladder on a light background">
</p>

| Variant | Weight | Recommended Use |
| --- | --- | --- |
| Regular | 400 | Normal terminal text |
| Italic | 400 | Emphasized text |
| Medium | 500 | UI labels, intermediate weight |
| Medium Italic | 500 | UI labels italic |
| Bold | 700 | Standard bold |
| Bold Italic | 700 | Standard bold italic |
| **ExtraBold** | **800** | **Terminal bold text** |
| **ExtraBold Italic** | **800** | **Terminal bold italic** |

### ExtraBold for Terminals

The jump from Regular (400) to Bold (700) is often too subtle at terminal sizes.
ExtraBold (800) gives bold text (prompts, headings, highlighted output) the contrast to
stand out. Map your terminal’s bold to ExtraBold:

```
# Ghostty
font-family = "Planetaire Mono Extended"
font-style-bold = "ExtraBold"

# Alacritty
[font.bold]
family = "Planetaire Mono Extended"
style = "ExtraBold"

# WezTerm
config.font_rules = {
  {
    intensity = 'Bold',
    font = wezterm.font('Planetaire Mono Extended', { weight = 'ExtraBold' }),
  },
}

# VS Code terminal
"terminal.integrated.fontWeightBold": "800"
```

See [terminal-config.md](docs/terminal-config.md) for Ghostty, Alacritty, WezTerm,
iTerm2, Kitty, and VS Code.

## High Legibility

<p>
<img src="docs/images/features-dark.png" width="680" alt="Confusable-character pairs and the dotted-zero variants in Planetaire Mono, on a dark background">
<br>
<img src="docs/images/features-light.png" width="680" alt="The same confusable-character pairs and dotted-zero variants on a light background">
</p>

B612’s letterforms keep commonly confused characters distinct: `Il1|`, `O0o`, `rn` vs
`m`, `5S`, `8B`, `2Z`. Coverage spans Latin Extended A/B, Greek and Coptic, Cyrillic,
and Latin Extended Additional: over 12,000 glyphs in the Extended family.

## Install

> The **fonts** are distributed via
> [GitHub Releases](https://github.com/jlevy/planetaire/releases).
> The [PyPI package](https://pypi.org/project/planetaire/) is the **build tooling**, not
> the font. Install it only to build from source.

### macOS

```bash
curl -L https://github.com/jlevy/planetaire/releases/latest/download/PlanetaireMono-Extended.tar.xz | tar xJ
cp PlanetaireMonoExtended-*.ttf ~/Library/Fonts/
```

### Linux

```bash
curl -L https://github.com/jlevy/planetaire/releases/latest/download/PlanetaireMono-Extended.tar.xz | tar xJ
mkdir -p ~/.local/share/fonts/PlanetaireMono
cp PlanetaireMonoExtended-*.ttf ~/.local/share/fonts/PlanetaireMono/
fc-cache -fv
```

### Web (CSS `@font-face`)

Use the Text family on the web.
The Text archive ships WOFF2/WOFF and a ready `planetaire-mono-text.css`:

```html
<link rel="stylesheet" href="planetaire-mono-text.css">
<style>
  body { font-family: "Planetaire Mono Text", ui-monospace, monospace; }
  /* rectangle zero instead of the dotted circle: */
  .code { font-feature-settings: "ss01" 1; }
</style>
```

Each weight and style is declared (400/500/700/800, upright and italic) with
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

- [**B612**](https://b612-font.com/): Intactile Design for Airbus
  ([polarsys/b612](https://github.com/polarsys/b612)). The letterforms.
- [**Hack**](https://sourcefoundry.org/hack/): Chris Simpkins.
  The base providing punctuation, symbols, and metrics.
- [**Nerd Fonts**](https://www.nerdfonts.com/): Ryan McIntyre.
  12,000+ developer icons.
- [**carlosedp**](https://github.com/carlosedp/b612): Carlos Eduardo de Paula’s B612
  Nerd Font fork, which inspired the dotted zero.
  Not a build dependency.

## License

Planetaire Mono is released under the
[SIL Open Font License 1.1](https://openfontlicense.org/) (OFL-1.1). The source fonts
carry: **B612** OFL-1.1 and EPL-2.0; **Hack** MIT; **Nerd Fonts** patches MIT. The build
tooling is [MIT](LICENSE).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
