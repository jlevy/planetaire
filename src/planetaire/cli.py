"""
Planetaire CLI: thin Typer wrapper around ops/ functions.

Data to stdout, progress/errors to stderr. Supports `--format text|json`
on inspection commands and `--no-progress` for CI.
"""

from __future__ import annotations

import sys
from enum import StrEnum
from pathlib import Path

import typer
from rich.console import Console


class OutputFormat(StrEnum):
    """Output format for inspection commands."""

    text = "text"
    json = "json"


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
    format: OutputFormat = typer.Option(OutputFormat.text, help="Output format: text or json"),
    features: bool = typer.Option(
        False, "--features", help="Show detailed GSUB feature/lookup info"
    ),
) -> None:
    """Inspect font metadata, glyph counts, and features."""
    from planetaire.ops.info import inspect_font

    path = _resolve_font_path(font)
    font_info = inspect_font(path, feature_details=features)

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
        if font_info.gsub_feature_details:
            err_console.print()
            err_console.print("[bold]GSUB Feature Details[/bold]")
            for feat in font_info.gsub_feature_details:
                err_console.print(f"  [cyan]{feat.tag}[/cyan]  lookups: {feat.lookup_indices}")
                for lk in feat.lookups:
                    err_console.print(
                        f"    [{lk.index}] {lk.lookup_type_name} ({lk.subtable_count} subtable(s))"
                    )
                    if lk.substitutions:
                        for src, dst in sorted(lk.substitutions.items())[:20]:
                            err_console.print(f"        {src} → {dst}")
                        if len(lk.substitutions) > 20:
                            err_console.print(f"        ... and {len(lk.substitutions) - 20} more")


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
    fonts: list[Path] = typer.Argument(..., help="Path(s) to font file(s)"),
    format: OutputFormat = typer.Option(OutputFormat.text, help="Output format: text or json"),
) -> None:
    """Check glyph coverage, metrics, and features for one or more fonts."""
    from dataclasses import asdict
    from typing import Any

    from fontTools.ttLib import TTFont

    from planetaire.ops.validate import validate_font

    results: dict[str, list[dict[str, Any]]] = {}
    total_errors = 0
    for font in fonts:
        path = _resolve_font_path(font)
        issues = validate_font(TTFont(path))
        results[str(font)] = [asdict(i) for i in issues]
        total_errors += sum(1 for i in issues if i.severity == "error")

    if format == "json":
        import json

        json.dump(results, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        for font, issues in results.items():
            if not issues:
                err_console.print(f"[green]{font}: no issues found.[/green]")
                continue
            err_console.print(f"[bold]{font}[/bold]")
            for issue in issues:
                severity = str(issue["severity"])
                style = {"error": "red", "warning": "yellow", "info": "blue"}[severity]
                err_console.print(f"  [{style}]{severity.upper()}[/{style}] {issue['message']}")

    if total_errors:
        raise ValidationError(f"{total_errors} validation error(s) found")


# -- compare command --


@app.command()
def compare(
    font_a: Path = typer.Argument(..., help="First font file"),
    font_b: Path = typer.Argument(..., help="Second font file"),
    ranges: str | None = typer.Option(None, help="Unicode ranges to compare (default: all shared)"),
    format: OutputFormat = typer.Option(OutputFormat.text, help="Output format: text or json"),
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
    output_dir: Path = typer.Option(Path("fonts/source"), help="Directory containing source fonts"),
) -> None:
    """Locate and integrity-check source fonts (verified against SHA256SUMS)."""
    from planetaire.recipes.sources import download_sources

    fonts = download_sources(output_dir)
    err_console.print(f"[green]Verified {len(fonts)} source font(s) in {output_dir}[/green]")


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


@build_app.command("text")
def build_text_cmd(
    source_dir: Path = typer.Option(Path("fonts/source"), help="Directory containing source fonts"),
    output_dir: Path = typer.Option(Path("fonts/output"), help="Directory for output fonts"),
) -> None:
    """Build the lightweight Planetaire Mono Text family (WOFF2/WOFF/TTF + CSS)."""
    from planetaire.recipes.planetaire_mono import build_text

    outputs = build_text(source_dir, output_dir)
    for p in outputs:
        err_console.print(f"  {p}")
    err_console.print(f"[green]Built {len(outputs)} file(s)[/green]")


@build_app.command("images")
def build_images_cmd(
    out_dir: Path = typer.Option(Path("docs/images"), help="Directory for README images"),
    font_dir: Path = typer.Option(Path("fonts/output"), help="Directory containing built fonts"),
    ppi: int = typer.Option(300, help="Render resolution (pixels per inch)"),
) -> None:
    """Render the README images from the specimen's shared content (in sync with the PDF).

    Each card is rendered as a matched dark/light pair (<card>-dark.png, <card>-light.png)
    so the README can switch with the GitHub color scheme.
    """
    import subprocess

    from planetaire.recipes.specimen import render_png

    card = Path("docs/specimen/card.typ")
    card_names = ("code", "terminal", "text", "weights", "features", "sample", "waterfall", "rfc")
    count = 0
    try:
        for card_name in card_names:
            for theme in ("dark", "light"):
                out = out_dir / f"{card_name}-{theme}.png"
                render_png(card, out, font_dir, ppi=ppi, inputs={"card": card_name, "theme": theme})
                err_console.print(f"  {out}")
                count += 1
        # White header banner for the top of the README (light/white only).
        header_out = out_dir / "header.png"
        render_png(card, header_out, font_dir, ppi=ppi, inputs={"card": "header", "theme": "light"})
        err_console.print(f"  {header_out}")
        count += 1
    except subprocess.CalledProcessError as e:
        err_console.print("[red]Typst render failed:[/red]")
        if e.stderr:
            err_console.print(e.stderr)
        raise SystemExit(1) from e
    err_console.print(f"[green]Rendered {count} README images to {out_dir}[/green]")


@build_app.command("html-specimen")
def build_html_specimen_cmd(
    output: Path = typer.Option(Path("fonts/output/specimen.html"), help="Output HTML path"),
    css_href: str = typer.Option(
        "planetaire-mono-text.css", help="Relative href to the @font-face stylesheet"
    ),
) -> None:
    """Generate a static HTML specimen that loads the Text web fonts."""
    from planetaire.recipes.html_specimen import generate_html_specimen

    path = generate_html_specimen(output, css_href=css_href)
    err_console.print(f"[green]HTML specimen written to {path}[/green]")


@build_app.command("site")
def build_site_cmd(
    output_dir: Path = typer.Option(Path("site"), help="Directory for the generated site"),
    fonts_dir: Path = typer.Option(
        Path("fonts/output"), help="Directory with built fonts, CSS, and specimen"
    ),
) -> None:
    """Assemble a static site (landing page + specimen + web fonts). No deploy."""
    from planetaire.recipes.site import generate_site

    index = generate_site(output_dir, fonts_dir)
    err_console.print(f"[green]Site written to {index.parent} (open {index})[/green]")


@build_app.command("specimen")
def build_specimen_cmd(
    source: Path = typer.Option(
        Path("docs/specimen/planetaire-mono-specimen.typ"),
        help="Typst source file for the specimen",
    ),
    output: Path | None = typer.Option(None, help="Output PDF path (default: same dir as source)"),
    font_dir: Path = typer.Option(Path("fonts/output"), help="Directory containing built fonts"),
    version: str | None = typer.Option(
        None,
        help="Version to stamp into the specimen (default: the canonical git-tag version). "
        "Pass explicitly at release time to stamp the tag-to-be before it exists.",
    ),
    open: bool = typer.Option(False, "--open", help="Open the PDF after compilation"),
) -> None:
    """Compile the font specimen PDF from Typst source."""
    import subprocess

    from planetaire.recipes.specimen import build_specimen

    try:
        pdf_path = build_specimen(source, output, font_dir, version=version, open_after=open)
    except subprocess.CalledProcessError as e:
        err_console.print("[red]Typst compilation failed:[/red]")
        if e.stderr:
            err_console.print(e.stderr)
        raise SystemExit(1) from e
    err_console.print(f"[green]Specimen PDF written to {pdf_path}[/green]")


# -- regression subcommands --

regression_app = typer.Typer(
    name="regression",
    help="Glyph regression detection: compare builds against a saved manifest.",
    no_args_is_help=True,
)
app.add_typer(regression_app, name="regression")

MANIFEST_PATH = Path("fonts/golden/manifest.json.gz")


@regression_app.command("generate")
def regression_generate(
    font_dir: Path = typer.Option(Path("fonts/output"), help="Built fonts directory"),
    output: Path = typer.Option(MANIFEST_PATH, help="Manifest output path"),
    version: str = typer.Option("dev", help="Version label"),
) -> None:
    """Generate a golden manifest from current build."""
    from planetaire.ops.regression import generate_manifest, save_manifest

    manifest = generate_manifest(font_dir, version=version)
    output.parent.mkdir(parents=True, exist_ok=True)
    save_manifest(manifest, output)

    total_glyphs = sum(len(vm.glyphs) for vm in manifest.variants)
    err_console.print(
        f"[green]Manifest saved:[/green] {len(manifest.variants)} variants, "
        f"{total_glyphs} glyphs total → {output}"
    )


@regression_app.command("verify")
def regression_verify(
    font_dir: Path = typer.Option(Path("fonts/output"), help="Built fonts directory"),
    manifest: Path = typer.Option(MANIFEST_PATH, help="Golden manifest to compare against"),
) -> None:
    """Compare current build against saved golden manifest."""
    from planetaire.ops.regression import (
        compare_manifests,
        format_report,
        generate_manifest,
        load_manifest,
    )

    if not manifest.exists():
        raise CLIError(f"No manifest found at {manifest}. Run 'regression generate' first.")

    old = load_manifest(manifest)
    new = generate_manifest(font_dir)
    reports = compare_manifests(old, new)
    print(format_report(reports))

    has_changes = any(r.changed > 0 or r.removed > 0 for r in reports)
    if has_changes:
        raise SystemExit(1)


def main() -> None:
    """Entry point: run the app, rendering CLIError cleanly instead of a traceback."""
    try:
        app()
    except CLIError as e:
        err_console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(e.exit_code) from e


if __name__ == "__main__":
    main()
