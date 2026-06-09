"""Integration test for the full Planetaire Mono build pipeline."""

from __future__ import annotations

import logging
import tempfile
from pathlib import Path

import pytest
from fontTools.ttLib import TTFont

from planetaire.config import TEXT_SUBSET_GROUPS
from planetaire.ops.info import inspect_font
from planetaire.recipes.planetaire_mono import build_planetaire_mono, build_text

FONTS_SOURCE = Path(__file__).parent.parent.parent / "fonts" / "source"


@pytest.fixture
def source_dir() -> Path:
    if not (FONTS_SOURCE / "b612").exists() or not (FONTS_SOURCE / "hack").exists():
        pytest.skip("Source fonts not available")
    return FONTS_SOURCE


def _css_pct(value: float) -> str:
    text = f"{value:.1f}".rstrip("0").rstrip(".")
    return f"{text}%"


def _font_metric_pct(font: TTFont, metric: str) -> str:
    hhea = font["hhea"]
    units_per_em = font["head"].unitsPerEm
    value = getattr(hhea, metric)
    if metric == "descent":
        value = abs(value)
    return _css_pct((value / units_per_em) * 100)


def test_build_produces_regular(source_dir: Path):
    """Full pipeline produces a valid Planetaire Mono Regular."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        outputs = build_planetaire_mono(source_dir, output_dir, variant="Regular")

        # Extended is a superset: TTF (local) plus WOFF2/WOFF + CSS (web).
        names = {p.name for p in outputs}
        assert "PlanetaireMonoExtended-Regular.ttf" in names
        assert "PlanetaireMonoExtended-Regular.woff2" in names
        assert "PlanetaireMonoExtended-Regular.woff" not in names  # WOFF2-only
        assert "planetaire-mono-extended.css" in names
        css = (output_dir / "planetaire-mono-extended.css").read_text()
        assert "Planetaire Mono Extended" in css and "woff2" in css
        output_path = output_dir / "PlanetaireMonoExtended-Regular.ttf"
        assert output_path.exists()

        # Verify metadata
        info = inspect_font(output_path)
        assert info.family == "Planetaire Mono Extended"
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
        assert "PlanetaireMonoText-Regular.woff" not in names  # web fonts are WOFF2-only
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


def test_build_text_split_regular(source_dir: Path):
    """Split Text build emits Google Fonts-style Latin range WOFF2s + CSS."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        outputs = build_text(
            source_dir,
            output_dir,
            variant="Regular",
            split=True,
            formats=("woff2",),
        )

        names = {p.name for p in outputs}
        assert "PlanetaireMonoText-Regular-latin.woff2" in names
        assert "PlanetaireMonoText-Regular-latin-ext.woff2" in names
        assert "PlanetaireMonoText-Regular.ttf" not in names
        assert "planetaire-mono-text.css" in names
        assert "planetaire-mono-text-italics.css" not in names

        latin = TTFont(output_dir / "PlanetaireMonoText-Regular-latin.woff2")
        latin_cmap = latin.getBestCmap()
        assert latin_cmap is not None
        assert 0x0041 in latin_cmap  # Basic Latin
        assert 0x00E9 in latin_cmap  # Latin-1
        assert 0x0100 not in latin_cmap  # Latin Extended lives in the companion file
        assert 0x2500 not in latin_cmap  # Box drawing is not a Google Fonts Latin subset

        latin_ext = TTFont(output_dir / "PlanetaireMonoText-Regular-latin-ext.woff2")
        latin_ext_cmap = latin_ext.getBestCmap()
        assert latin_ext_cmap is not None
        assert 0x0100 in latin_ext_cmap
        assert 0x0041 not in latin_ext_cmap

        css = (output_dir / "planetaire-mono-text.css").read_text()
        assert css.count("font-family: 'Planetaire Mono Text';") == 2
        assert "font-family: 'Planetaire Mono Text Fallback';" in css
        assert "--planetaire-mono-text-font-stack" in css
        assert "size-adjust: 100%;" in css
        assert f"ascent-override: {_font_metric_pct(latin, 'ascent')};" in css
        assert f"descent-override: {_font_metric_pct(latin, 'descent')};" in css
        assert f"line-gap-override: {_font_metric_pct(latin, 'lineGap')};" in css
        assert "font-style: normal" in css
        assert "font-weight: 400" in css
        assert "PlanetaireMonoText-Regular-latin.woff2" in css
        assert "unicode-range: U+0000-00FF,U+0131" in css
        assert "unicode-range: U+0100-024F,U+0259" in css


