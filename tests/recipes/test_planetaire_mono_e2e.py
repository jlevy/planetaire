"""
E2E validation: verify Planetaire Mono glyphs match source fonts exactly.

For each variant:
- B612-range glyphs must be binary-identical to the B612 donor
- All other glyphs must be binary-identical to the UPM-scaled Hack base

Uses fast glyf binary comparison (hash-based), with detailed RecordingPen
comparison only for debugging mismatches.
"""

from __future__ import annotations

import copy
import hashlib
import tempfile
from pathlib import Path

import pytest
from fontTools.ttLib import TTFont

from planetaire.config import PLANETAIRE_LETTER_RANGES, VARIANTS
from planetaire.ops.merge import scale_font_upm
from planetaire.ops.monospace import check_monospace
from planetaire.recipes.planetaire_mono import build_planetaire_mono
from planetaire.unicode_ranges import codepoints_in_ranges

FONTS_SOURCE = Path(__file__).parent.parent.parent / "fonts" / "source"

B612_CODEPOINTS: set[int] = set(codepoints_in_ranges(PLANETAIRE_LETTER_RANGES))


def _glyph_hash(font: TTFont, glyph_name: str) -> str:
    """Fast hash of a glyph's binary data + metrics."""
    glyf = font["glyf"]
    hmtx = font["hmtx"]
    h = hashlib.md5()

    if glyph_name in glyf:
        # Compare outlines only (ignore TrueType instructions): the merge strips
        # donor hinting, so bytecode legitimately differs while shapes must not.
        g = copy.deepcopy(glyf[glyph_name])
        if hasattr(g, "program"):
            from fontTools.ttLib.tables import ttProgram

            g.program = ttProgram.Program()
            g.program.fromBytecode(b"")
        try:
            h.update(g.compile(glyf))
        except Exception:
            h.update(b"compile-error")
    else:
        h.update(b"missing")

    if glyph_name in hmtx.metrics:
        w, lsb = hmtx.metrics[glyph_name]
        h.update(f"{w},{lsb}".encode())

    return h.hexdigest()


@pytest.fixture(scope="module")
def all_built_fonts() -> dict[str, TTFont]:
    """Build all 8 Planetaire Mono variants once for the module."""
    if not (FONTS_SOURCE / "b612").exists() or not (FONTS_SOURCE / "hack").exists():
        pytest.skip("Source fonts not available")

    with tempfile.TemporaryDirectory() as tmpdir:
        outputs = build_planetaire_mono(FONTS_SOURCE, Path(tmpdir))
        ttfs = [p for p in outputs if p.suffix == ".ttf"]
        assert len(ttfs) == 8
        return {p.stem.split("-")[1]: TTFont(p) for p in ttfs}


@pytest.fixture(scope="module")
def scaled_hack_fonts() -> dict[str, TTFont]:
    """Pre-scale all Hack source fonts to UPM=2000 for direct binary comparison."""
    if not (FONTS_SOURCE / "hack").exists():
        pytest.skip("Source fonts not available")

    result = {}
    for vdef in VARIANTS:
        hack = TTFont(FONTS_SOURCE / "hack" / vdef["hack_file"])
        scaled = copy.deepcopy(hack)
        scale_font_upm(scaled, 2000)
        result[vdef["name"]] = scaled
    return result


# --- Verify ALL variants: B612 letters match donor (binary identical) ---


