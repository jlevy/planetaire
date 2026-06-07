"""
Heavier-weight generation via FontForge's changeWeight().

Used to derive the synthetic weights (Medium 500, SemiBold 600, ExtraBold 800)
from a lighter source face. This is the only op requiring a system dependency.
All others use pure Python (fontTools).
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
    max_points: int | None = None,
) -> Path:
    """
    Generate a heavier weight variant using FontForge's changeWeight().

    Requires FontForge to be installed (`brew install fontforge` or
    `apt install fontforge`). Raises `SystemDependencyError` if not found.

    ``max_points`` caps which glyphs are emboldened: any glyph whose on/off-curve
    point count exceeds the cap keeps its source outline. ``changeWeight`` does
    stroke expansion with self-intersection removal that scales steeply with point
    count, so a few dozen ultra-dense Nerd Font logo glyphs (up to ~4,700 points)
    would otherwise dominate the runtime -- a full-font pass runs well over an hour.
    Capping them keeps generation to a few minutes with no visible difference (those
    glyphs render identically at any normal size; see TODO.md to revisit full
    fidelity). The emboldened masters are vendored so normal builds and CI never run
    this op.
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
        max_points=max_points,
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
    max_points: int | None = None,
) -> str:
    """Generate the FontForge Python script for emboldening."""
    skip_set = repr(set(skip_glyphs))
    half_set = repr(set(half_weight_glyphs))

    return f"""\
import fontforge

font = fontforge.open({input_path!r})
skip = {skip_set}
half = {half_set}
max_points = {max_points!r}

def too_dense(glyph):
    if max_points is None:
        return False
    return sum(len(contour) for contour in glyph.foreground) > max_points

for glyph in font.glyphs():
    if glyph.glyphname in skip:
        continue
    # Skip ultra-dense glyphs (a few Nerd Font logos): changeWeight's
    # self-intersection removal is ~quadratic in point count, so these cost
    # minutes each for no visible gain. They keep their source-weight outline.
    if too_dense(glyph):
        continue
    amount = {change_amount}
    if glyph.glyphname in half:
        amount = amount // 2
    try:
        glyph.changeWeight(amount, "auto", 0, 0, "auto")
    except Exception:
        pass

font.os2_weight = {target_weight}
font.generate({output_path!r})
font.close()
"""
