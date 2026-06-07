# Terminal Configuration

After installing the font, configure your terminal to use it.

To install the font on macOS, download `PlanetaireMono-Extended` from the
[latest release](https://github.com/jlevy/planetaire/releases/latest), unarchive it,
then double-click any `.ttf` and click **Install Font** (Font Book) or copy the `.ttf`
files into `~/Library/Fonts/`. The [README Install section](../README.md#install) covers
one-line download commands and Linux and web setup.

**Important:** For best results, map bold text to **ExtraBold (weight 800)** instead of
regular Bold (700). The heavier weight provides much better contrast between normal and
bold text at terminal font sizes (12-16px). This is how the font was originally designed
to be used.

## macOS Terminal.app

1. Install the font (see above), then quit and reopen Terminal so it picks up the new
   font.
2. Open **Terminal → Settings…** (Cmd+,) and select the **Profiles** tab.
3. Choose your profile, open the **Text** tab, and click **Change…** under **Font**.
4. Select **Planetaire Mono Extended**, set the size (14 pt is a good start), and close
   the font panel.
5. Check **Use bold fonts** so bold output renders in the bold weight.

Terminal.app applies the family’s **Bold (700)** for bold text and has no per-weight
bold mapping, so it cannot route bold to ExtraBold.
For ExtraBold bold text, use Ghostty (below), which supports `font-style-bold`.

## Ghostty

In `~/.config/ghostty/config`:

```
font-family = "Planetaire Mono Extended"
font-size = 14
font-style-bold = "ExtraBold"
font-style-bold-italic = "ExtraBold Italic"
```

`font-style-bold` maps bold text to the font’s own **ExtraBold** face (the weight the
font is designed around) instead of synthesizing it from Bold.
Run `ghostty +list-fonts` if a style name does not resolve.

## Alacritty

In `~/.config/alacritty/alacritty.toml`:

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

## WezTerm

In `~/.wezterm.lua`:

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
    font = wezterm.font('Planetaire Mono Extended', { weight = 'ExtraBold', italic = true }),
  },
}

return config
```

## iTerm2

1. Open **Preferences** (Cmd+,)
2. Go to **Profiles** > **Text**
3. Click **Font** and select “Planetaire Mono Extended”
4. Set size to 14
5. For the bold font, select “Planetaire Mono Extended ExtraBold”

## Kitty

In `~/.config/kitty/kitty.conf`:

```
font_family      Planetaire Mono Extended
bold_font        Planetaire Mono Extended ExtraBold
italic_font      Planetaire Mono Extended Italic
bold_italic_font Planetaire Mono Extended ExtraBold Italic
font_size        14.0
```

## VS Code Terminal

In `settings.json`:

```json
{
  "terminal.integrated.fontFamily": "Planetaire Mono Extended",
  "terminal.integrated.fontSize": 14,
  "terminal.integrated.fontWeight": "normal",
  "terminal.integrated.fontWeightBold": "800"
}
```

## About the Weights

Planetaire Mono ships with 10 variants:

| Variant | Weight | Usage |
| --- | --- | --- |
| Regular | 400 | Normal terminal text |
| Italic | 400 | Italic/emphasized text |
| Medium | 500 | UI labels, intermediate weight |
| Medium Italic | 500 | UI labels italic |
| SemiBold | 600 | UI emphasis, intermediate weight |
| SemiBold Italic | 600 | UI emphasis italic |
| Bold | 700 | Standard bold |
| Bold Italic | 700 | Standard bold italic |
| **ExtraBold** | **800** | **Recommended for terminal bold** |
| ExtraBold Italic | 800 | Recommended for terminal bold italic |

The jump from Regular (400) to Bold (700) can feel subtle at small terminal sizes.
ExtraBold (800) provides a visibly heavier stroke that makes bold text (prompts,
headings, highlighted output) stand out clearly.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