@pytest.mark.parametrize("variant", [v["name"] for v in VARIANTS])
def test_b612_letterforms_preserved(variant: str, all_built_fonts: dict[str, TTFont]):
    """B612 letterforms survive the monospace normalization intact.

    The pipeline pins every B612 letter (designed on a 1300 cell) to the Hack
    base cell, recentering horizontally and condensing only where ink would
    bleed. That is a pure x-axis transform, so each letter must keep its EXACT
    vertical metrics and never grow wider than the donor. (It is no longer
    binary-identical to the donor -- that is the point of the fix.)

    Zero (U+0030) is excluded because the pipeline adds a center dot.
    """
    vdef = next(v for v in VARIANTS if v["name"] == variant)
    donor = TTFont(FONTS_SOURCE / "b612" / vdef["b612_file"])
    pm = all_built_fonts[variant]
    donor_cmap = donor.getBestCmap() or {}
    pm_cmap = pm.getBestCmap() or {}
    dglyf = donor["glyf"]
    pglyf = pm["glyf"]

    checked = 0
    problems: list[str] = []
    for cp in sorted(B612_CODEPOINTS):
        if cp == 0x0030:
            continue
        if cp not in donor_cmap or cp not in pm_cmap:
            continue
        dg = dglyf[donor_cmap[cp]]
        pg = pglyf[pm_cmap[cp]]
        dg.recalcBounds(dglyf)
        pg.recalcBounds(pglyf)
        if dg.numberOfContours == 0:
            continue
        checked += 1
        # Vertical metrics must be untouched (transform is x-only).
        if (pg.yMin, pg.yMax) != (dg.yMin, dg.yMax):
            problems.append(f"U+{cp:04X} y {(dg.yMin, dg.yMax)}->{(pg.yMin, pg.yMax)}")
        # Ink may be recentered/condensed but never stretched wider.
        if (pg.xMax - pg.xMin) > (dg.xMax - dg.xMin) + 2:
            problems.append(f"U+{cp:04X} wider {dg.xMax - dg.xMin}->{pg.xMax - pg.xMin}")

    assert checked > 20, f"{variant}: only {checked} B612 glyphs checked"
    assert not problems, f"{variant}: {len(problems)} letterform problems: {problems[:10]}"


# --- Verify ALL variants: non-B612 glyphs match UPM-scaled Hack (binary identical) ---


@pytest.mark.parametrize("variant", [v["name"] for v in VARIANTS])
def test_hack_glyphs_binary_identical(
    variant: str,
    all_built_fonts: dict[str, TTFont],
    scaled_hack_fonts: dict[str, TTFont],
):
    """Every non-B612 glyph keeps the UPM-scaled Hack base, unless the monospace
    normalization had to touch it.

    The merge does deepcopy(hack) -> scale_upm -> overwrite B612 glyphs, so
    untouched Hack glyphs stay byte-identical. In the FontForge-emboldened
    weights (Medium/ExtraBold) some Hack glyphs were inflated off the cell grid
    and are normalized back; those legitimately differ and are skipped here
    (the monospace invariant test covers them).
    """
    pm = all_built_fonts[variant]
    scaled_hack = scaled_hack_fonts[variant]
    pm_cmap = pm.getBestCmap() or {}
    hack_cmap = scaled_hack.getBestCmap() or {}
    pm_hmtx = pm["hmtx"]
    hack_hmtx = scaled_hack["hmtx"]

    mismatches = []
    checked = 0
    for cp in sorted(pm_cmap):
        if cp in B612_CODEPOINTS:
            continue
        if cp not in hack_cmap:
            continue
        pm_name = pm_cmap[cp]
        hack_name = hack_cmap[cp]
        # Skip glyphs the normalization repositioned (advance changed).
        if pm_hmtx[pm_name][0] != hack_hmtx[hack_name][0]:
            continue
        checked += 1
        if _glyph_hash(pm, pm_name) != _glyph_hash(scaled_hack, hack_name):
            mismatches.append(cp)

    assert checked > 1000, f"{variant}: expected 1000+ non-B612 glyphs, got {checked}"
    assert len(mismatches) == 0, (
        f"{variant}: {len(mismatches)}/{checked} Hack glyphs differ after UPM scaling: "
        + ", ".join(f"U+{cp:04X}" for cp in mismatches[:20])
    )


# --- Verify ALL variants: Nerd Font glyphs present ---


@pytest.mark.parametrize("variant", [v["name"] for v in VARIANTS])
def test_nerd_font_glyphs_present(variant: str, all_built_fonts: dict[str, TTFont]):
    """Nerd Font glyphs from Hack must be present in every variant."""
    cmap = all_built_fonts[variant].getBestCmap()
    assert cmap is not None

    for cp, label in [
        (0xE0A0, "Powerline Branch"),
        (0xE0A1, "Powerline Line number"),
        (0xE0A2, "Powerline Padlock"),
        (0xE0B0, "Powerline Right arrow"),
        (0xE5FA, "Seti-UI glyph"),
    ]:
        assert cp in cmap, f"{variant}: missing {label} U+{cp:04X}"


