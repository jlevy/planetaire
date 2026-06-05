#!/usr/bin/env python3
"""Generate font showcase images for the README.

Creates PNG renders of Planetaire Mono on dark backgrounds,
demonstrating letterforms, weights, and features.

Usage:
    python scripts/generate_showcase.py [--output-dir docs/images]
"""

from __future__ import annotations

import argparse
import atexit
import tempfile
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.ttLib.tables import ttProgram
from PIL import Image, ImageDraw, ImageFont

FONTS_DIR = Path(__file__).parent.parent / "fonts" / "output"

# Colors
BG = (22, 22, 28)  # Dark background
FG = (220, 220, 220)  # Primary text
DIM = (120, 120, 140)  # Dim/comment text
ACCENT_GREEN = (80, 200, 120)
ACCENT_BLUE = (100, 160, 255)
ACCENT_ORANGE = (255, 180, 80)
ACCENT_PURPLE = (180, 130, 255)
ACCENT_RED = (255, 100, 100)
ACCENT_CYAN = (80, 220, 220)
ACCENT_YELLOW = (220, 200, 80)

# Cache for unhinted font files (temp copies, cleaned up on exit)
_unhinted_cache: dict[str, str] = {}


@atexit.register
def _cleanup_unhinted_cache() -> None:
    for tmp_path in _unhinted_cache.values():
        Path(tmp_path).unlink(missing_ok=True)


def _strip_hinting(font_path: str) -> str:
    """Strip TrueType hinting from font and return path to unhinted copy.

    The merged font inherits Hack's hinting tables which are incompatible
    with B612 glyphs. Stripping hinting ensures correct rendering.
    """
    if font_path in _unhinted_cache:
        return _unhinted_cache[font_path]

    t = TTFont(font_path)
    for table in ("prep", "fpgm", "cvt "):
        if table in t:
            del t[table]
    glyf = t["glyf"]
    for name in glyf.keys():
        g = glyf[name]
        if hasattr(g, "program") and g.program is not None:
            g.program = ttProgram.Program()
            g.program.fromBytecode(b"")

    tmp = tempfile.NamedTemporaryFile(suffix=".ttf", delete=False)
    t.save(tmp.name)
    _unhinted_cache[font_path] = tmp.name
    return tmp.name


def load_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    path = FONTS_DIR / f"PlanetaireMono-{name}.ttf"
    unhinted = _strip_hinting(str(path))
    return ImageFont.truetype(unhinted, size)


def draw_hero(output: Path) -> None:
    """Hero image: code sample showing B612 letterforms in context."""
    width, height = 1500, 540
    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)

    font = load_font("Regular", 18)
    bold = load_font("ExtraBold", 18)
    italic = load_font("Italic", 18)

    y = 30
    lh = 28

    # Title
    draw.text((40, y), "# Planetaire Mono — B612 letterforms meet Hack infrastructure", DIM, font=font)
    y += lh * 2

    # Python code sample
    def code_line(y: int, parts: list[tuple[str, tuple[int, int, int], ImageFont.FreeTypeFont]]) -> int:
        x = 40
        for text, color, f in parts:
            draw.text((x, y), text, color, font=f)
            x += draw.textlength(text, font=f)
        return y + lh

    y = code_line(y, [
        ("def ", ACCENT_PURPLE, bold), ("analyze_trajectory", ACCENT_BLUE, font),
        ("(altitude: ", FG, font), ("float", ACCENT_CYAN, font),
        (", velocity: ", FG, font), ("float", ACCENT_CYAN, font),
        (") -> ", FG, font), ("dict", ACCENT_CYAN, font), (":", FG, font),
    ])
    y = code_line(y, [('    """Calculate orbital parameters from trajectory data."""', ACCENT_GREEN, italic)])
    y += lh

    y = code_line(y, [
        ("    G = ", FG, font), ("6.674e-11", ACCENT_ORANGE, font),
        ("  # gravitational constant (N⋅m²/kg²)", DIM, font),
    ])
    y = code_line(y, [
        ("    mass_earth = ", FG, font), ("5.972e24", ACCENT_ORANGE, font),
    ])
    y += lh

    y = code_line(y, [
        ("    if ", ACCENT_PURPLE, bold), ("altitude > ", FG, font),
        ("400_000", ACCENT_ORANGE, font), (":", FG, font),
    ])
    y = code_line(y, [
        ("        orbit_type = ", FG, font), ('"LEO"', ACCENT_GREEN, font),
        ("  # Low Earth Orbit", DIM, font),
    ])
    y = code_line(y, [
        ("    elif ", ACCENT_PURPLE, bold), ("altitude > ", FG, font),
        ("35_786_000", ACCENT_ORANGE, font), (":", FG, font),
    ])
    y = code_line(y, [
        ("        orbit_type = ", FG, font), ('"GEO"', ACCENT_GREEN, font),
        ("  # Geostationary", DIM, font),
    ])
    y += lh

    y = code_line(y, [
        ("    period = ", FG, font), ("2", ACCENT_ORANGE, font),
        (" * math.pi * math.sqrt(altitude**", FG, font),
        ("3", ACCENT_ORANGE, font), (" / (G * mass_earth))", FG, font),
    ])
    y += lh

    y = code_line(y, [
        ("    return ", ACCENT_PURPLE, bold),
        ("{", FG, font), ('"type"', ACCENT_GREEN, font),
        (": orbit_type, ", FG, font), ('"period"', ACCENT_GREEN, font),
        (": period, ", FG, font), ('"v"', ACCENT_GREEN, font),
        (": velocity}", FG, font),
    ])

    img.save(output / "hero.png")


