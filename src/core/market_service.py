"""Provider integrations and normalized market service methods."""

from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import Any

from src.core.api_client import (
    ApiClient,
    ApiHTTPError,
    RetryPolicy,
)
from src.core.models import HistoryData, HistoryPoint, QuoteData
from src.utils.config import AppConfig

YAHOO_BASE_URL = "https://query1.finance.yahoo.com"
COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"
SUPPORTED_MARKETS = {"stock", "crypto"}
SYMBOL_PATTERN = re.compile(r"^[A-Za-z0-9.\-]{1,20}$")

CRYPTO_SYMBOL_MAP = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "sol": "solana",
    "doge": "dogecoin",
    "ada": "cardano",
    "xrp": "ripple",
}


class MarketServiceError(RuntimeError):
    """Base exception for market service failures."""


class InvalidSymbolError(MarketServiceError):
    """Raised when user symbol input fails validation."""


class SymbolNotFoundError(MarketServiceError):
    """Raised when a provider cannot find requested symbol data."""


class InvalidMarketError(MarketServiceError):
    """Raised for unsupported market types."""


class MarketService:
    """Service layer that normalizes stock and crypto provider payloads."""

    def __init__(self, api_client: ApiClient | None = None, config: AppConfig | None = None) -> None:
        self.config = config or AppConfig.from_env()
        self.api_client = api_client or ApiClient(
            timeout=self.config.request_timeout_seconds,
            retry_policy=RetryPolicy(max_retries=self.config.max_retries),
            user_agent=self.config.user_agent,
        )

    def close(self) -> None:
        """Close managed resources."""
        self.api_client.close()

    def get_quote(self, symbol: str, market: str) -> QuoteData:
        """Fetch and normalize quote data for stock or crypto."""
        normalized_market = market.lower().strip()
        normalized_symbol = self._validate_symbol(symbol)

        if normalized_market not in SUPPORTED_MARKETS:
            raise InvalidMarketError(f"Unsupported market '{market}'. Use 'stock' or 'crypto'.")

        if normalized_market == "stock":
            return self._get_stock_quote(normalized_symbol)
        return self._get_crypto_quote(normalized_symbol)

    def get_history(
        self,
        symbol: str,
        market: str,
        range_value: str = "7d",
        interval: str = "1d",
    ) -> HistoryData:
        """Fetch and normalize historical data for stock or crypto."""
        normalized_market = market.lower().strip()
        normalized_symbol = self._validate_symbol(symbol)

        if normalized_market not in SUPPORTED_MARKETS:
            raise InvalidMarketError(f"Unsupported market '{market}'. Use 'stock' or 'crypto'.")

        if normalized_market == "stock":
            return self._get_stock_history(normalized_symbol, range_value=range_value, interval=interval)
        return self._get_crypto_history(normalized_symbol, range_value=range_value, interval=interval)

    def _validate_symbol(self, symbol: str) -> str:
        candidate = symbol.strip()
        if not SYMBOL_PATTERN.fullmatch(candidate):
            raise InvalidSymbolError(
                "Symbol must be 1-20 characters and only include letters, numbers, '.' or '-'."
            )
        return candidate.upper()

    def _get_stock_quote(self, symbol: str) -> QuoteData:
        payload = self.api_client.request(
            method="GET",
            endpoint=f"{YAHOO_BASE_URL}/v8/finance/chart/{symbol}",
            params={"range": "1d", "interval": "1d"},
        )

        chart_payload = payload.get("chart", {}) if isinstance(payload, dict) else {}
        result_items = chart_payload.get("result", []) if isinstance(chart_payload, dict) else []
        if not result_items:
            raise SymbolNotFoundError(f"Stock symbol '{symbol}' was not found.")

        item = result_items[0]
        meta = item.get("meta", {})
        price = meta.get("regularMarketPrice")
        if price is None:
            raise SymbolNotFoundError(f"No quote data found for stock symbol '{symbol}'.")

        name = meta.get("longName") or meta.get("shortName") or symbol
        price_value = float(price)
        return QuoteData(
            market="stock",
            symbol=meta.get("symbol", symbol),
            name=name,
            price=price_value,
            currency=meta.get("currency", "USD"),
            change_percent=self._stock_change_percent(meta=meta, price=price_value),
        )

    def _get_stock_history(self, symbol: str, range_value: str, interval: str) -> HistoryData:
        payload = self.api_client.request(
            method="GET",
            endpoint=f"{YAHOO_BASE_URL}/v8/finance/chart/{symbol}",
            params={"range": range_value, "interval": interval},
        )

        chart_payload = payload.get("chart", {}) if isinstance(payload, dict) else {}
        result_items = chart_payload.get("result", []) if isinstance(chart_payload, dict) else []
        if not result_items:
            raise SymbolNotFoundError(f"Stock history for '{symbol}' was not found.")

        item = result_items[0]
        timestamps = item.get("timestamp", [])
        close_values = (
            item.get("indicators", {})
            .get("quote", [{}])[0]
            .get("close", [])
        )

        points = self._build_stock_points(timestamps=timestamps, closes=close_values)
        if not points:
            raise MarketServiceError(f"No stock history points available for '{symbol}'.")

        meta = item.get("meta", {})
        return HistoryData(
            market="stock",
            symbol=meta.get("symbol", symbol),
            name=meta.get("symbol", symbol),
            currency=meta.get("currency", "USD"),
            interval=interval,
            points=points,
        )

    def _get_crypto_quote(self, symbol: str) -> QuoteData:
        coin_id = self._resolve_crypto_id(symbol)
        payload = self.api_client.request(
            method="GET",
            endpoint=f"{COINGECKO_BASE_URL}/simple/price",
            params={
                "ids": coin_id,
                "vs_currencies": "usd",
                "include_24hr_change": "true",
            },
        )

        if not isinstance(payload, dict) or coin_id not in payload:
            raise SymbolNotFoundError(f"Crypto symbol '{symbol}' was not found.")

        coin_payload = payload[coin_id]
        usd_price = coin_payload.get("usd")
        if usd_price is None:
            raise SymbolNotFoundError(f"No quote data found for crypto symbol '{symbol}'.")

        return QuoteData(
            market="crypto",
            symbol=symbol,
            name=coin_id,
            price=float(usd_price),
            currency="USD",
            change_percent=self._as_float(coin_payload.get("usd_24h_change")),
        )

    def _get_crypto_history(self, symbol: str, range_value: str, interval: str) -> HistoryData:
        coin_id = self._resolve_crypto_id(symbol)
        days = self._range_days(range_value)
        cg_interval = "daily" if interval == "1d" else "hourly" if interval == "1h" else interval
        payload = self.api_client.request(
            method="GET",
            endpoint=f"{COINGECKO_BASE_URL}/coins/{coin_id}/market_chart",
            params={
                "vs_currency": "usd",
                "days": str(days),
                "interval": cg_interval,
            },
        )

        price_rows = payload.get("prices", []) if isinstance(payload, dict) else []
        points: list[HistoryPoint] = []
        for row in price_rows:
            if not isinstance(row, list) or len(row) != 2:
                continue
            timestamp_ms, value = row
            if value is None:
                continue
            date = datetime.fromtimestamp(timestamp_ms / 1000, tz=UTC).date().isoformat()
            points.append(HistoryPoint(date=date, price=float(value)))

        if not points:
            raise MarketServiceError(f"No crypto history points available for '{symbol}'.")

        return HistoryData(
            market="crypto",
            symbol=symbol,
            name=coin_id,
            currency="USD",
            interval=interval,
            points=points,
        )

    def _resolve_crypto_id(self, symbol: str) -> str:
        lookup = symbol.lower()
        if lookup in CRYPTO_SYMBOL_MAP:
            return CRYPTO_SYMBOL_MAP[lookup]

        payload = self.api_client.request(
            method="GET",
            endpoint=f"{COINGECKO_BASE_URL}/search",
            params={"query": lookup},
        )
        coins = payload.get("coins", []) if isinstance(payload, dict) else []
        for coin in coins:
            coin_symbol = str(coin.get("symbol", "")).lower()
            coin_name = str(coin.get("name", "")).lower()
            coin_id = str(coin.get("id", "")).lower()
            if lookup in {coin_symbol, coin_name, coin_id}:
                return coin.get("id")
        raise SymbolNotFoundError(f"Crypto symbol '{symbol}' was not found.")

    def _build_stock_points(self, timestamps: list[Any], closes: list[Any]) -> list[HistoryPoint]:
        points: list[HistoryPoint] = []
        for ts, close_value in zip(timestamps, closes):
            if close_value is None:
                continue
            date = datetime.fromtimestamp(ts, tz=UTC).date().isoformat()
            points.append(HistoryPoint(date=date, price=float(close_value)))
        return points

    def _range_days(self, range_value: str) -> int:
        candidate = range_value.lower().strip()
        if not candidate.endswith("d"):
            return 7
        numeric = candidate[:-1]
        if not numeric.isdigit():
            return 7
        return max(1, int(numeric))

    def _as_float(self, value: Any) -> float | None:
        if value is None:
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            raise MarketServiceError("Unexpected provider payload value type.") from None

    def _stock_change_percent(self, meta: dict[str, Any], price: float) -> float | None:
        """Resolve stock percent change from direct field or computed fallbacks."""
        direct_percent = self._as_float(meta.get("regularMarketChangePercent"))
        if direct_percent is not None:
            return direct_percent

        change_value = self._as_float(meta.get("regularMarketChange"))
        previous_close = self._as_float(
            meta.get("regularMarketPreviousClose")
            or meta.get("previousClose")
            or meta.get("chartPreviousClose")
        )

        if previous_close and change_value is not None:
            return (change_value / previous_close) * 100

        if previous_close:
            return ((price - previous_close) / previous_close) * 100

        return None
