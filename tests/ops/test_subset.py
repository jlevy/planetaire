"""Tests for ops/subset — glyph subsetting and web-font output."""

from __future__ import annotations

from pathlib import Path

from fontTools.ttLib import TTFont

from planetaire.ops.subset import save_web_font, subset_font


def test_subset_keeps_only_requested_ranges(base_font: TTFont):
    subset_font(base_font, [(0x41, 0x5A)])  # A-Z only
    cmap = base_font.getBestCmap()
    assert 0x41 in cmap  # A kept
    assert 0x5A in cmap  # Z kept
    assert 0x30 not in cmap  # digit dropped
    assert 0x61 not in cmap  # lowercase dropped


def test_save_web_font_woff2(base_font: TTFont, tmp_path: Path):
    subset_font(base_font, [(0x41, 0x5A)])
    out = tmp_path / "out.woff2"
    save_web_font(base_font, out, flavor="woff2")
    assert out.exists()
    assert TTFont(out).flavor == "woff2"


def test_save_web_font_ttf(base_font: TTFont, tmp_path: Path):
    out = tmp_path / "out.ttf"
    save_web_font(base_font, out, flavor=None)
    assert out.exists()
    assert TTFont(out).flavor is None
