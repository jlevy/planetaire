"""Tests for ops/subset — glyph subsetting and web-font output."""

from __future__ import annotations

from pathlib import Path

import pytest
from fontTools.misc.timeTools import timestampSinceEpoch
from fontTools.ttLib import TTFont

from planetaire.config import DEFAULT_SOURCE_DATE_EPOCH
from planetaire.ops.subset import build_timestamp, save_web_font, subset_font


def test_subset_keeps_only_requested_ranges(base_font: TTFont):
    subset_font(base_font, [(0x41, 0x5A)])  # A-Z only
    cmap = base_font.getBestCmap()
    assert cmap is not None
    assert 0x41 in cmap  # A kept
    assert 0x5A in cmap  # Z kept
    assert 0x30 not in cmap  # digit dropped
    assert 0x61 not in cmap  # lowercase dropped


def test_subset_drops_web_metadata_overhead(base_font: TTFont):
    """Web subsets drop glyph names and non-English name records."""
    subset_font(base_font, [(0x41, 0x5A)])

    assert base_font["post"].formatType == 3.0
    assert {name.langID for name in base_font["name"].names} <= {0x0409}


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


def test_save_web_font_is_byte_reproducible(
    base_font: TTFont, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """Two saves of the same font are byte-identical, not stamped with the wall clock."""
    monkeypatch.delenv("SOURCE_DATE_EPOCH", raising=False)
    first = tmp_path / "first.woff2"
    second = tmp_path / "second.woff2"
    save_web_font(base_font, first, flavor="woff2")
    save_web_font(base_font, second, flavor="woff2")

    assert first.read_bytes() == second.read_bytes()
    # Identical bytes alone would pass by luck if both saves landed in the same
    # second, so pin the value too.
    assert TTFont(first)["head"].modified == timestampSinceEpoch(DEFAULT_SOURCE_DATE_EPOCH)


def test_save_web_font_honours_source_date_epoch(
    base_font: TTFont, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "1234567890")
    out = tmp_path / "out.ttf"
    save_web_font(base_font, out)

    assert TTFont(out)["head"].modified == timestampSinceEpoch(1234567890)


def test_build_timestamp_rejects_malformed_source_date_epoch(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "yesterday")
    with pytest.raises(ValueError, match="SOURCE_DATE_EPOCH"):
        build_timestamp()
