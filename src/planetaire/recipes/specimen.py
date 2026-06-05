"""
Specimen PDF build recipe.

Compiles the Typst specimen source into a PDF, ensuring the font
directory is correctly passed so Typst can find the built fonts.
"""

from __future__ import annotations

import logging
import shutil
import subprocess
from pathlib import Path

log = logging.getLogger(__name__)

# Default paths relative to the repository root.
SPECIMEN_SOURCE = Path("docs/specimen/planetaire-mono-specimen.typ")
SPECIMEN_OUTPUT = Path("docs/specimen/planetaire-mono-specimen.pdf")
FONT_DIR = Path("fonts/output")


def build_specimen(
    source: Path = SPECIMEN_SOURCE,
    output: Path | None = None,
    font_dir: Path = FONT_DIR,
    *,
    version: str | None = None,
    open_after: bool = False,
) -> Path:
    """
    Compile the Typst specimen source to PDF.

    Args:
        source: Path to the .typ specimen source file.
        output: Output PDF path. Defaults to source with .pdf extension.
        font_dir: Directory containing built Planetaire Mono font files.
        version: Font version to stamp into the specimen. Defaults to the
            canonical package version so the specimen never disagrees with the
            built fonts.
        open_after: Open the PDF after compilation.

    Returns:
        Path to the generated PDF.

    Raises:
        FileNotFoundError: If typst is not installed or source file is missing.
        subprocess.CalledProcessError: If typst compilation fails.
    """
    if not source.exists():
        raise FileNotFoundError(f"Specimen source not found: {source}")

    if not font_dir.exists():
        raise FileNotFoundError(
            f"Font directory not found: {font_dir}. Run 'planetaire build planetaire-mono' first."
        )

    typst_bin = shutil.which("typst")
    if typst_bin is None:
        raise FileNotFoundError("typst not found. Install it: https://github.com/typst/typst")

    if output is None:
        output = source.with_suffix(".pdf")

    if version is None:
        from planetaire.version import get_version, to_font_version

        version = to_font_version(get_version())

    from datetime import date

    build_date = date.today().isoformat()

    output.parent.mkdir(parents=True, exist_ok=True)

    # Typst --font-path tells it where to find custom fonts; --input passes the
    # canonical version and build date into the document via sys.inputs.
    cmd = [
        typst_bin,
        "compile",
        "--font-path",
        str(font_dir.resolve()),
        "--input",
        f"version={version}",
        "--input",
        f"build-date={build_date}",
        str(source),
        str(output),
    ]

    log.info("Compiling specimen: %s", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode, cmd, output=result.stdout, stderr=result.stderr
        )

    log.info("Specimen PDF written to %s", output)

    if open_after:
        _open_pdf(output)

    return output


def render_png(
    source: Path,
    output: Path,
    font_dir: Path = FONT_DIR,
    *,
    ppi: int = 200,
    version: str | None = None,
) -> Path:
    """Render a Typst source to a PNG (e.g. the README hero image).

    Shares the font path and version injection with the PDF specimen so every
    rendered artifact comes from one Typst pipeline.
    """
    if not source.exists():
        raise FileNotFoundError(f"Typst source not found: {source}")
    if not font_dir.exists():
        raise FileNotFoundError(
            f"Font directory not found: {font_dir}. Run 'planetaire build planetaire-mono' first."
        )

    typst_bin = shutil.which("typst")
    if typst_bin is None:
        raise FileNotFoundError("typst not found. Install it: https://github.com/typst/typst")

    if version is None:
        from planetaire.version import get_version, to_font_version

        version = to_font_version(get_version())

    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        typst_bin,
        "compile",
        "--font-path",
        str(font_dir.resolve()),
        "--format",
        "png",
        "--ppi",
        str(ppi),
        "--input",
        f"version={version}",
        str(source),
        str(output),
    ]
    log.info("Rendering PNG: %s", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode, cmd, output=result.stdout, stderr=result.stderr
        )
    log.info("PNG written to %s", output)
    return output


def _open_pdf(path: Path) -> None:
    """Best-effort open a PDF with the system viewer."""
    import platform

    system = platform.system()
    try:
        if system == "Darwin":
            subprocess.Popen(["open", str(path)])
        elif system == "Linux":
            subprocess.Popen(["xdg-open", str(path)])
        elif system == "Windows":
            subprocess.Popen(["start", str(path)], shell=True)
    except OSError:
        log.warning("Could not open PDF automatically")
