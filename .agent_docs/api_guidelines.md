# API Integration Guidelines

## Purpose
Set strict rules for interacting with stock/crypto data providers (Yahoo Finance, CoinGecko, Alpha Vantage, etc.).

## API Client Requirements
- Implement provider calls in a dedicated module (for example `src/core/api_client.py`).
- Use a reusable client object rather than ad-hoc request calls in multiple places.
- Configure sensible defaults:
  - Timeout per request (for example `5-15s` depending on endpoint).
  - Consistent `User-Agent`.
  - Optional base URL per provider.

## Resilience and Retries
- Handle expected network failures:
  - timeouts
  - connection errors
  - 5xx server errors
  - provider rate limits (`429`)
- Implement retries with exponential backoff and jitter for retryable failures.
- Do not retry non-retryable 4xx errors (except `429`).
- Cap retry attempts to avoid excessive wait or API abuse.

## Rate Limit Awareness
- Detect and surface rate limit responses with clear user messaging.
- If provider headers expose reset or remaining quota, include that context when possible.
- Keep rate-limit handling centralized in client code.

## Response Handling
- Validate status code and required payload fields before downstream use.
- Normalize provider-specific schemas into internal models.
- Return stable internal structures so CLI commands remain provider-agnostic.

## Logging and Observability
- Log high-level request outcome metadata (endpoint, status, duration).
- Never log secrets, API keys, auth headers, or full sensitive payloads.
- Keep logs concise and actionable.

## Testing Requirements
- Mock external requests in tests (`pytest` + `respx`/`responses`/mock transport).
- Add tests for:
  - successful response parsing
  - timeout behavior
  - retry behavior
  - rate-limit handling
  - malformed provider payloads
