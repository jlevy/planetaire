"""Tests for recipes/html_specimen — static HTML specimen generation."""

from __future__ import annotations

from pathlib import Path

from planetaire.recipes.html_specimen import generate_html_specimen


def test_generate_html_specimen(tmp_path: Path):
    out = generate_html_specimen(tmp_path / "specimen.html", version="1.2.3")
    assert out.exists()
    html = out.read_text()
    assert "Planetaire Mono Text" in html
    assert "Version 1.2.3" in html
    assert 'href="planetaire-mono-text.css"' in html
    assert "ss01" in html  # dotted-zero toggle
    assert "font-weight:800" in html  # weight ladder present


def test_generate_html_specimen_custom_css_href(tmp_path: Path):
    out = generate_html_specimen(
        tmp_path / "s.html", css_href="../fonts/pm-text.css", version="0.1.0"
    )
    assert 'href="../fonts/pm-text.css"' in out.read_text()
