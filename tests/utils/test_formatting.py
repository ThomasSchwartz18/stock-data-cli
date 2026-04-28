"""Unit tests for value formatting utilities."""

from __future__ import annotations

from src.utils.formatting import format_currency, format_percentage


def test_format_currency_with_standard_value() -> None:
    """Currency helper should format with commas and two decimals."""
    assert format_currency(1234.5) == "$1,234.50"


def test_format_currency_with_none_value() -> None:
    """Currency helper should support null fallback rendering."""
    assert format_currency(None) == "N/A"


def test_format_percentage_with_positive_value() -> None:
    """Positive percentages should include a leading plus by default."""
    assert format_percentage(5.234) == "+5.23%"


def test_format_percentage_with_negative_value() -> None:
    """Negative percentages should preserve negative sign."""
    assert format_percentage(-1.234) == "-1.23%"


def test_format_percentage_with_none_value() -> None:
    """Percentage helper should support null fallback rendering."""
    assert format_percentage(None) == "N/A"
