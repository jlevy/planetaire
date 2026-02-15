"""
Planetaire CLI — thin Typer wrapper around ops/ functions.

Data to stdout, progress/errors to stderr. Supports `--format text|json`
on inspection commands and `--no-progress` for CI.
"""

from __future__ import annotations

import sys
from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(
    name="planetaire",
    help="Planetaire Mono font build toolkit.",
    no_args_is_help=True,
    pretty_exceptions_enable=False,
)

build_app = typer.Typer(
    name="build",
    help="Planetaire-specific build recipes.",
    no_args_is_help=True,
)
app.add_typer(build_app, name="build")

err_console = Console(stderr=True)


class CLIError(Exception):
    """Base CLI error with exit code."""

    exit_code: int

    def __init__(self, message: str, exit_code: int = 1):
        super().__init__(message)
        self.exit_code = exit_code


class ValidationError(CLIError):
    """Validation failure (exit code 2)."""

    def __init__(self, message: str):
        super().__init__(message, exit_code=2)


def _resolve_font_path(path: Path) -> Path:
    """Resolve and validate a font file path."""
    resolved = path.resolve()
    if not resolved.exists():
        raise CLIError(f"Font file not found: {path}")
    if not resolved.is_file():
        raise CLIError(f"Not a file: {path}")
    return resolved


# -- info command --


