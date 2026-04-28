"""Unit tests for the shared API client."""

from __future__ import annotations

import httpx
import pytest

from src.core.api_client import (
    ApiClient,
    ApiHTTPError,
    ApiRateLimitError,
    ApiResponseError,
    ApiTimeoutError,
    RetryPolicy,
)


def test_request_success_returns_decoded_json() -> None:
    """Successful requests should return decoded JSON payloads."""

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/quote"
        return httpx.Response(200, json={"symbol": "AAPL", "price": 180.5})

    client = httpx.Client(transport=httpx.MockTransport(handler))
    api_client = ApiClient(base_url="https://example.test", client=client)

    payload = api_client.request("GET", "/quote")

    assert payload == {"symbol": "AAPL", "price": 180.5}


def test_request_retries_on_timeout_then_succeeds() -> None:
    """Timeouts should trigger retry logic before succeeding."""
    call_count = {"count": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        call_count["count"] += 1
        if call_count["count"] == 1:
            raise httpx.ReadTimeout("timed out", request=request)
        return httpx.Response(200, json={"ok": True})

    client = httpx.Client(transport=httpx.MockTransport(handler))
    api_client = ApiClient(
        base_url="https://example.test",
        client=client,
        retry_policy=RetryPolicy(max_retries=1, backoff_factor=0.0, jitter_min=0.0, jitter_max=0.0),
        sleep_func=lambda _seconds: None,
    )

    payload = api_client.request("GET", "/quote")

    assert payload == {"ok": True}
    assert call_count["count"] == 2


def test_request_raises_on_non_retryable_4xx() -> None:
    """Non-retryable 4xx responses should raise immediately."""

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"detail": "not found"})

    client = httpx.Client(transport=httpx.MockTransport(handler))
    api_client = ApiClient(base_url="https://example.test", client=client)

    with pytest.raises(ApiHTTPError) as exc_info:
        api_client.request("GET", "/quote")

    assert exc_info.value.status_code == 404


def test_request_retries_then_raises_on_5xx() -> None:
    """5xx responses should retry until attempts are exhausted."""
    call_count = {"count": 0}

    def handler(_request: httpx.Request) -> httpx.Response:
        call_count["count"] += 1
        return httpx.Response(503, json={"detail": "unavailable"})

    client = httpx.Client(transport=httpx.MockTransport(handler))
    api_client = ApiClient(
        base_url="https://example.test",
        client=client,
        retry_policy=RetryPolicy(max_retries=2, backoff_factor=0.0, jitter_min=0.0, jitter_max=0.0),
        sleep_func=lambda _seconds: None,
    )

    with pytest.raises(ApiHTTPError) as exc_info:
        api_client.request("GET", "/quote")

    assert exc_info.value.status_code == 503
    assert call_count["count"] == 3


def test_request_raises_rate_limit_with_retry_after() -> None:
    """429 responses should eventually raise a rate limit error."""

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(429, headers={"Retry-After": "30"})

    client = httpx.Client(transport=httpx.MockTransport(handler))
    api_client = ApiClient(
        base_url="https://example.test",
        client=client,
        retry_policy=RetryPolicy(max_retries=0, backoff_factor=0.0, jitter_min=0.0, jitter_max=0.0),
        sleep_func=lambda _seconds: None,
    )

    with pytest.raises(ApiRateLimitError) as exc_info:
        api_client.request("GET", "/quote")

    assert exc_info.value.retry_after == "30"


def test_request_raises_response_error_for_invalid_json() -> None:
    """Invalid JSON payloads should raise an ApiResponseError."""

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text="not-json")

    client = httpx.Client(transport=httpx.MockTransport(handler))
    api_client = ApiClient(base_url="https://example.test", client=client)

    with pytest.raises(ApiResponseError):
        api_client.request("GET", "/quote")


def test_request_raises_timeout_after_exhausted_retries() -> None:
    """Repeated timeout exceptions should raise ApiTimeoutError."""

    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("timed out", request=request)

    client = httpx.Client(transport=httpx.MockTransport(handler))
    api_client = ApiClient(
        base_url="https://example.test",
        client=client,
        retry_policy=RetryPolicy(max_retries=1, backoff_factor=0.0, jitter_min=0.0, jitter_max=0.0),
        sleep_func=lambda _seconds: None,
    )

    with pytest.raises(ApiTimeoutError):
        api_client.request("GET", "/quote")
