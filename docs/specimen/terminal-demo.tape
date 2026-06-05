# Planetaire Mono — terminal demo.
# Render with: vhs docs/specimen/terminal-demo.tape
# Requires the Planetaire Mono font installed plus VHS (+ its headless Chromium).
# Produces an animated GIF and a final-frame PNG for the README/site.

Output docs/images/terminal-demo.gif

Set FontFamily "Planetaire Mono"
Set FontSize 20
Set Width 1100
Set Height 640
Set Padding 28
Set Theme { "name": "Planetaire", "background": "#0d1117", "foreground": "#e6edf3", "cursor": "#58a6ff", "black": "#484f58", "red": "#ff7b72", "green": "#3fb950", "yellow": "#d29922", "blue": "#58a6ff", "magenta": "#bc8cff", "cyan": "#39c5cf", "white": "#b1bac4", "brightBlack": "#6e7681", "brightRed": "#ffa198", "brightGreen": "#56d364", "brightYellow": "#e3b341", "brightBlue": "#79c0ff", "brightMagenta": "#d2a8ff", "brightCyan": "#56d4dd", "brightWhite": "#f0f6fc" }

# Hidden setup: clean prompt + the project venv so `planetaire` is on PATH.
Hide
Type "source .venv/bin/activate" Enter
Type "PS1='planetaire $ '" Enter
Type "clear" Enter
Show
Sleep 600ms

# Legibility line (note the dotted zero, Il1|, O0o).
Type "echo 'Il1| O0o rn/m 5S 8B 2Z  0123456789'" Sleep 500ms Enter
Sleep 1200ms

# Real programs rendered in the font.
Type "planetaire info fonts/output/PlanetaireMono-Regular.ttf" Sleep 500ms Enter
Sleep 2400ms
Type "flowmark --version" Sleep 400ms Enter
Sleep 1600ms
Screenshot docs/images/terminal-demo.png