def test_build_text_split_italic_companion(source_dir: Path):
    """Split italic variants are emitted as an optional companion stylesheet."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        outputs = build_text(
            source_dir,
            output_dir,
            variant="Italic",
            split=True,
            formats=("woff2",),
        )

        names = {p.name for p in outputs}
        assert "PlanetaireMonoText-Italic-latin.woff2" in names
        assert "PlanetaireMonoText-Italic-latin-ext.woff2" in names
        assert "planetaire-mono-text.css" not in names
        assert "planetaire-mono-text-italics.css" in names

        css = (output_dir / "planetaire-mono-text-italics.css").read_text()
        assert css.count("font-family: 'Planetaire Mono Text';") == 2
        assert "font-family: 'Planetaire Mono Text Fallback';" not in css
        assert "--planetaire-mono-text-font-stack" not in css
        assert "font-style: italic" in css
        assert "font-weight: 400" in css
        assert "unicode-range: U+0000-00FF,U+0131" in css


def test_build_text_split_italics_companion_does_not_duplicate_fallback(source_dir: Path):
    """Base split CSS owns the fallback stack; italic CSS stays purely additive."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        build_text(
            source_dir,
            output_dir,
            split=True,
            subsets=("latin",),
            formats=("woff2",),
            include_italics=True,
        )

        base_css = (output_dir / "planetaire-mono-text.css").read_text()
        italic_css = (output_dir / "planetaire-mono-text-italics.css").read_text()
        combined_css = base_css + italic_css

        assert "font-family: 'Planetaire Mono Text Fallback';" in base_css
        assert "font-family: 'Planetaire Mono Text Fallback';" not in italic_css
        assert combined_css.count("font-family: 'Planetaire Mono Text Fallback';") == 1
        assert "--planetaire-mono-text-font-stack" in base_css
        assert "--planetaire-mono-text-font-stack" not in italic_css


def test_build_text_split_warns_when_non_web_formats_are_ignored(
    source_dir: Path, caplog: pytest.LogCaptureFixture
):
    """Split web builds warn before defaulting a non-web-only request to WOFF2."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        with caplog.at_level(logging.WARNING):
            outputs = build_text(
                source_dir,
                output_dir,
                variant="Regular",
                split=True,
                subsets=("latin",),
                formats=("ttf",),
            )

        names = {p.name for p in outputs}
        assert "PlanetaireMonoText-Regular-latin.woff2" in names
        assert "PlanetaireMonoText-Regular-latin.ttf" not in names
        assert "Split Text web build ignores non-web format(s): ttf" in caplog.text


def test_build_text_split_skips_empty_subset(
    source_dir: Path,
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
):
    """Requested subset names that match no encoded glyphs warn and produce no file."""
    monkeypatch.setitem(
        TEXT_SUBSET_GROUPS,
        "empty",
        {
            "name": "empty",
            "unicode_range": "U+10FFFF",
            "ranges": [(0x10FFFF, 0x10FFFF)],
        },
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        with caplog.at_level(logging.WARNING):
            outputs = build_text(
                source_dir,
                output_dir,
                variant="Regular",
                split=True,
                subsets=("empty",),
                formats=("woff2",),
            )

        assert outputs == []
        assert "subset empty: no codepoints match U+10FFFF" in caplog.text
        assert not any(output_dir.iterdir())


def test_no_dangling_composite_components(source_dir: Path):
    """Every composite glyph must reference components that exist in the font.

    Guards the merge step: B612's in-range glyphs are currently all simple
    contours, so no accented composite ends up referencing an uncopied component.
    This test fails loudly if a future donor introduces composites whose
    components are not carried over.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        build_planetaire_mono(source_dir, output_dir, variant="Regular")
        font = TTFont(output_dir / "PlanetaireMonoExtended-Regular.ttf")
        glyf = font["glyf"]
        order = set(font.getGlyphOrder())

        dangling: list[str] = []
        for name in font.getGlyphOrder():
            glyph = glyf[name]
            if glyph.isComposite():
                for comp in glyph.components:
                    if comp.glyphName not in order:
                        dangling.append(f"{name} -> {comp.glyphName}")

        assert dangling == [], f"Dangling composite components: {dangling[:10]}"


def test_build_all_variants(source_dir: Path):
    """Full pipeline builds all 10 variants."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        outputs = build_planetaire_mono(source_dir, output_dir)

        # 10 variants emitted as TTF + WOFF2 plus one @font-face CSS.
        ttf_names = {p.name for p in outputs if p.suffix == ".ttf"}
        assert len(ttf_names) == 10
        assert "PlanetaireMonoExtended-Regular.ttf" in ttf_names
        assert "PlanetaireMonoExtended-Italic.ttf" in ttf_names
        assert "PlanetaireMonoExtended-Medium.ttf" in ttf_names
        assert "PlanetaireMonoExtended-MediumItalic.ttf" in ttf_names
        assert "PlanetaireMonoExtended-SemiBold.ttf" in ttf_names
        assert "PlanetaireMonoExtended-SemiBoldItalic.ttf" in ttf_names
        assert "PlanetaireMonoExtended-Bold.ttf" in ttf_names
        assert "PlanetaireMonoExtended-BoldItalic.ttf" in ttf_names
        assert "PlanetaireMonoExtended-ExtraBold.ttf" in ttf_names
        assert "PlanetaireMonoExtended-ExtraBoldItalic.ttf" in ttf_names
        # Web fonts + CSS ship too (Extended is a superset of Text).
        all_names = {p.name for p in outputs}
        assert "PlanetaireMonoExtended-Regular.woff2" in all_names
        assert "PlanetaireMonoExtended-Regular.woff" not in all_names  # WOFF2-only
        assert "planetaire-mono-extended.css" in all_names

        # Verify weights across the family
        for filename, expected_weight in [
            ("PlanetaireMonoExtended-Medium.ttf", 500),
            ("PlanetaireMonoExtended-SemiBold.ttf", 600),
            ("PlanetaireMonoExtended-Bold.ttf", 700),
            ("PlanetaireMonoExtended-ExtraBold.ttf", 800),
        ]:
            path = [p for p in outputs if p.name == filename][0]
            info = inspect_font(path)
            assert info.weight_class == expected_weight, (
                f"{filename}: expected weight {expected_weight}, got {info.weight_class}"
            )
