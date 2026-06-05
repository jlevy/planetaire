"""Tests for recipes/site — static site assembly."""

from __future__ import annotations

from pathlib import Path

from planetaire.recipes.site import generate_site


def test_generate_site_minimal(tmp_path: Path):
    """Site builds even when only some assets exist, embedding what's present."""
    fonts = tmp_path / "fonts"
    fonts.mkdir()
    (fonts / "planetaire-mono-text.css").write_text("/* css */")
    (fonts / "specimen.html").write_text("<html></html>")

    out = tmp_path / "site"
    index = generate_site(out, fonts, images_dir=fonts, version="1.2.3")

    assert index.exists()
    html = index.read_text()
    assert "Planetaire Mono" in html
    assert "v1.2.3" in html
    assert "specimen.html" in html  # specimen linked
    assert (out / "specimen.html").exists()  # copied in
    assert (out / "planetaire-mono-text.css").exists()


def test_generate_site_includes_optional_demo(tmp_path: Path):
    fonts = tmp_path / "fonts"
    fonts.mkdir()
    (fonts / "terminal-demo.svg").write_text("<svg></svg>")

    out = tmp_path / "site"
    html = generate_site(out, fonts, images_dir=fonts, version="0.1.0").read_text()
    assert "terminal-demo.svg" in html
    assert (out / "terminal-demo.svg").exists()
