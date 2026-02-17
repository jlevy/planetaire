# Terminal Configuration

After installing Planetaire Mono, configure your terminal to use it.

**Important:** For best results, map bold text to **ExtraBold (weight 800)** instead of
regular Bold (700). The heavier weight provides much better contrast between normal and
bold text at terminal font sizes (12-16px). This is how the font was originally designed
to be used.

## Ghostty

In `~/.config/ghostty/config`:

```
font-family = "Planetaire Mono"
font-size = 14
font-thicken = true
```

Ghostty automatically selects the best weight for bold text. With `font-thicken = true`,
bold text uses heavier strokes for improved contrast.

## Alacritty

In `~/.config/alacritty/alacritty.toml`:

```toml
[font]
size = 14.0

[font.normal]
family = "Planetaire Mono"
style = "Regular"

[font.bold]
family = "Planetaire Mono"
style = "ExtraBold"

[font.italic]
family = "Planetaire Mono"
style = "Italic"

[font.bold_italic]
family = "Planetaire Mono"
style = "ExtraBold Italic"
```

## WezTerm

In `~/.wezterm.lua`:

```lua
local wezterm = require 'wezterm'
local config = wezterm.config_builder()

config.font = wezterm.font('Planetaire Mono')
config.font_size = 14.0

-- Map bold to ExtraBold for maximum contrast
config.font_rules = {
  {
    intensity = 'Bold',
    font = wezterm.font('Planetaire Mono', { weight = 'ExtraBold' }),
  },
  {
    intensity = 'Bold',
    italic = true,
    font = wezterm.font('Planetaire Mono', { weight = 'ExtraBold', italic = true }),
  },
}

return config
```

## iTerm2

1. Open **Preferences** (Cmd+,)
2. Go to **Profiles** > **Text**
3. Click **Font** and select "Planetaire Mono"
4. Set size to 14
5. For the bold font, select "Planetaire Mono ExtraBold"

## Kitty

In `~/.config/kitty/kitty.conf`:

```
font_family      Planetaire Mono
bold_font        Planetaire Mono ExtraBold
italic_font      Planetaire Mono Italic
bold_italic_font Planetaire Mono ExtraBold Italic
font_size        14.0
```

## VS Code Terminal

In `settings.json`:

```json
{
  "terminal.integrated.fontFamily": "Planetaire Mono",
  "terminal.integrated.fontSize": 14,
  "terminal.integrated.fontWeight": "normal",
  "terminal.integrated.fontWeightBold": "800"
}
```

## About the Weights

Planetaire Mono ships with 6 variants:

| Variant | Weight | Usage |
|---------|--------|-------|
| Regular | 400 | Normal terminal text |
| Italic | 400 | Italic/emphasized text |
| Bold | 700 | Standard bold |
| Bold Italic | 700 | Standard bold italic |
| **ExtraBold** | **800** | **Recommended for terminal bold** |
| ExtraBold Italic | 800 | Recommended for terminal bold italic |

The jump from Regular (400) to Bold (700) can feel subtle at small terminal sizes.
ExtraBold (800) provides a visibly heavier stroke that makes bold text — prompts,
headings, highlighted output — stand out clearly.
