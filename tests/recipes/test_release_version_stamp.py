"""The release build and a rebuild at the resulting tag must agree, byte for byte.

A release builds the committed web fonts before `scripts/release.py finalize` creates
its tag, so it stamps the version explicitly; CI rebuilds at the tagged commit, where
the version resolves from the tag. Those are two different code paths to the same
bytes, and when they disagreed the committed `fonts/web/` lagged a release behind and
CI's rebuild gate failed (plt-0204). This pins them together.

The two builds are shared by both tests: each one processes all ten faces, so this
module is the expensive part of the suite it is worth keeping to two.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from fontTools.ttLib import TTFont

from planetaire.config import text_web_font_file_names
from planetaire.recipes.planetaire_mono import build_text
from planetaire.version import get_version, to_font_revision

FONTS_SOURCE = Path(__file__).parent.parent.parent / "fonts" / "source"

# Deliberately not any version this repo has tagged, so a stamp that leaked from the
# resolved version instead of the requested one cannot pass by coincidence.
RELEASE_VERSION = "9.9.9"


@pytest.fixture(scope="module")
def builds(tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, Path]:
    """Build the published web fonts both ways: told the version, and resolving it.

    `release` is the prepare-time build: the tag does not exist, so the version is
    passed in. `rebuild` is what CI (and `release.py finalize`) run afterwards: the tag
    exists, so the version resolves from it.
    """
    if not (FONTS_SOURCE / "b612").exists() or not (FONTS_SOURCE / "hack").exists():
        pytest.skip("Source fonts not available")
    assert get_version() != RELEASE_VERSION, "fixture version must differ from the resolved one"

    root = tmp_path_factory.mktemp("release-version-stamp")
    release_dir = root / "release"
    rebuild_dir = root / "rebuild"

    build_text(FONTS_SOURCE, release_dir, formats=("woff2",), version=RELEASE_VERSION)

    # The tag now exists, so the rebuild resolves the version instead of being told it.
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr("planetaire.recipes.planetaire_mono.get_version", lambda: RELEASE_VERSION)
        build_text(FONTS_SOURCE, rebuild_dir, formats=("woff2",))

    return release_dir, rebuild_dir


def test_build_text_stamps_the_requested_version(builds: tuple[Path, Path]):
    """An explicit version reaches name IDs 3 and 5 and head.fontRevision on every face."""
    release_dir, _ = builds

    faces = sorted(release_dir.glob("*.woff2"))
    assert len(faces) == 10
    for path in faces:
        font = TTFont(path)
        assert font["name"].getDebugName(5) == f"Version {RELEASE_VERSION}", path.name
        unique_id = font["name"].getDebugName(3) or ""
        assert unique_id.startswith(f"{RELEASE_VERSION};"), path.name
        assert round(font["head"].fontRevision, 3) == to_font_revision(RELEASE_VERSION)


def test_release_build_matches_rebuild_at_the_tag(builds: tuple[Path, Path]):
    """The two paths to the published web fonts produce identical bytes.

    Byte equality is the whole contract — the build is reproducible by design
    (`ops/subset.py`), so any difference is a version that failed to thread through.
    """
    release_dir, rebuild_dir = builds

    published = text_web_font_file_names()
    assert {path.name for path in release_dir.iterdir()} == set(published), (
        "the published file set no longer matches what a default Text web build emits"
    )

    differing = [
        name
        for name in published
        if (release_dir / name).read_bytes() != (rebuild_dir / name).read_bytes()
    ]
    assert not differing, f"release build and rebuild differ in: {differing}"
