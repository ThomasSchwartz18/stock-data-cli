"""Reusable HTTP client with retries and normalized error handling."""

from __future__ import annotations

import random
import time
from dataclasses import dataclass
from typing import Any, Callable, Mapping

import httpx

DEFAULT_TIMEOUT_SECONDS = 10.0
DEFAULT_MAX_RETRIES = 3
DEFAULT_BACKOFF_FACTOR = 0.5
DEFAULT_JITTER_RANGE = (0.0, 0.2)
DEFAULT_USER_AGENT = "stock-stat-tracker/0.1"


class ApiClientError(RuntimeError):
    """Base exception for API client failures."""


class ApiTimeoutError(ApiClientError):
    """Raised when a request times out after retry attempts."""


class ApiRateLimitError(ApiClientError):
    """Raised when a provider rate limit is reached."""

    def __init__(self, message: str, retry_after: str | None = None) -> None:
        super().__init__(message)
        self.retry_after = retry_after


class ApiHTTPError(ApiClientError):
    """Raised for non-retryable or exhausted HTTP status errors."""

    def __init__(self, message: str, status_code: int, response_text: str = "") -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text


class ApiResponseError(ApiClientError):
    """Raised when a response payload cannot be decoded as valid JSON."""


@dataclass(frozen=True)
class RetryPolicy:
    """Retry settings for the API client."""

    max_retries: int = DEFAULT_MAX_RETRIES
    backoff_factor: float = DEFAULT_BACKOFF_FACTOR
    jitter_min: float = DEFAULT_JITTER_RANGE[0]
    jitter_max: float = DEFAULT_JITTER_RANGE[1]


class ApiClient:
    """A reusable synchronous HTTP API client with retry and timeout behavior."""

    def __init__(
        self,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        retry_policy: RetryPolicy | None = None,
        user_agent: str = DEFAULT_USER_AGENT,
        client: httpx.Client | None = None,
        sleep_func: Callable[[float], None] | None = None,
        jitter_func: Callable[[float, float], float] | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/") if base_url else None
        self.timeout = timeout
        self.retry_policy = retry_policy or RetryPolicy()
        self._sleep = sleep_func or time.sleep
        self._jitter = jitter_func or random.uniform
        self._owns_client = client is None
        self._client = client or httpx.Client(
            timeout=timeout,
            headers={"User-Agent": user_agent},
        )

    def close(self) -> None:
        """Close the underlying HTTP client if owned by this instance."""
        if self._owns_client:
            self._client.close()

    def request(
        self,
        method: str,
        endpoint: str,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        """Perform an HTTP request and return the decoded JSON payload."""
        url = self._build_url(endpoint)
        attempts = self.retry_policy.max_retries + 1

        for attempt_index in range(attempts):
            try:
                response = self._client.request(
                    method=method.upper(),
                    url=url,
                    params=params,
                    headers=headers,
                )
            except (httpx.TimeoutException, httpx.ConnectError) as exc:
                if attempt_index >= self.retry_policy.max_retries:
                    raise ApiTimeoutError(
                        f"Request to {url} failed after {attempts} attempts."
                    ) from exc
                self._sleep_for_retry(retry_number=attempt_index + 1)
                continue

            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                if attempt_index >= self.retry_policy.max_retries:
                    raise ApiRateLimitError(
                        f"Rate limit reached for {url}.",
                        retry_after=retry_after,
                    )
                self._sleep_for_retry(retry_number=attempt_index + 1)
                continue

            if 500 <= response.status_code < 600:
                if attempt_index >= self.retry_policy.max_retries:
                    raise ApiHTTPError(
                        message=f"Provider server error from {url}.",
                        status_code=response.status_code,
                        response_text=response.text,
                    )
                self._sleep_for_retry(retry_number=attempt_index + 1)
                continue

            if response.status_code >= 400:
                raise ApiHTTPError(
                    message=f"Provider request failed for {url}.",
                    status_code=response.status_code,
                    response_text=response.text,
                )

            try:
                return response.json()
            except ValueError as exc:
                raise ApiResponseError(f"Invalid JSON payload returned by {url}.") from exc

        raise ApiClientError(f"Unexpected request state while calling {url}.")

    def _build_url(self, endpoint: str) -> str:
        if endpoint.startswith(("https://", "http://")):
            return endpoint
        if not self.base_url:
            raise ValueError("Relative endpoint provided without a base_url.")
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def _sleep_for_retry(self, retry_number: int) -> None:
        base_wait = self.retry_policy.backoff_factor * (2 ** (retry_number - 1))
        jitter = self._jitter(self.retry_policy.jitter_min, self.retry_policy.jitter_max)
        self._sleep(max(0.0, base_wait + jitter))