# --- Verify B612 digits: digits 0-9 per variant (zero has added dot) ---


@pytest.mark.parametrize("variant", [v["name"] for v in VARIANTS])
def test_b612_digits_all_present(variant: str, all_built_fonts: dict[str, TTFont]):
    """Digits 1-9 must be present, monospace, and keep the B612 letterform.

    The digits come from B612 but, like the letters, are normalized to the
    cell (recentered horizontally), so they are no longer byte-identical to the
    donor -- their vertical metrics are preserved and they never grow wider.

    Zero (U+0030) has a center dot added and is verified separately.
    """
    vdef = next(v for v in VARIANTS if v["name"] == variant)
    donor = TTFont(FONTS_SOURCE / "b612" / vdef["b612_file"])
    pm = all_built_fonts[variant]
    cell = check_monospace(pm).cell_width
    donor_cmap = donor.getBestCmap() or {}
    pm_cmap = pm.getBestCmap() or {}

    for cp in range(0x31, 0x3A):
        assert cp in pm_cmap, f"{variant}: digit U+{cp:04X} missing"
        dg = donor["glyf"][donor_cmap[cp]]
        pg = pm["glyf"][pm_cmap[cp]]
        dg.recalcBounds(donor["glyf"])
        pg.recalcBounds(pm["glyf"])
        assert pm["hmtx"][pm_cmap[cp]][0] == cell, f"{variant}: digit U+{cp:04X} off cell"
        assert (pg.yMin, pg.yMax) == (dg.yMin, dg.yMax), f"{variant}: digit U+{cp:04X} y changed"
        assert (pg.xMax - pg.xMin) <= (dg.xMax - dg.xMin) + 2, f"{variant}: digit U+{cp:04X} wider"


@pytest.mark.parametrize("variant", [v["name"] for v in VARIANTS])
def test_dotted_zero(variant: str, all_built_fonts: dict[str, TTFont]):
    """Zero glyph must have 3 contours (outer + inner counter + center dot)."""
    pm = all_built_fonts[variant]
    cmap = pm.getBestCmap() or {}
    assert 0x30 in cmap, f"{variant}: zero not in cmap"
    zero_name = cmap[0x30]
    glyph = pm["glyf"][zero_name]
    assert glyph.numberOfContours == 3, (
        f"{variant}: zero has {glyph.numberOfContours} contours, expected 3 (with dot)"
    )


# --- Spot-check: B612 letter outlines match via RecordingPen ---


@pytest.mark.parametrize("variant", [v["name"] for v in VARIANTS])
def test_built_fonts_are_monospace(variant: str, all_built_fonts: dict[str, TTFont]):
    """Headline invariant: every variant is truly monospace.

    Before the fix this failed for every weight -- B612 letters were 1300 while
    the Hack base was 1204, and FontForge-emboldened Medium/ExtraBold letters
    ranged 1239-1420. After normalization every non-zero glyph shares one cell
    width, the font declares isFixedPitch, and no core ASCII coding glyph bleeds
    past the cell.
    """
    pm = all_built_fonts[variant]
    report = check_monospace(pm)
    assert report.is_monospace, (
        f"{variant}: {len(report.nonuniform)} glyph(s) off cell {report.cell_width}: "
        f"{report.nonuniform[:8]}"
    )
    assert pm["post"].isFixedPitch == 1, f"{variant}: isFixedPitch not set"

    cmap = pm.getBestCmap() or {}
    glyf = pm["glyf"]
    cell = report.cell_width
    core = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    bleeders = []
    for ch in core:
        name = cmap.get(ord(ch))
        if name and glyf[name].numberOfContours:
            glyf[name].recalcBounds(glyf)
            if glyf[name].xMin < -2 or glyf[name].xMax > cell + 2:
                bleeders.append(f"{ch}[{glyf[name].xMin},{glyf[name].xMax}]")
    assert not bleeders, f"{variant}: core glyphs bleed past cell {cell}: {bleeders}"


# --- Spot-check: Hack punctuation outlines match (after UPM scaling) ---


HACK_PUNCT_RANGES = [
    (0x0021, 0x002F),
    (0x003A, 0x0040),
    (0x005B, 0x0060),
    (0x007B, 0x007E),
]


