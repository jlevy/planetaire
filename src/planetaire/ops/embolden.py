"""
ExtraBold weight generation via FontForge's changeWeight().

This is the only op requiring a system dependency. All others use pure
Python (fontTools).
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path


class SystemDependencyError(Exception):
    """A required system tool is not installed."""


def embolden_font(
    input_path: Path,
    output_path: Path,
    *,
    target_weight: int = 800,
    change_amount: int = 30,
    skip_glyphs: list[str] | None = None,
    half_weight_glyphs: list[str] | None = None,
) -> Path:
    """
    Generate a heavier weight variant using FontForge's changeWeight().

    Requires FontForge to be installed (`brew install fontforge` or
    `apt install fontforge`). Raises `SystemDependencyError` if not found.
    """
    fontforge_path = shutil.which("fontforge")
    if fontforge_path is None:
        raise SystemDependencyError(
            "FontForge is required for emboldening but was not found.\n"
            "Install it with:\n"
            "  macOS:  brew install fontforge\n"
            "  Linux:  apt install fontforge\n"
        )

    skip = skip_glyphs or []
    half = half_weight_glyphs or []

    # Build the FontForge Python script
    script = _build_fontforge_script(
        input_path=str(input_path),
        output_path=str(output_path),
        target_weight=target_weight,
        change_amount=change_amount,
        skip_glyphs=skip,
        half_weight_glyphs=half,
    )

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(script)
        script_path = f.name

    try:
        result = subprocess.run(
            [fontforge_path, "-script", script_path],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"FontForge embolden failed (exit {result.returncode}):\n{result.stderr}"
            )
    finally:
        Path(script_path).unlink(missing_ok=True)

    return output_path


def _build_fontforge_script(
    *,
    input_path: str,
    output_path: str,
    target_weight: int,
    change_amount: int,
    skip_glyphs: list[str],
    half_weight_glyphs: list[str],
) -> str:
    """Generate the FontForge Python script for emboldening."""
    skip_set = repr(set(skip_glyphs))
    half_set = repr(set(half_weight_glyphs))

    return f"""\
import fontforge

font = fontforge.open("{input_path}")
skip = {skip_set}
half = {half_set}

for glyph in font.glyphs():
    if glyph.glyphname in skip:
        continue
    amount = {change_amount}
    if glyph.glyphname in half:
        amount = amount // 2
    try:
        glyph.changeWeight(amount, "auto", 0, 0, "auto")
    except Exception:
        pass

font.os2_weight = {target_weight}
font.generate("{output_path}")
font.close()
"""
