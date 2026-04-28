"""Normalized market data models used by service and CLI layers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class QuoteData:
    """Normalized quote payload for a stock or crypto symbol."""

    market: str
    symbol: str
    name: str
    price: float
    currency: str = "USD"
    change_percent: float | None = None


@dataclass(frozen=True)
class HistoryPoint:
    """Single historical price point."""

    date: str
    price: float


@dataclass(frozen=True)
class HistoryData:
    """Historical price payload for a stock or crypto symbol."""

    market: str
    symbol: str
    name: str
    currency: str
    interval: str
    points: list[HistoryPoint]
