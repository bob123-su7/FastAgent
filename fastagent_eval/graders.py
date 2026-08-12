"""Deterministic, provider-independent output graders."""

from __future__ import annotations

from collections.abc import Sequence


def exact_match(output: str, expected: str) -> bool:
    """Compare output and expected text after stripping surrounding whitespace."""
    return output.strip() == expected.strip()


def contains_all(output: str, expected_parts: Sequence[str]) -> bool:
    """Return whether every expected string occurs literally in the output."""
    return all(part in output for part in expected_parts)


def contains_none(output: str, forbidden_parts: Sequence[str]) -> bool:
    """Return whether no forbidden string occurs literally in the output."""
    return not any(part in output for part in forbidden_parts)