@app.command()
def info(
    font: Path = typer.Argument(..., help="Path to a font file (.ttf/.otf)"),
    format: str = typer.Option("text", help="Output format: text or json"),
) -> None:
    """Inspect font metadata, glyph counts, and features."""
    from planetaire.ops.info import inspect_font

    path = _resolve_font_path(font)
    font_info = inspect_font(path)

    if format == "json":
        import json
        from dataclasses import asdict

        json.dump(asdict(font_info), sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        err_console.print(f"[bold]{font_info.full_name}[/bold]")
        err_console.print(f"  Family:      {font_info.family}")
        err_console.print(f"  Subfamily:   {font_info.subfamily}")
        err_console.print(f"  PostScript:  {font_info.postscript_name}")
        err_console.print(f"  Version:     {font_info.version}")
        err_console.print(f"  Glyphs:      {font_info.glyph_count}")
        err_console.print(f"  UPM:         {font_info.upm}")
        err_console.print(f"  Weight:      {font_info.weight_class}")
        err_console.print(f"  Italic:      {font_info.is_italic}")
        if font_info.gsub_features:
            err_console.print(f"  GSUB:        {', '.join(font_info.gsub_features)}")


# -- merge command --


@app.command()
def merge(
    base: Path = typer.Option(..., help="Base font file (keeps non-overlapping glyphs)"),
    donor: Path = typer.Option(..., help="Donor font file (provides glyphs for ranges)"),
    ranges: str = typer.Option(..., help="Unicode ranges, e.g. 'U+0041-005A,U+0061-007A'"),
    output: Path = typer.Option(..., help="Output font path"),
) -> None:
    """Copy glyphs from donor font into base font by unicode range."""
    from fontTools.ttLib import TTFont
    from strif import atomic_output_file

    from planetaire.ops.merge import merge_glyphs
    from planetaire.unicode_ranges import parse_unicode_ranges

    base_path = _resolve_font_path(base)
    donor_path = _resolve_font_path(donor)
    parsed = parse_unicode_ranges(ranges)

    base_font = TTFont(base_path)
    donor_font = TTFont(donor_path)
    result = merge_glyphs(base_font, donor_font, parsed)

    with atomic_output_file(str(output)) as tmp:
        result.save(tmp)

    err_console.print(f"Merged font written to {output}")


# -- rename command --


@app.command()
def rename(
    font: Path = typer.Argument(..., help="Path to a font file"),
    family: str = typer.Option(..., help="New font family name"),
    output: Path = typer.Option(..., help="Output font path"),
    subfamily: str | None = typer.Option(None, help="Subfamily (e.g. Bold, Italic)"),
    weight: int | None = typer.Option(None, help="OS/2 weight class (e.g. 400, 700)"),
) -> None:
    """Update font family name and metadata."""
    from fontTools.ttLib import TTFont
    from strif import atomic_output_file

    from planetaire.ops.rename import rename_font

    path = _resolve_font_path(font)
    tt_font = TTFont(path)
    result = rename_font(tt_font, family=family, subfamily=subfamily, weight=weight)

    with atomic_output_file(str(output)) as tmp:
        result.save(tmp)

    err_console.print(f"Renamed font written to {output}")


# -- fix command --


@app.command()
def fix(
    font: Path = typer.Argument(..., help="Path to a font file"),
    output: Path = typer.Option(..., help="Output font path"),
) -> None:
    """Apply post-processing fixes (DSIG, fsType, GASP)."""
    from fontTools.ttLib import TTFont
    from strif import atomic_output_file

    from planetaire.ops.fix import fix_font

    path = _resolve_font_path(font)
    tt_font = TTFont(path)
    result = fix_font(tt_font)

    with atomic_output_file(str(output)) as tmp:
        result.save(tmp)

    err_console.print(f"Fixed font written to {output}")


# -- validate command --


@app.command()
def validate(
    font: Path = typer.Argument(..., help="Path to a font file"),
    format: str = typer.Option("text", help="Output format: text or json"),
) -> None:
    """Check glyph coverage, metrics, and features."""
    from fontTools.ttLib import TTFont

    from planetaire.ops.validate import validate_font

    path = _resolve_font_path(font)
    tt_font = TTFont(path)
    issues = validate_font(tt_font)

    if format == "json":
        import json
        from dataclasses import asdict

        json.dump([asdict(i) for i in issues], sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        if not issues:
            err_console.print("[green]No issues found.[/green]")
        else:
            for issue in issues:
                style = {"error": "red", "warning": "yellow", "info": "blue"}[issue.severity]
                err_console.print(f"[{style}]{issue.severity.upper()}[/{style}] {issue.message}")
            errors = sum(1 for i in issues if i.severity == "error")
            if errors:
                raise SystemExit(2)


# -- compare command --


@app.command()
def compare(
    font_a: Path = typer.Argument(..., help="First font file"),
    font_b: Path = typer.Argument(..., help="Second font file"),
    ranges: str | None = typer.Option(None, help="Unicode ranges to compare (default: all shared)"),
    format: str = typer.Option("text", help="Output format: text or json"),
    strict: bool = typer.Option(False, help="Exit with error if any differences found"),
) -> None:
    """Compare glyph outlines between two fonts."""
    from fontTools.ttLib import TTFont

    from planetaire.ops.compare import compare_fonts
    from planetaire.unicode_ranges import parse_unicode_ranges

    path_a = _resolve_font_path(font_a)
    path_b = _resolve_font_path(font_b)
    parsed_ranges = parse_unicode_ranges(ranges) if ranges else None

    fa = TTFont(path_a)
    fb = TTFont(path_b)
    result = compare_fonts(fa, fb, parsed_ranges)

    if format == "json":
        import json
        from dataclasses import asdict

        json.dump(asdict(result), sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        err_console.print(
            f"Identical: {result.identical}  Different: {result.different}  "
            f"Missing A: {result.missing_a}  Missing B: {result.missing_b}"
        )
        for diff in result.diffs:
            err_console.print(f"  U+{diff.codepoint:04X} {diff.status}: {diff.diff_details or ''}")

    if strict and (result.different > 0 or result.missing_a > 0 or result.missing_b > 0):
        raise SystemExit(2)


# -- embolden command --


@app.command()
def embolden(
    font: Path = typer.Argument(..., help="Path to a font file"),
    output: Path = typer.Option(..., help="Output font path"),
    weight: int = typer.Option(800, help="Target OS/2 weight class"),
    change: int = typer.Option(30, help="FontForge changeWeight amount"),
) -> None:
    """Generate heavier weight variant (requires FontForge)."""
    from planetaire.ops.embolden import embolden_font

    path = _resolve_font_path(font)
    embolden_font(path, output, target_weight=weight, change_amount=change)
    err_console.print(f"Emboldened font written to {output}")


# -- build subcommands --


@build_app.command("download")
def build_download(
    output_dir: Path = typer.Option(
        Path("fonts/source"), help="Directory to download source fonts into"
    ),
) -> None:
    """Fetch source fonts from upstream repositories."""
    from planetaire.recipes.sources import download_sources

    download_sources(output_dir)
    err_console.print(f"Source fonts downloaded to {output_dir}")


@build_app.command("planetaire-mono")
def build_planetaire_mono(
    source_dir: Path = typer.Option(Path("fonts/source"), help="Directory containing source fonts"),
    output_dir: Path = typer.Option(Path("fonts/output"), help="Directory for output fonts"),
) -> None:
    """Run the full Planetaire Mono build pipeline."""
    from planetaire.recipes.planetaire_mono import build_planetaire_mono

    outputs = build_planetaire_mono(source_dir, output_dir)
    for p in outputs:
        err_console.print(f"  {p}")
    err_console.print(f"[green]Built {len(outputs)} font(s)[/green]")
