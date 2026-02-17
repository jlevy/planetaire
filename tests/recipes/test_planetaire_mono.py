"""Integration test for the full Planetaire Mono build pipeline."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from fontTools.ttLib import TTFont

from planetaire.ops.info import inspect_font
from planetaire.recipes.planetaire_mono import build_planetaire_mono

FONTS_SOURCE = Path(__file__).parent.parent.parent / "fonts" / "source"


@pytest.fixture
def source_dir() -> Path:
    if not (FONTS_SOURCE / "b612").exists() or not (FONTS_SOURCE / "hack").exists():
        pytest.skip("Source fonts not available")
    return FONTS_SOURCE


def test_build_produces_regular(source_dir: Path):
    """Full pipeline produces a valid Planetaire Mono Regular."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        outputs = build_planetaire_mono(source_dir, output_dir, variant="Regular")

        assert len(outputs) == 1
        output_path = outputs[0]
        assert output_path.exists()
        assert output_path.name == "PlanetaireMono-Regular.ttf"

        # Verify metadata
        info = inspect_font(output_path)
        assert info.family == "Planetaire Mono"
        assert info.weight_class == 400
        assert info.glyph_count > 1000

        # Verify the font has both B612 and Hack glyphs
        font = TTFont(output_path)
        cmap = font.getBestCmap()
        assert cmap is not None
        # ASCII letters (from B612)
        for cp in range(0x41, 0x5B):
            assert cp in cmap
        # Nerd Font glyphs should still be present (from Hack base)
        # U+E0A0 is a Powerline glyph
        assert 0xE0A0 in cmap


def test_build_all_variants(source_dir: Path):
    """Full pipeline builds all 10 variants."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        outputs = build_planetaire_mono(source_dir, output_dir)

        assert len(outputs) == 10
        names = {p.name for p in outputs}
        assert "PlanetaireMono-Regular.ttf" in names
        assert "PlanetaireMono-Italic.ttf" in names
        assert "PlanetaireMono-Medium.ttf" in names
        assert "PlanetaireMono-MediumItalic.ttf" in names
        assert "PlanetaireMono-SemiBold.ttf" in names
        assert "PlanetaireMono-SemiBoldItalic.ttf" in names
        assert "PlanetaireMono-Bold.ttf" in names
        assert "PlanetaireMono-BoldItalic.ttf" in names
        assert "PlanetaireMono-ExtraBold.ttf" in names
        assert "PlanetaireMono-ExtraBoldItalic.ttf" in names

        # Verify weights across the family
        for filename, expected_weight in [
            ("PlanetaireMono-Medium.ttf", 500),
            ("PlanetaireMono-SemiBold.ttf", 600),
            ("PlanetaireMono-Bold.ttf", 700),
            ("PlanetaireMono-ExtraBold.ttf", 800),
        ]:
            path = [p for p in outputs if p.name == filename][0]
            info = inspect_font(path)
            assert info.weight_class == expected_weight, (
                f"{filename}: expected weight {expected_weight}, got {info.weight_class}"
            )
