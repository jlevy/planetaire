"""Locate and integrity-check source fonts.

B612 Mono: original polarsys/b612 from Airbus/Intactile DESIGN.
Hack Nerd Font: from ryanoasis/nerd-fonts releases.

The source fonts are currently vendored under ``fonts/source/`` and verified
against ``fonts/source/SHA256SUMS``. (Network downloading from upstream is not yet
implemented; until then this step locates the vendored fonts and checks their
integrity.) B612 Medium/SemiBold/ExtraBold and Hack Medium/SemiBold are generated
from the base weights via FontForge emboldening (see ops/embolden.py) when not
already present.
"""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path

log = logging.getLogger(__name__)

CHECKSUM_FILE = "SHA256SUMS"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_checksums(path: Path) -> dict[str, str]:
    """Parse a ``SHA256SUMS`` file into {relative_path: hash}."""
    checksums: dict[str, str] = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        digest, _, name = line.partition("  ")
        if name:
            checksums[name.strip()] = digest.strip()
    return checksums


def verify_sources(output_dir: Path) -> dict[str, Path]:
    """Verify vendored source fonts against ``SHA256SUMS``.

    Returns a dict mapping ``"<subdir>/<file>"`` to its path for every verified
    font.

    Raises:
        FileNotFoundError: if no source fonts (or the checksum file) are found.
        ValueError: if any font's hash does not match the recorded checksum.
    """
    checksum_path = output_dir / CHECKSUM_FILE
    expected = _load_checksums(checksum_path) if checksum_path.exists() else {}
    if not expected:
        log.warning("No %s found in %s; skipping integrity check", CHECKSUM_FILE, output_dir)

    fonts: dict[str, Path] = {}
    mismatches: list[str] = []

    for subdir in ("b612", "hack"):
        for path in sorted((output_dir / subdir).glob("*.ttf")):
            rel = f"{subdir}/{path.name}"
            fonts[rel] = path
            if rel in expected:
                actual = _sha256(path)
                if actual != expected[rel]:
                    mismatches.append(rel)
                    log.error("Checksum mismatch for %s", rel)

    if not fonts:
        raise FileNotFoundError(
            f"No source fonts found in {output_dir}. "
            "Copy fonts to fonts/source/ (b612/ and hack/) first."
        )

    if mismatches:
        raise ValueError(
            f"Source font integrity check failed for: {', '.join(mismatches)}. "
            "The vendored fonts differ from the recorded checksums."
        )

    verified = sum(1 for rel in fonts if rel in expected)
    log.info(
        "Located %d source font(s); %d verified against %s", len(fonts), verified, CHECKSUM_FILE
    )
    return fonts


def download_sources(output_dir: Path) -> dict[str, Path]:
    """Locate and verify source fonts (currently vendored, not network-fetched).

    Kept under the ``build download`` command name for compatibility. Returns a
    dict mapping ``"<subdir>/<file>"`` to its path.
    """
    return verify_sources(output_dir)
