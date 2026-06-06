"""Tests for ops/regression — manifest save/load (incl. gzip)."""

from __future__ import annotations

from pathlib import Path

import pytest

from planetaire.ops.regression import (
    FontManifest,
    GlyphEntry,
    VariantManifest,
    load_manifest,
    save_manifest,
)


def _sample_manifest() -> FontManifest:
    manifest = FontManifest(version="1.2.3")
    manifest.variants.append(
        VariantManifest(
            variant="Regular",
            filename="PlanetaireMono-Regular.ttf",
            glyph_count=1,
            upm=2000,
            weight=400,
            glyphs=[
                GlyphEntry(codepoint=0x41, name="A", glyf_hash="abc", advance_width=1200, lsb=100)
            ],
        )
    )
    return manifest


@pytest.mark.parametrize("filename", ["manifest.json", "manifest.json.gz"])
def test_manifest_roundtrip(filename: str, tmp_path: Path):
    path = tmp_path / filename
    save_manifest(_sample_manifest(), path)
    assert path.exists()

    loaded = load_manifest(path)
    assert loaded.version == "1.2.3"
    assert len(loaded.variants) == 1
    assert loaded.variants[0].glyphs[0].name == "A"


def test_gzip_manifest_is_smaller(tmp_path: Path):
    plain = tmp_path / "m.json"
    gz = tmp_path / "m.json.gz"
    # Repeat glyphs so compression has something to chew on.
    manifest = _sample_manifest()
    manifest.variants[0].glyphs *= 200
    save_manifest(manifest, plain)
    save_manifest(manifest, gz)
    assert gz.stat().st_size < plain.stat().st_size
