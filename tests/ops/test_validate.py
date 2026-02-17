"""Tests for ops/validate — font validation."""

from __future__ import annotations

from fontTools.ttLib import TTFont

from planetaire.ops.validate import validate_font


def test_validate_clean_font(base_font: TTFont):
    """A well-formed font with no expectations passes validation."""
    issues = validate_font(base_font)
    assert not any(i.severity == "error" for i in issues)


def test_validate_detects_weight_mismatch(base_font: TTFont):
    issues = validate_font(base_font, expected_weight=700)
    errors = [i for i in issues if i.severity == "error" and i.category == "metrics"]
    assert len(errors) == 1
    assert "700" in errors[0].message


def test_validate_detects_missing_glyphs(base_font: TTFont):
    # Expect Greek range, which our minimal font doesn't have
    issues = validate_font(base_font, expected_ranges=[(0x0370, 0x03FF)])
    errors = [i for i in issues if i.severity == "error" and i.category == "glyph_coverage"]
    assert len(errors) == 1
    assert "Missing" in errors[0].message


def test_validate_passes_with_correct_ranges(base_font: TTFont):
    # Expect A-Z which our font does have
    issues = validate_font(base_font, expected_ranges=[(0x0041, 0x005A)])
    errors = [i for i in issues if i.severity == "error" and i.category == "glyph_coverage"]
    assert len(errors) == 0


def test_validate_real_b612(b612_regular: TTFont):
    """Real B612 font passes basic validation."""
    issues = validate_font(b612_regular)
    errors = [i for i in issues if i.severity == "error"]
    assert len(errors) == 0
