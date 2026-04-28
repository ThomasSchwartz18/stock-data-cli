"""Formatting helpers for market values shown in the CLI."""

from __future__ import annotations


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
    null_value: str = "N/A",
) -> str:
    """Format a numeric value as a percentage string."""
    if value is None:
        return null_value

    numeric = float(value)
    percentage = f"{numeric:.{decimals}f}%"
    if include_sign and numeric > 0:
        return f"+{percentage}"
    return percentage
