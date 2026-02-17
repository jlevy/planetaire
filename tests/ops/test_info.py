"""Tests for ops/info — font metadata inspection."""

from __future__ import annotations

import tempfile
from pathlib import Path

from fontTools.ttLib import TTFont

from planetaire.ops.info import inspect_font


def test_inspect_minimal_font(base_font: TTFont):
    """inspect_font extracts correct metadata from a minimal font."""
    with tempfile.NamedTemporaryFile(suffix=".ttf", delete=False) as f:
        base_font.save(f.name)
        info = inspect_font(Path(f.name))

    assert info.family == "BaseFont"
    assert info.subfamily == "Regular"
    assert info.upm == 1000
    assert info.weight_class == 400
    assert info.glyph_count > 0
    assert not info.is_italic


def test_inspect_real_b612(b612_regular: TTFont):
    """inspect_font reads real B612 font metadata correctly."""
    with tempfile.NamedTemporaryFile(suffix=".ttf", delete=False) as f:
        b612_regular.save(f.name)
        info = inspect_font(Path(f.name))

    assert "B612" in info.family
    assert info.upm == 2000
    assert info.weight_class == 400
    assert info.glyph_count > 500


def test_inspect_real_hack(hack_regular: TTFont):
    """inspect_font reads real Hack font metadata correctly."""
    with tempfile.NamedTemporaryFile(suffix=".ttf", delete=False) as f:
        hack_regular.save(f.name)
        info = inspect_font(Path(f.name))

    assert "Hack" in info.family
    assert info.upm == 2048
    assert info.weight_class == 400
    assert info.glyph_count > 1000
