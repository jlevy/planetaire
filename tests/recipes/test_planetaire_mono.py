"""Integration test for the full Planetaire Mono build pipeline."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from fontTools.ttLib import TTFont

from planetaire.ops.info import inspect_font
from planetaire.recipes.planetaire_mono import build_planetaire_mono, build_text

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


def test_build_text_regular(source_dir: Path):
    """Text build subsets to text glyphs, drops icons, and emits web formats + CSS."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        outputs = build_text(source_dir, output_dir, variant="Regular")

        names = {p.name for p in outputs}
        assert "PlanetaireMonoText-Regular.woff2" in names
        assert "PlanetaireMonoText-Regular.woff" in names
        assert "PlanetaireMonoText-Regular.ttf" in names
        assert "planetaire-mono-text.css" in names

        ttf = output_dir / "PlanetaireMonoText-Regular.ttf"
        info = inspect_font(ttf)
        assert info.family == "Planetaire Mono Text"
        # Far smaller than the full ~12k-glyph build.
        assert info.glyph_count < 2000

        cmap = TTFont(ttf).getBestCmap()
        assert cmap is not None
        for cp in range(0x41, 0x5B):  # ASCII letters kept
            assert cp in cmap
        assert 0x2500 in cmap  # box-drawing kept
        assert 0xE0A0 not in cmap  # Powerline/PUA icons dropped

        css = (output_dir / "planetaire-mono-text.css").read_text()
        assert "Planetaire Mono Text" in css
        assert "woff2" in css
        assert "font-weight: 400" in css


def test_build_all_variants(source_dir: Path):
    """Full pipeline builds all 8 variants."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        outputs = build_planetaire_mono(source_dir, output_dir)

        assert len(outputs) == 8
        names = {p.name for p in outputs}
        assert "PlanetaireMono-Regular.ttf" in names
        assert "PlanetaireMono-Italic.ttf" in names
        assert "PlanetaireMono-Medium.ttf" in names
        assert "PlanetaireMono-MediumItalic.ttf" in names
        assert "PlanetaireMono-Bold.ttf" in names
        assert "PlanetaireMono-BoldItalic.ttf" in names
        assert "PlanetaireMono-ExtraBold.ttf" in names
        assert "PlanetaireMono-ExtraBoldItalic.ttf" in names

        # Verify weights across the family
        for filename, expected_weight in [
            ("PlanetaireMono-Medium.ttf", 500),
            ("PlanetaireMono-Bold.ttf", 700),
            ("PlanetaireMono-ExtraBold.ttf", 800),
        ]:
            path = [p for p in outputs if p.name == filename][0]
            info = inspect_font(path)
            assert info.weight_class == expected_weight, (
                f"{filename}: expected weight {expected_weight}, got {info.weight_class}"
            )
