"""
Pipeline configuration: unicode ranges, variant definitions, and constants.

The letter ranges define which glyphs come from B612 (the donor font).
Everything else comes from Hack (the base font).

B612 source: original polarsys/b612 from Airbus/Intactile DESIGN.
"""

from __future__ import annotations

from typing import TypedDict

# Unicode ranges for B612 glyph selection.
# These glyphs are copied from B612 into the Hack base.
# Source: adapted from the kerm CSS font-stack unicode-range declarations.
PLANETAIRE_LETTER_RANGES: list[tuple[int, int]] = [
    (0x0031, 0x0039),  # Basic Latin digits 1-9 (zero kept from Hack for disambiguation)
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
# Note: the original B612 from polarsys has no special GSUB features.
# Ligatures (calt) and zero alternates (zero, ezer) were carlosedp additions.
# This list is empty now that we use original B612 sources.
# Future: re-implement dotted/slashed zero and ligatures in our own pipeline.
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
