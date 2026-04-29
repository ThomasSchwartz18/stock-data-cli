"""Unit tests for value formatting utilities."""

from __future__ import annotations

from src.utils.formatting import (
    format_currency,
    format_percentage,
    trend_arrow,
    trend_word,
)


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


def test_format_percentage_with_arrow() -> None:
    """Percentage helper should optionally include trend arrows."""
    assert format_percentage(3.2, with_arrow=True) == "▲ +3.20%"
    assert format_percentage(-3.2, with_arrow=True) == "▼ -3.20%"


def test_trend_helpers_return_expected_values() -> None:
    """Trend helpers should map values to arrows and labels."""
    assert trend_arrow(1.0) == "▲"
    assert trend_arrow(-1.0) == "▼"
    assert trend_arrow(0.0) == "■"
    assert trend_word(1.0) == "Bullish"
    assert trend_word(-1.0) == "Bearish"
    assert trend_word(0.0) == "Flat"
