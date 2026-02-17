"""
Parse and manipulate unicode range specifications.

Supports formats like "U+0041-005A", "U+0041", and comma-separated lists.
"""

from __future__ import annotations

import re


def parse_unicode_ranges(spec: str) -> list[tuple[int, int]]:
    """
    Parse a unicode range string into a list of (start, end) inclusive tuples.

    Accepts formats:
    - Single codepoint: "U+0041" -> [(0x41, 0x41)]
    - Range: "U+0041-005A" -> [(0x41, 0x5A)]
    - Comma-separated: "U+0041-005A,U+0061-007A" -> [(0x41, 0x5A), (0x61, 0x7A)]
    - Whitespace is ignored around commas and ranges.
    """
    ranges: list[tuple[int, int]] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        match = re.match(r"U\+([0-9A-Fa-f]+)(?:-([0-9A-Fa-f]+))?$", part)
        if not match:
            raise ValueError(f"Invalid unicode range: {part!r}")
        start = int(match.group(1), 16)
        end = int(match.group(2), 16) if match.group(2) else start
        if start > end:
            raise ValueError(f"Invalid range: U+{start:04X} > U+{end:04X}")
        ranges.append((start, end))
    if not ranges:
        raise ValueError(f"Empty unicode range specification: {spec!r}")
    return ranges


def codepoints_in_ranges(ranges: list[tuple[int, int]]) -> set[int]:
    """Expand a list of (start, end) ranges into a set of all codepoints."""
    result: set[int] = set()
    for start, end in ranges:
        result.update(range(start, end + 1))
    return result


## Tests


def test_parse_single_codepoint():
    assert parse_unicode_ranges("U+0041") == [(0x41, 0x41)]


def test_parse_range():
    assert parse_unicode_ranges("U+0041-005A") == [(0x41, 0x5A)]


def test_parse_multiple_ranges():
    result = parse_unicode_ranges("U+0041-005A, U+0061-007A")
    assert result == [(0x41, 0x5A), (0x61, 0x7A)]


def test_parse_mixed():
    result = parse_unicode_ranges("U+0041-005A,U+0042")
    assert result == [(0x41, 0x5A), (0x42, 0x42)]


def test_codepoints_in_ranges():
    cps = codepoints_in_ranges([(0x41, 0x43)])
    assert cps == {0x41, 0x42, 0x43}


def test_parse_invalid():
    import pytest

    with pytest.raises(ValueError):
        parse_unicode_ranges("not-a-range")


def test_parse_empty():
    import pytest

    with pytest.raises(ValueError):
        parse_unicode_ranges("")
