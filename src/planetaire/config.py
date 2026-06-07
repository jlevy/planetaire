"""
Pipeline configuration: unicode ranges, variant definitions, and constants.

The letter ranges define which glyphs come from B612 (the donor font).
Everything else comes from Hack (the base font).

B612 source: original polarsys/b612 from Airbus/Intactile DESIGN.
"""

from __future__ import annotations

from typing import TypedDict

# Font family names.
# The full build is "Planetaire Mono Extended" (all Nerd Font icons); the lightweight
# web/text subset is a distinct family so the two can be installed side by side.
FAMILY_NAME: str = "Planetaire Mono Extended"
TEXT_FAMILY_NAME: str = "Planetaire Mono Text"

# Unicode ranges retained in the lightweight "Text" family.
# These are the standard-Unicode text blocks (letters, punctuation, box-drawing,
# block elements, geometric shapes). Everything at/above the Private Use Area
# (Powerline at U+E0A0+ and the ~10k Nerd Font icons) is excluded, which is where
# essentially all the size lives.
TEXT_SUBSET_RANGES: list[tuple[int, int]] = [
    (0x0000, 0x00FF),  # Basic Latin + Latin-1 Supplement
    (0x0100, 0x024F),  # Latin Extended-A and B
    (0x0250, 0x02FF),  # IPA Extensions + Spacing Modifier Letters
    (0x0300, 0x036F),  # Combining Diacritical Marks (used by composites)
    (0x0370, 0x03FF),  # Greek and Coptic
    (0x0400, 0x052F),  # Cyrillic + Cyrillic Supplement
    (0x1E00, 0x1EFF),  # Latin Extended Additional
    (0x1F00, 0x1FFF),  # Greek Extended
    (0x2000, 0x206F),  # General Punctuation
    (0x2070, 0x209F),  # Superscripts and Subscripts
    (0x20A0, 0x20CF),  # Currency Symbols
    (0x2100, 0x214F),  # Letterlike Symbols
    (0x2150, 0x218F),  # Number Forms
    (0x2190, 0x21FF),  # Arrows
    (0x2200, 0x22FF),  # Mathematical Operators
    (0x2300, 0x23FF),  # Miscellaneous Technical
    (0x2500, 0x257F),  # Box Drawing
    (0x2580, 0x259F),  # Block Elements
    (0x25A0, 0x25FF),  # Geometric Shapes
    (0x2C60, 0x2C7F),  # Latin Extended-C
]

# Unicode ranges for B612 glyph selection.
# These glyphs are copied from B612 into the Hack base.
# Source: adapted from the kerm CSS font-stack unicode-range declarations.
PLANETAIRE_LETTER_RANGES: list[tuple[int, int]] = [
    (0x0030, 0x0039),  # Basic Latin digits 0-9 (dot added to zero in post-processing)
    (0x0041, 0x005A),  # Basic Latin uppercase
    (0x0061, 0x007A),  # Basic Latin lowercase
    (0x00C0, 0x00D6),  # Latin-1 uppercase with diacritics
    (0x00D8, 0x00F6),  # Latin-1 lowercase with diacritics
    (0x00F8, 0x00FF),  # Latin-1 more lowercase with diacritics
    (0x0100, 0x024F),  # Latin Extended-A and B
    (0x0370, 0x03FF),  # Greek and Coptic
    (0x0400, 0x04FF),  # Cyrillic
    (0x0500, 0x052F),  # Cyrillic Supplement
    (0x1E00, 0x1EFF),  # Latin Extended Additional
    (0x2C60, 0x2C7F),  # Latin Extended-C
]

# GSUB features to copy from B612 donor into merged font.
# The original B612 from polarsys has no special GSUB features, so this is empty.
# Dotted zero (circle default, rectangle alternate via ss01/zero features)
# is implemented via add_dotted_zero() in ops/zero.py.
PLANETAIRE_GSUB_FEATURES: list[str] = []


class VariantDef(TypedDict):
    """Definition for a Planetaire Mono font variant."""

    name: str
    hack_file: str
    b612_file: str
    subfamily: str
    weight: int


# Font variant definitions.
# Each variant maps to specific Hack and B612 source files.
VARIANTS: list[VariantDef] = [
    {
        "name": "Regular",
        "hack_file": "HackNerdFont-Regular.ttf",
        "b612_file": "B612Mono-Regular.ttf",
        "subfamily": "Regular",
        "weight": 400,
    },
    {
        "name": "Italic",
        "hack_file": "HackNerdFont-Italic.ttf",
        "b612_file": "B612Mono-Italic.ttf",
        "subfamily": "Italic",
        "weight": 400,
    },
    {
        "name": "Medium",
        "hack_file": "HackNerdFont-Medium.ttf",
        "b612_file": "B612Mono-Medium.ttf",
        "subfamily": "Medium",
        "weight": 500,
    },
    {
        "name": "MediumItalic",
        "hack_file": "HackNerdFont-MediumItalic.ttf",
        "b612_file": "B612Mono-MediumItalic.ttf",
        "subfamily": "Medium Italic",
        "weight": 500,
    },
    {
        "name": "SemiBold",
        "hack_file": "HackNerdFont-SemiBold.ttf",
        "b612_file": "B612Mono-SemiBold.ttf",
        "subfamily": "SemiBold",
        "weight": 600,
    },
    {
        "name": "SemiBoldItalic",
        "hack_file": "HackNerdFont-SemiBoldItalic.ttf",
        "b612_file": "B612Mono-SemiBoldItalic.ttf",
        "subfamily": "SemiBold Italic",
        "weight": 600,
    },
    {
        "name": "Bold",
        "hack_file": "HackNerdFont-Bold.ttf",
        "b612_file": "B612Mono-Bold.ttf",
        "subfamily": "Bold",
        "weight": 700,
    },
    {
        "name": "BoldItalic",
        "hack_file": "HackNerdFont-BoldItalic.ttf",
        "b612_file": "B612Mono-BoldItalic.ttf",
        "subfamily": "Bold Italic",
        "weight": 700,
    },
    {
        "name": "ExtraBold",
        "hack_file": "HackNerdFont-ExtraBold.ttf",
        "b612_file": "B612Mono-ExtraBold.ttf",
        "subfamily": "ExtraBold",
        "weight": 800,
    },
    {
        "name": "ExtraBoldItalic",
        "hack_file": "HackNerdFont-ExtraBoldItalic.ttf",
        "b612_file": "B612Mono-ExtraBoldItalic.ttf",
        "subfamily": "ExtraBold Italic",
        "weight": 800,
    },
]
