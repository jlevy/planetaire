"""Glyph subsetting and web-font (WOFF/WOFF2) output.

Used to derive the lightweight "Text" family from the full build by keeping only
standard-Unicode text glyphs (letters, punctuation, box-drawing, ...) and dropping
the thousands of Private-Use Nerd Font icons, which is where nearly all the size is.
"""

from __future__ import annotations

import os
from pathlib import Path

from fontTools.misc.timeTools import timestampSinceEpoch
from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont
from strif import atomic_output_file

from planetaire.config import DEFAULT_SOURCE_DATE_EPOCH
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


def build_timestamp() -> int:
    """Return the deterministic `head.modified` value, in OpenType LONGDATETIME.

    Honours ``SOURCE_DATE_EPOCH`` (the reproducible-builds standard: Unix epoch
    seconds) when it is set, otherwise a fixed project epoch. `timestampSinceEpoch`
    converts to the OpenType 1904-based epoch.

    A malformed ``SOURCE_DATE_EPOCH`` raises rather than silently falling back, so a
    build that meant to be stamped never quietly gets the fallback instead.
    """
    raw = os.environ.get("SOURCE_DATE_EPOCH")
    if raw is None or not raw.strip():
        return timestampSinceEpoch(DEFAULT_SOURCE_DATE_EPOCH)
    try:
        epoch = int(raw.strip())
    except ValueError as exc:
        raise ValueError(f"SOURCE_DATE_EPOCH must be Unix epoch seconds (got {raw!r})") from exc
    return timestampSinceEpoch(epoch)


def save_web_font(font: TTFont, path: Path, *, flavor: str | None = None) -> None:
    """Save `font` as TTF (flavor=None), WOFF (``"woff"``) or WOFF2 (``"woff2"``).

    WOFF2 requires the ``brotli`` package (pulled in via ``fonttools[woff]``).

    Every font artifact this project writes goes through here, so this is also where
    the build is made byte-reproducible. fontTools otherwise stamps `head.modified`
    from the wall clock at save time (``TTFont.recalcTimestamp`` defaults to true),
    which — together with the `head.checkSumAdjustment` derived from the file content
    — is the only thing that differs between two builds of the same sources. Pinning
    the timestamp and disabling the recalculation makes a rebuild byte-identical,
    which is what lets CI gate the committed `fonts/web/` binaries against a rebuild.
    """
    if "head" in font:
        font["head"].modified = build_timestamp()
    font.recalcTimestamp = False
    font.flavor = flavor
    path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(str(path)) as tmp:
        font.save(tmp)
