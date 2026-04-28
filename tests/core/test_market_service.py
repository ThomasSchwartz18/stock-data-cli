"""Unit tests for market service provider integrations."""

from __future__ import annotations

import httpx
import pytest

from src.core.api_client import ApiClient, ApiRateLimitError, RetryPolicy
from src.core.market_service import (
    InvalidMarketError,
    InvalidSymbolError,
    MarketService,
    SymbolNotFoundError,
)


def _make_service(handler: httpx.MockTransport) -> MarketService:
    client = httpx.Client(transport=handler)
    api_client = ApiClient(
        client=client,
        retry_policy=RetryPolicy(max_retries=0, backoff_factor=0.0, jitter_min=0.0, jitter_max=0.0),
        sleep_func=lambda _seconds: None,
    )
    return MarketService(api_client=api_client)


def test_get_stock_quote_success() -> None:
    """Stock quote data should parse from Yahoo quote payload."""

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v7/finance/quote"
        return httpx.Response(
            200,
            json={
                "quoteResponse": {
                    "result": [
                        {
                            "symbol": "AAPL",
                            "longName": "Apple Inc.",
                            "regularMarketPrice": 189.32,
                            "regularMarketChangePercent": 1.23,
                            "currency": "USD",
                        }
                    ]
                }
            },
        )

    service = _make_service(httpx.MockTransport(handler))
    quote = service.get_quote("aapl", "stock")

    assert quote.symbol == "AAPL"
    assert quote.name == "Apple Inc."
    assert quote.price == 189.32
    assert quote.change_percent == 1.23


def test_get_stock_quote_symbol_not_found() -> None:
    """Missing stock results should raise SymbolNotFoundError."""

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"quoteResponse": {"result": []}})

    service = _make_service(httpx.MockTransport(handler))
    with pytest.raises(SymbolNotFoundError):
        service.get_quote("MISSING", "stock")


def test_get_crypto_quote_success_from_symbol_map() -> None:
    """Mapped crypto symbols should resolve without search endpoint."""

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v3/simple/price"
        assert request.url.params.get("ids") == "bitcoin"
        return httpx.Response(200, json={"bitcoin": {"usd": 65000.0, "usd_24h_change": 2.5}})

    service = _make_service(httpx.MockTransport(handler))
    quote = service.get_quote("btc", "crypto")

    assert quote.market == "crypto"
    assert quote.name == "bitcoin"
    assert quote.price == 65000.0
    assert quote.change_percent == 2.5


def test_get_crypto_quote_resolves_search_result() -> None:
    """Unknown crypto symbol should resolve via CoinGecko search."""
    calls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request.url.path)
        if request.url.path == "/api/v3/search":
            return httpx.Response(
                200,
                json={"coins": [{"id": "matic-network", "symbol": "matic", "name": "Polygon"}]},
            )
        if request.url.path == "/api/v3/simple/price":
            return httpx.Response(
                200,
                json={"matic-network": {"usd": 0.89, "usd_24h_change": -0.4}},
            )
        raise AssertionError(f"Unexpected path {request.url.path}")

    service = _make_service(httpx.MockTransport(handler))
    quote = service.get_quote("matic", "crypto")

    assert quote.name == "matic-network"
    assert quote.price == 0.89
    assert calls == ["/api/v3/search", "/api/v3/simple/price"]


def test_get_stock_history_success() -> None:
    """Stock history should parse timestamp and close rows."""

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v8/finance/chart/AAPL"
        return httpx.Response(
            200,
            json={
                "chart": {
                    "result": [
                        {
                            "meta": {"symbol": "AAPL", "currency": "USD"},
                            "timestamp": [1714176000, 1714262400],
                            "indicators": {"quote": [{"close": [180.1, 181.9]}]},
                        }
                    ]
                }
            },
        )

    service = _make_service(httpx.MockTransport(handler))
    history = service.get_history("AAPL", "stock", range_value="5d", interval="1d")

    assert history.symbol == "AAPL"
    assert len(history.points) == 2
    assert history.points[0].price == 180.1


def test_get_crypto_history_success() -> None:
    """Crypto history should parse market chart price rows."""

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/v3/search":
            return httpx.Response(
                200,
                json={"coins": [{"id": "ethereum", "symbol": "eth", "name": "Ethereum"}]},
            )
        if request.url.path == "/api/v3/coins/ethereum/market_chart":
            return httpx.Response(
                200,
                json={"prices": [[1714176000000, 3000.0], [1714262400000, 3100.0]]},
            )
        raise AssertionError(f"Unexpected path {request.url.path}")

    service = _make_service(httpx.MockTransport(handler))
    history = service.get_history("eth", "crypto", range_value="7d", interval="1d")

    assert history.symbol == "ETH"
    assert history.name == "ethereum"
    assert len(history.points) == 2


def test_get_quote_rejects_invalid_symbol_input() -> None:
    """Invalid symbol format should fail before any provider request."""
    service = _make_service(httpx.MockTransport(lambda _request: httpx.Response(200, json={})))
    with pytest.raises(InvalidSymbolError):
        service.get_quote("DROP TABLE;", "stock")


def test_get_quote_rejects_invalid_market() -> None:
    """Unsupported market values should raise InvalidMarketError."""
    service = _make_service(httpx.MockTransport(lambda _request: httpx.Response(200, json={})))
    with pytest.raises(InvalidMarketError):
        service.get_quote("AAPL", "forex")


def test_get_quote_propagates_rate_limit_error() -> None:
    """Provider rate limit responses should surface as ApiRateLimitError."""

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(429, headers={"Retry-After": "20"})

    service = _make_service(httpx.MockTransport(handler))
    with pytest.raises(ApiRateLimitError):
        service.get_quote("AAPL", "stock")