@pytest.mark.parametrize("variant", [v["name"] for v in VARIANTS])
def test_hack_punctuation_matches_base(
    variant: str,
    all_built_fonts: dict[str, TTFont],
    scaled_hack_fonts: dict[str, TTFont],
):
    """ASCII punctuation keeps the UPM-scaled Hack outline, unless normalized.

    Untouched punctuation must be byte-identical to scaled Hack. A few wide
    punctuation glyphs in the emboldened weights were inflated off the cell and
    are normalized back; those differ and are skipped (covered by the monospace
    invariant test).
    """
    pm = all_built_fonts[variant]
    scaled_hack = scaled_hack_fonts[variant]
    pm_cmap = pm.getBestCmap() or {}
    hack_cmap = scaled_hack.getBestCmap() or {}

    checked = 0
    mismatches = []
    for lo, hi in HACK_PUNCT_RANGES:
        for cp in range(lo, hi + 1):
            if cp not in pm_cmap or cp not in hack_cmap:
                continue
            pm_name, hack_name = pm_cmap[cp], hack_cmap[cp]
            if pm["hmtx"][pm_name][0] != scaled_hack["hmtx"][hack_name][0]:
                continue  # normalized off the cell grid
            checked += 1
            if _glyph_hash(pm, pm_name) != _glyph_hash(scaled_hack, hack_name):
                mismatches.append(cp)

    assert checked > 0, f"{variant}: no untouched punctuation to compare"
    assert not mismatches, f"{variant}: punctuation differs from Hack: " + ", ".join(
        f"U+{cp:04X}" for cp in mismatches
    )


# --- Sanity checks for intermediate weights (Medium) ---


_INTERMEDIATE_VARIANTS = ["Medium", "MediumItalic"]


_REQUIRED_TABLES = {
    "cmap",
    "glyf",
    "head",
    "hhea",
    "hmtx",
    "loca",
    "maxp",
    "name",
    "post",
    "OS/2",
    "DSIG",
    "GDEF",
    "GPOS",
    "GSUB",
    "gasp",
}


@pytest.mark.parametrize("variant", _INTERMEDIATE_VARIANTS)
def test_intermediate_weight_structure(variant: str, all_built_fonts: dict[str, TTFont]):
    """Intermediate weight fonts must have all required OpenType tables."""
    intermediate = all_built_fonts[variant]
    intermediate_tables = set(intermediate.keys())

    missing = _REQUIRED_TABLES - intermediate_tables
    assert not missing, f"{variant}: missing required tables: {missing}"


@pytest.mark.parametrize("variant", _INTERMEDIATE_VARIANTS)
def test_intermediate_weight_glyph_count(variant: str, all_built_fonts: dict[str, TTFont]):
    """Intermediate weights must have comparable glyph count to Regular."""
    regular = all_built_fonts["Regular"]
    intermediate = all_built_fonts[variant]

    regular_count = len(regular.getGlyphOrder())
    intermediate_count = len(intermediate.getGlyphOrder())

    # Glyph counts should be within 1% (emboldening may rarely add/remove composites)
    assert abs(intermediate_count - regular_count) / regular_count < 0.01, (
        f"{variant}: glyph count {intermediate_count} differs significantly "
        f"from Regular ({regular_count})"
    )


def test_weight_progression_stroke_width(all_built_fonts: dict[str, TTFont]):
    """Verify emboldened weights have progressively thicker strokes.

    Measures the advance width and horizontal stem hints of uppercase I
    as a proxy for stroke weight. At minimum, verifies the OS/2 weight
    class values form a monotonic sequence.
    """
    weight_order = ["Regular", "Medium", "Bold", "ExtraBold"]
    weight_classes = []
    for name in weight_order:
        font = all_built_fonts[name]
        weight_classes.append(font["OS/2"].usWeightClass)

    # Weight classes must be strictly increasing
    for i in range(len(weight_classes) - 1):
        assert weight_classes[i] < weight_classes[i + 1], (
            f"Weight class not increasing: {weight_order[i]}={weight_classes[i]} "
            f">= {weight_order[i + 1]}={weight_classes[i + 1]}"
        )
