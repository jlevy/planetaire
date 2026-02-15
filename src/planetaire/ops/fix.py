"""
Post-processing fixes for font files.

Implements the fixes from gftools fix-nonhinting: DSIG placeholder,
fsType embedding bits, and GASP table for optimal rendering.
"""

from __future__ import annotations

from fontTools.ttLib import TTFont


def fix_font(font: TTFont) -> TTFont:
    """
    Apply standard post-processing fixes.

    1. Add empty DSIG table (digital signature placeholder).
    2. Set OS/2.fsType = 0 (installable embedding allowed).
    3. Fix GASP table for optimal rendering across screen sizes.
    """
    _fix_dsig(font)
    _fix_fstype(font)
    _fix_gasp(font)
    return font


def _fix_dsig(font: TTFont) -> None:
    """Add an empty DSIG table if missing (required by some validators)."""
    if "DSIG" not in font:
        from fontTools.ttLib import newTable

        dsig = newTable("DSIG")
        dsig.ulVersion = 1  # pyright: ignore
        dsig.usFlag = 0  # pyright: ignore
        dsig.usNumSigs = 0  # pyright: ignore
        dsig.signatureRecords = []  # pyright: ignore
        font["DSIG"] = dsig


def _fix_fstype(font: TTFont) -> None:
    """Set fsType to 0 (installable embedding)."""
    if "OS/2" in font:
        font["OS/2"].fsType = 0


def _fix_gasp(font: TTFont) -> None:
    """
    Set GASP table for optimal rendering.

    Range 0xFFFF with flags 0x000A means: use gridfitting and symmetric
    smoothing at all sizes.
    """
    if "gasp" not in font:
        from fontTools.ttLib import newTable

        gasp = newTable("gasp")
        font["gasp"] = gasp

    font["gasp"].gaspRange = {0xFFFF: 0x000A}  # pyright: ignore
