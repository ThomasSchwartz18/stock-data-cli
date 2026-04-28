# Architecture Guidelines

## Purpose
Define the code organization and layering rules for this stock/crypto CLI.

## Recommended Project Layout
Use this structure unless the repository already defines a different standard:

```text
src/
  cli/
    app.py
    commands/
      quote.py
      history.py
      crypto.py
  core/
    api_client.py
    market_service.py
    models.py
  utils/
    config.py
    validators.py
    formatting.py
tests/
  cli/
  core/
  utils/
```

## Layer Responsibilities
- `src/cli/`
  - Parse args/options, invoke services, render user output.
  - No raw HTTP requests in command handlers.
- `src/core/`
  - API adapters/clients, provider-specific mapping, business logic.
  - Return typed models or normalized dictionaries.
- `src/utils/`
  - Cross-cutting helpers: config/env loading, validation, formatting, shared errors.

## Design Rules
- Keep command functions thin: route inputs -> call service -> print result.
- Prefer dependency injection for API client/service in tests.
- Centralize provider URL construction and auth handling in API client modules.
- Add a model layer (`dataclass` or `pydantic` if already used) for normalized market data.
- Keep provider-specific response parsing out of CLI.

## Command Addition Checklist
When adding a new CLI command:
- Add command module under `src/cli/commands/`.
- Register it in `src/cli/app.py` (or current command registry).
- Add/extend service logic in `src/core/market_service.py`.
- Add/extend API call methods in `src/core/api_client.py`.
- Add tests:
  - CLI behavior test.
  - Service logic test.
  - API client error-path test with mocks.

## Error Handling Pattern
- Raise typed exceptions in `core` (`RateLimitError`, `ProviderError`, `TimeoutError` wrapper).
- Convert exceptions to user-friendly output in CLI layer.
- Do not print stack traces for expected operational failures.