def draw_weights(output: Path) -> None:
    """Weight comparison: all 8 variants."""
    width, height = 1500, 700
    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)

    y = 30
    lh = 34

    title_font = load_font("Regular", 15)
    draw.text((40, y), "WEIGHT COMPARISON", DIM, font=title_font)
    y += lh + 5

    sample = "The quick brown fox jumps over the lazy dog"

    weights = [
        ("Regular (400)", "Regular", FG),
        ("Italic (400)", "Italic", FG),
        ("Medium (500)", "Medium", FG),
        ("Medium Italic (500)", "MediumItalic", FG),
        ("Bold (700)", "Bold", FG),
        ("Bold Italic (700)", "BoldItalic", FG),
        ("ExtraBold (800)  ★", "ExtraBold", ACCENT_CYAN),
        ("ExtraBold Italic (800)", "ExtraBoldItalic", ACCENT_CYAN),
    ]

    label_font = load_font("Regular", 13)
    for label, variant, color in weights:
        draw.text((40, y + 2), label, DIM, font=label_font)
        font = load_font(variant, 18)
        draw.text((320, y), sample, color, font=font)
        y += lh

    y += 20
    draw.text((40, y), "DIGITS AND SYMBOLS", DIM, font=title_font)
    y += lh

    digits = "0123456789   AaBbCcDd   {[()]} <=> !@#$%"
    for label, variant, color in weights:
        font = load_font(variant, 18)
        draw.text((40, y), digits, color, font=font)
        y += lh - 4

    img.save(output / "weights.png")


