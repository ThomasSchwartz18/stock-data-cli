"""Formatting helpers for market values shown in the CLI."""

from __future__ import annotations


def trend_arrow(value: float | int | None) -> str:
    """Return an up/down/flat arrow based on numeric trend value."""
    if value is None:
        return "■"
    numeric = float(value)
    if numeric > 0:
        return "▲"
    if numeric < 0:
        return "▼"
    return "■"


def trend_word(value: float | int | None) -> str:
    """Return a short semantic trend label for UI messaging."""
    if value is None:
        return "Flat"
    numeric = float(value)
    if numeric > 0:
        return "Bullish"
    if numeric < 0:
        return "Bearish"
    return "Flat"


def format_currency(
    value: float | int | None,
    decimals: int = 2,
    currency_symbol: str = "$",
    null_value: str = "N/A",
) -> str:
    """Format a numeric value as a currency string."""
    if value is None:
        return null_value
    return f"{currency_symbol}{value:,.{decimals}f}"


def format_percentage(
    value: float | int | None,
    decimals: int = 2,
    include_sign: bool = True,
    with_arrow: bool = False,
    null_value: str = "N/A",
) -> str:
    """Format a numeric value as a percentage string."""
    if value is None:
        return null_value

    numeric = float(value)
    percentage = f"{numeric:.{decimals}f}%"
    if include_sign and numeric > 0:
        percentage = f"+{percentage}"

    if with_arrow:
        return f"{trend_arrow(numeric)} {percentage}"
    return percentage
