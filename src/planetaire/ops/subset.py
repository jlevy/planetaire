"""Glyph subsetting and web-font (WOFF/WOFF2) output.

Used to derive the lightweight "Text" family from the full build by keeping only
standard-Unicode text glyphs (letters, punctuation, box-drawing, ...) and dropping
the thousands of Private-Use Nerd Font icons, which is where nearly all the size is.
"""

from __future__ import annotations

from pathlib import Path

from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont
from strif import atomic_output_file

from planetaire.unicode_ranges import codepoints_in_ranges

WEB_NAME_IDS: list[int] = [0, 1, 2, 3, 4, 5, 6, 13, 14, 16, 17]
WINDOWS_ENGLISH = 0x0409


def subset_font(
    font: TTFont, ranges: list[tuple[int, int]], *, drop_hinting: bool = False
) -> TTFont:
    """Subset `font` in place to the codepoints within `ranges`, returning it.

    Layout features are pruned to the retained glyphs, and component glyphs
    referenced by retained composites are kept automatically (subsetter closure),
    so accented Latin/Greek/Cyrillic continue to render.

    When ``drop_hinting`` is set, TrueType hinting tables/instructions are removed.
    This roughly halves web-font size and avoids carrying Hack's hinting (which is
    tuned for Hack outlines, not the merged B612 letterforms) — a sensible default
    for grayscale-antialiased web rendering.
    """
    options = Options()
    options.layout_features = ["*"]  # keep features (e.g. ss01/zero) for kept glyphs
    options.name_IDs = WEB_NAME_IDS
    options.name_legacy = False
    options.name_languages = [WINDOWS_ENGLISH]
    options.notdef_outline = True
    options.recalc_bounds = True
    options.recalc_timestamp = False
    options.glyph_names = False
    options.hinting = not drop_hinting
    options.drop_tables = []

    subsetter = Subsetter(options=options)
    subsetter.populate(unicodes=codepoints_in_ranges(ranges))
    subsetter.subset(font)
    return font


def save_web_font(font: TTFont, path: Path, *, flavor: str | None = None) -> None:
    """Save `font` as TTF (flavor=None), WOFF (``"woff"``) or WOFF2 (``"woff2"``).

    WOFF2 requires the ``brotli`` package (pulled in via ``fonttools[woff]``).
    """
    font.flavor = flavor
    path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(str(path)) as tmp:
        font.save(tmp)
