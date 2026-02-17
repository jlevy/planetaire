"""Tests for ops/fix — post-processing fixes."""

from __future__ import annotations

from fontTools.ttLib import TTFont

from planetaire.ops.fix import fix_font


def test_fix_adds_dsig(base_font: TTFont):
    # Remove DSIG if present
    if "DSIG" in base_font:
        del base_font["DSIG"]

    result = fix_font(base_font)
    assert "DSIG" in result


def test_fix_sets_fstype(base_font: TTFont):
    base_font["OS/2"].fsType = 8  # Editable embedding
    result = fix_font(base_font)
    assert result["OS/2"].fsType == 0


def test_fix_sets_gasp(base_font: TTFont):
    result = fix_font(base_font)
    assert "gasp" in result
    assert 0xFFFF in result["gasp"].gaspRange


def test_fix_idempotent(base_font: TTFont):
    """Applying fix twice produces same result."""
    result1 = fix_font(base_font)
    result2 = fix_font(result1)
    assert result2["OS/2"].fsType == 0
    assert "DSIG" in result2
    assert 0xFFFF in result2["gasp"].gaspRange
