"""
Generate and verify glyph manifests for regression detection.

A manifest captures the hash of every glyph in the built fonts. When the
pipeline changes, comparing the new manifest against the saved one shows
exactly which glyphs changed, categorized as:

- Identical: no change
- Trivial: outline identical, only metrics (advance width / side bearing) changed
- Changed: outline shape differs (requires visual review)
- Added/Removed: glyph count changed

Usage:
    # Generate a new manifest after building fonts
    planetaire regression generate

    # Compare current build against saved manifest
    planetaire regression verify

    # Show detailed report
    planetaire regression report
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from fontTools.ttLib import TTFont


@dataclass
class GlyphEntry:
    """Manifest entry for a single glyph."""

    codepoint: int
    name: str
    glyf_hash: str
    advance_width: int
    lsb: int


@dataclass
class VariantManifest:
    """Manifest for a single font variant."""

    variant: str
    filename: str
    glyph_count: int
    upm: int
    weight: int
    glyphs: list[GlyphEntry] = field(default_factory=list)


@dataclass
class FontManifest:
    """Complete manifest for all Planetaire Mono variants."""

    version: str
    variants: list[VariantManifest] = field(default_factory=list)


@dataclass
class GlyphDiffReport:
    """Report of differences between two manifests."""

    variant: str
    identical: int = 0
    trivial: int = 0  # outline identical, only metrics (advance/lsb) changed
    changed: int = 0  # outline shape differs
    added: int = 0
    removed: int = 0
    changed_glyphs: list[str] = field(default_factory=list)


def _glyph_hash(font: TTFont, glyph_name: str) -> str:
    """Hash a glyph's binary data."""
    glyf = font["glyf"]
    h = hashlib.sha256()
    if glyph_name in glyf:
        g = glyf[glyph_name]
        try:
            h.update(g.compile(glyf))
        except Exception:
            h.update(b"compile-error")
    else:
        h.update(b"missing")
    return h.hexdigest()[:16]


def generate_manifest(font_dir: Path, version: str = "dev") -> FontManifest:
    """Generate a manifest from built font files."""
    manifest = FontManifest(version=version)

    for ttf_path in sorted(font_dir.glob("PlanetaireMonoExtended-*.ttf")):
        font = TTFont(ttf_path)
        variant = ttf_path.stem.split("-")[1]

        vm = VariantManifest(
            variant=variant,
            filename=ttf_path.name,
            glyph_count=len(font.getGlyphOrder()),
            upm=font["head"].unitsPerEm,
            weight=font["OS/2"].usWeightClass,
        )

        cmap = font.getBestCmap() or {}
        hmtx = font["hmtx"]

        for cp in sorted(cmap.keys()):
            glyph_name = cmap[cp]
            width, lsb = hmtx.metrics.get(glyph_name, (0, 0))
            vm.glyphs.append(
                GlyphEntry(
                    codepoint=cp,
                    name=glyph_name,
                    glyf_hash=_glyph_hash(font, glyph_name),
                    advance_width=width,
                    lsb=lsb,
                )
            )

        manifest.variants.append(vm)

    return manifest


def save_manifest(manifest: FontManifest, path: Path) -> None:
    """Save manifest to JSON.

    If `path` ends in ``.gz`` the JSON is written compactly and gzip-compressed,
    which shrinks the per-glyph manifest by ~20x (the committed form).
    """
    data = {
        "version": manifest.version,
        "variants": [
            {
                "variant": vm.variant,
                "filename": vm.filename,
                "glyph_count": vm.glyph_count,
                "upm": vm.upm,
                "weight": vm.weight,
                "glyphs": [asdict(g) for g in vm.glyphs],
            }
            for vm in manifest.variants
        ],
    }
    if path.suffix == ".gz":
        import gzip

        payload = json.dumps(data, separators=(",", ":")).encode()
        path.write_bytes(gzip.compress(payload, compresslevel=9))
    else:
        path.write_text(json.dumps(data, indent=2) + "\n")


