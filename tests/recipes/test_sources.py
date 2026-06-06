"""Tests for recipes/sources — source font location and integrity checks."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from planetaire.recipes.sources import verify_sources


def _make_source_tree(root: Path) -> Path:
    """Create a fake fonts/source tree with one font + matching SHA256SUMS."""
    (root / "b612").mkdir(parents=True)
    (root / "hack").mkdir(parents=True)
    font = root / "hack" / "HackNerdFont-Regular.ttf"
    font.write_bytes(b"fake-font-bytes")
    digest = hashlib.sha256(font.read_bytes()).hexdigest()
    (root / "SHA256SUMS").write_text(f"{digest}  hack/HackNerdFont-Regular.ttf\n")
    return root


def test_verify_sources_passes_with_matching_checksums(tmp_path: Path):
    root = _make_source_tree(tmp_path)
    fonts = verify_sources(root)
    assert "hack/HackNerdFont-Regular.ttf" in fonts


def test_verify_sources_raises_on_mismatch(tmp_path: Path):
    root = _make_source_tree(tmp_path)
    # Corrupt the font after the checksum was recorded.
    (root / "hack" / "HackNerdFont-Regular.ttf").write_bytes(b"tampered")
    with pytest.raises(ValueError, match="integrity check failed"):
        verify_sources(root)


def test_verify_sources_raises_when_empty(tmp_path: Path):
    (tmp_path / "b612").mkdir()
    (tmp_path / "hack").mkdir()
    with pytest.raises(FileNotFoundError):
        verify_sources(tmp_path)
