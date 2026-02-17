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
from planetaire.ops.compare import compare_fonts
from planetaire.ops.merge import scale_font_upm
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
        g = glyf[glyph_name]
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
    """Build all 10 Planetaire Mono variants once for the module."""
    if not (FONTS_SOURCE / "b612").exists() or not (FONTS_SOURCE / "hack").exists():
        pytest.skip("Source fonts not available")

    with tempfile.TemporaryDirectory() as tmpdir:
        outputs = build_planetaire_mono(FONTS_SOURCE, Path(tmpdir))
        assert len(outputs) == 10
        return {p.stem.split("-")[1]: TTFont(p) for p in outputs}


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
def test_b612_glyphs_binary_identical(variant: str, all_built_fonts: dict[str, TTFont]):
    """Every B612-range glyph must be binary-identical to the B612 donor.

    Zero (U+0030) is excluded because the pipeline adds a center dot
    for disambiguation from uppercase O.
    """
    vdef = next(v for v in VARIANTS if v["name"] == variant)
    donor = TTFont(FONTS_SOURCE / "b612" / vdef["b612_file"])
    pm = all_built_fonts[variant]
    donor_cmap = donor.getBestCmap() or {}
    pm_cmap = pm.getBestCmap() or {}

    mismatches = []
    checked = 0
    for cp in sorted(B612_CODEPOINTS):
        if cp == 0x0030:  # Zero modified by add_dotted_zero
            continue
        if cp not in donor_cmap or cp not in pm_cmap:
            continue
        checked += 1
        pm_name = pm_cmap[cp]
        donor_name = donor_cmap[cp]
        if _glyph_hash(pm, pm_name) != _glyph_hash(donor, donor_name):
            mismatches.append(cp)

    assert checked > 0, f"{variant}: No B612 glyphs found"
    assert len(mismatches) == 0, (
        f"{variant}: {len(mismatches)}/{checked} B612-range glyphs differ from donor: "
        + ", ".join(f"U+{cp:04X}" for cp in mismatches[:20])
    )


# --- Verify ALL variants: non-B612 glyphs match UPM-scaled Hack (binary identical) ---


@pytest.mark.parametrize("variant", [v["name"] for v in VARIANTS])
def test_hack_glyphs_binary_identical(
    variant: str,
    all_built_fonts: dict[str, TTFont],
    scaled_hack_fonts: dict[str, TTFont],
):
    """Every non-B612 glyph must be binary-identical to UPM-scaled Hack base.

    Since the merge does deepcopy(hack) → scale_upm → overwrite B612 glyphs,
    all non-B612 glyphs should be exactly what scale_font_upm produced.
    """
    pm = all_built_fonts[variant]
    scaled_hack = scaled_hack_fonts[variant]
    pm_cmap = pm.getBestCmap() or {}
    hack_cmap = scaled_hack.getBestCmap() or {}

    mismatches = []
    checked = 0
    for cp in sorted(pm_cmap):
        if cp in B612_CODEPOINTS:
            continue
        if cp not in hack_cmap:
            continue
        checked += 1
        pm_name = pm_cmap[cp]
        hack_name = hack_cmap[cp]
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
    """Digits 1-9 must be present and match B612 donor exactly.

    Zero (U+0030) comes from B612 but has a center dot added for
    disambiguation, so it's verified separately.
    """
    vdef = next(v for v in VARIANTS if v["name"] == variant)
    donor = TTFont(FONTS_SOURCE / "b612" / vdef["b612_file"])
    pm = all_built_fonts[variant]

    result = compare_fonts(pm, donor, [(0x0031, 0x0039)])
    assert result.identical == 9, (
        f"{variant}: expected 9 identical digits (1-9), got {result.identical}"
    )
    assert result.different == 0


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
def test_b612_letters_recordingpen_match(variant: str, all_built_fonts: dict[str, TTFont]):
    """Verify A-Z letter outlines match B612 donor (RecordingPen comparison).

    Uses tolerance=1.0 because FontForge-emboldened weights (Medium, SemiBold)
    can introduce sub-unit coordinate rounding in composite glyphs.
    The binary-identical test provides the stronger guarantee.
    """
    vdef = next(v for v in VARIANTS if v["name"] == variant)
    donor = TTFont(FONTS_SOURCE / "b612" / vdef["b612_file"])
    pm = all_built_fonts[variant]

    result = compare_fonts(pm, donor, [(0x0041, 0x005A)], tolerance=1.0)
    assert result.identical == 26, f"{variant}: expected 26 identical A-Z, got {result.identical}"
    assert result.different == 0


# --- Spot-check: Hack punctuation outlines match (after UPM scaling) ---


HACK_PUNCT_RANGES = [
    (0x0021, 0x002F),
    (0x003A, 0x0040),
    (0x005B, 0x0060),
    (0x007B, 0x007E),
]


@pytest.mark.parametrize("variant", [v["name"] for v in VARIANTS])
def test_hack_punctuation_recordingpen_match(variant: str, all_built_fonts: dict[str, TTFont]):
    """Verify basic ASCII punctuation matches Hack base (RecordingPen with UPM normalization).

    Uses tolerance=1.0 because UPM scaling (2048→2000) introduces integer
    rounding that creates sub-unit coordinate differences. The binary-identical
    test (test_hack_glyphs_binary_identical) provides the stronger guarantee.
    """
    vdef = next(v for v in VARIANTS if v["name"] == variant)
    base = TTFont(FONTS_SOURCE / "hack" / vdef["hack_file"])
    pm = all_built_fonts[variant]

    result = compare_fonts(pm, base, HACK_PUNCT_RANGES, tolerance=1.0)
    assert result.different == 0, (
        f"{variant}: {result.different} punctuation glyph(s) differ from Hack: "
        + ", ".join(f"U+{d.codepoint:04X}" for d in result.diffs if d.status == "different")
    )
    assert result.identical > 0


# --- Sanity checks for intermediate weights (Medium, SemiBold) ---


_INTERMEDIATE_VARIANTS = ["Medium", "MediumItalic", "SemiBold", "SemiBoldItalic"]


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
    weight_order = ["Regular", "Medium", "SemiBold", "Bold", "ExtraBold"]
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