def load_manifest(path: Path) -> FontManifest:
    """Load manifest from JSON (transparently handling gzip-compressed ``.gz``)."""
    if path.suffix == ".gz":
        import gzip

        data = json.loads(gzip.decompress(path.read_bytes()).decode())
    else:
        data = json.loads(path.read_text())
    manifest = FontManifest(version=data["version"])
    for vdata in data["variants"]:
        vm = VariantManifest(
            variant=vdata["variant"],
            filename=vdata["filename"],
            glyph_count=vdata["glyph_count"],
            upm=vdata["upm"],
            weight=vdata["weight"],
            glyphs=[GlyphEntry(**g) for g in vdata["glyphs"]],
        )
        manifest.variants.append(vm)
    return manifest


def compare_manifests(old: FontManifest, new: FontManifest) -> list[GlyphDiffReport]:
    """Compare two manifests and produce a diff report per variant."""
    reports = []

    old_variants = {vm.variant: vm for vm in old.variants}
    new_variants = {vm.variant: vm for vm in new.variants}

    for variant in sorted(set(old_variants) | set(new_variants)):
        report = GlyphDiffReport(variant=variant)

        if variant not in old_variants:
            new_vm = new_variants[variant]
            report.added = len(new_vm.glyphs)
            reports.append(report)
            continue

        if variant not in new_variants:
            old_vm = old_variants[variant]
            report.removed = len(old_vm.glyphs)
            reports.append(report)
            continue

        old_vm = old_variants[variant]
        new_vm = new_variants[variant]

        old_glyphs = {g.codepoint: g for g in old_vm.glyphs}
        new_glyphs = {g.codepoint: g for g in new_vm.glyphs}

        all_cps = sorted(set(old_glyphs) | set(new_glyphs))
        for cp in all_cps:
            if cp not in old_glyphs:
                report.added += 1
                continue
            if cp not in new_glyphs:
                report.removed += 1
                report.changed_glyphs.append(f"U+{cp:04X} (removed)")
                continue

            old_g = old_glyphs[cp]
            new_g = new_glyphs[cp]

            if old_g.glyf_hash == new_g.glyf_hash:
                if old_g.advance_width == new_g.advance_width and old_g.lsb == new_g.lsb:
                    report.identical += 1
                else:
                    # Outline identical, only metrics (advance/lsb) changed.
                    report.trivial += 1
            else:
                # Hash differs: the outline shape changed and needs review.
                # Equal advance width does NOT imply a similar shape, so any
                # hash difference is a real change, not a trivial one.
                report.changed += 1
                report.changed_glyphs.append(f"U+{cp:04X} ({new_g.name})")

        reports.append(report)

    return reports


def format_report(reports: list[GlyphDiffReport]) -> str:
    """Format a comparison report as human-readable text."""
    lines = ["Glyph Regression Report", "=" * 60, ""]

    total_identical = 0
    total_trivial = 0
    total_changed = 0
    total_added = 0
    total_removed = 0

    for r in reports:
        total = r.identical + r.trivial + r.changed + r.added + r.removed
        lines.append(f"{r.variant}:")
        lines.append(f"  Identical:  {r.identical:>6} / {total}")
        if r.trivial:
            lines.append(f"  Trivial:    {r.trivial:>6}  (rounding/metrics only)")
        if r.changed:
            lines.append(f"  Changed:    {r.changed:>6}  *** REQUIRES REVIEW ***")
        if r.added:
            lines.append(f"  Added:      {r.added:>6}")
        if r.removed:
            lines.append(f"  Removed:    {r.removed:>6}")
        if r.changed_glyphs:
            lines.append(f"  Changed glyphs: {', '.join(r.changed_glyphs[:20])}")
            if len(r.changed_glyphs) > 20:
                lines.append(f"  ... and {len(r.changed_glyphs) - 20} more")
        lines.append("")

        total_identical += r.identical
        total_trivial += r.trivial
        total_changed += r.changed
        total_added += r.added
        total_removed += r.removed

    lines.append("-" * 60)
    lines.append(
        f"Total: {total_identical} identical, {total_trivial} trivial, "
        f"{total_changed} changed, {total_added} added, {total_removed} removed"
    )

    if total_changed == 0 and total_removed == 0:
        lines.append("\nResult: PASS, no substantive regressions detected")
    else:
        lines.append(f"\nResult: REVIEW NEEDED: {total_changed} changed, {total_removed} removed")

    return "\n".join(lines)