def draw_features(output: Path) -> None:
    """Feature showcase: distinctive characters and coverage."""
    width, height = 1500, 480
    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)

    font = load_font("Regular", 18)
    bold = load_font("ExtraBold", 18)
    title_font = load_font("Regular", 15)

    y = 30
    lh = 30

    draw.text((40, y), "DISTINCTIVE CHARACTERS — B612 LETTERFORMS", DIM, font=title_font)
    y += lh + 8

    pairs = [
        ("Easily distinguished:", "  Il1|  O0Oo  rn m  cl d  {} [] ()"),
        ("Common confusables:", "  Il1|  0OoQ  5S  8B  2Z  9g  6b  :;"),
        ("Extended Latin:", "  ÀàÉéÎîÖöÜü  ŁłŃńŠšŽž  ÆæØøÞþ"),
        ("Greek & Cyrillic:", "  ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδ"),
    ]

    for label, chars in pairs:
        draw.text((40, y), label, DIM, font=font)
        draw.text((40 + draw.textlength(label, font=font), y), chars, FG, font=bold)
        y += lh + 8

    y += 12
    draw.text((40, y), "NERD FONT ICONS (FROM HACK BASE)", DIM, font=title_font)
    y += lh + 5

    # Powerline + common Nerd Font glyphs
    draw.text((40, y), "Powerline:  ", DIM, font=font)
    x = 40 + draw.textlength("Powerline:  ", font=font)
    icons_pw = "\ue0a0  \ue0a1  \ue0a2  \ue0b0  \ue0b2"
    draw.text((x, y), icons_pw, ACCENT_CYAN, font=font)
    y += lh + 3

    draw.text((40, y), "Dev icons:  ", DIM, font=font)
    x = 40 + draw.textlength("Dev icons:  ", font=font)
    icons_dev = "\uf015  \uf07c  \uf013  \uf0e7  \uf121  \uf1d3  \uf09b  \uf268  \uf1c0  \uf233"
    draw.text((x, y), icons_dev, ACCENT_CYAN, font=font)

    img.save(output / "features.png")


def draw_terminal_bold(output: Path) -> None:
    """Show why ExtraBold matters for terminals."""
    width, height = 1500, 480
    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)

    title_font = load_font("Regular", 15)
    small = load_font("Regular", 14)
    regular = load_font("Regular", 18)
    bold = load_font("Bold", 18)
    extrabold = load_font("ExtraBold", 18)

    y = 30
    lh = 28

    draw.text((40, y), "WHY EXTRABOLD FOR TERMINALS", DIM, font=title_font)
    y += lh + 5

    draw.text((40, y), "Set fontWeightBold = 800 in your terminal for maximum contrast between", DIM, font=small)
    y += lh - 4
    draw.text((40, y), "regular and bold text. This is the key to readable terminal output.", DIM, font=small)
    y += lh + 15

    # Simulated terminal prompts
    prompt = "user@host"
    path = " ~/projects/planetaire"
    branch = "  main"
    cmd = " $ make build"

    for label, font_used, highlight in [
        ("Regular (400):", regular, DIM),
        ("Bold (700):", bold, DIM),
        ("ExtraBold (800):", extrabold, ACCENT_CYAN),
    ]:
        draw.text((40, y), label, highlight, font=small)
        y += lh
        x = 60
        draw.text((x, y), prompt, ACCENT_GREEN, font=font_used)
        x += draw.textlength(prompt, font=font_used)
        draw.text((x, y), path, ACCENT_BLUE, font=font_used)
        x += draw.textlength(path, font=font_used)
        draw.text((x, y), branch, ACCENT_PURPLE, font=font_used)
        x += draw.textlength(branch, font=font_used)
        draw.text((x, y), cmd, FG, font=font_used)
        y += lh + 15

    y += 10
    draw.text((40, y), "TERMINAL CONFIGURATION", DIM, font=title_font)
    y += lh + 5

    config_lines = [
        ('Ghostty:    font-family = "Planetaire Mono"  font-thicken = true', FG),
        ('Alacritty:  bold = { family = "Planetaire Mono", style = "ExtraBold" }', FG),
        ('WezTerm:    config.font = wezterm.font("Planetaire Mono", {weight="ExtraBold"})', FG),
    ]
    for line, color in config_lines:
        draw.text((40, y), line, color, font=small)
        y += lh - 2

    img.save(output / "terminal-bold.png")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate font showcase images")
    parser.add_argument("--output-dir", default="docs/images", help="Output directory")
    args = parser.parse_args()

    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)

    if not FONTS_DIR.exists() or not list(FONTS_DIR.glob("*.ttf")):
        print("Error: No built fonts found. Run 'make fonts' first.")
        raise SystemExit(1)

    print("Generating showcase images...")
    draw_hero(output)
    print("  hero.png")
    draw_weights(output)
    print("  weights.png")
    draw_features(output)
    print("  features.png")
    draw_terminal_bold(output)
    print("  terminal-bold.png")
    print(f"Done! Images saved to {output}/")


if __name__ == "__main__":
    main()
