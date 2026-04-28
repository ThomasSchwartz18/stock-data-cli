# Python Standards

## Baseline
- Target Python 3.11+.
- Follow PEP 8 and keep functions focused and small.
- Use type hints for public functions, methods, and return values.
- Add docstrings for non-trivial modules/classes/functions.

## Style and Quality
- Prefer explicit imports and clear names over clever shorthand.
- Avoid deeply nested control flow; extract helpers when needed.
- Use `Enum`/constants for fixed sets of provider names or modes.
- Keep side effects localized and easy to test.

## Error Handling
- Raise meaningful exceptions with actionable context.
- Avoid broad `except Exception` unless re-raising with context and preserving traceback.
- Convert low-level exceptions to domain-specific errors in core modules.

## Typing Guidance
- Use concrete types where practical (`list[str]`, `dict[str, Any]` sparingly).
- Prefer `TypedDict`/`dataclass` for structured payloads.
- Keep `Any` usage minimal and justified.

## Testing Standards
- Use `pytest`.
- Add or update tests for every behavior change.
- Test normal path and failure path.
- Mock all external API/network interactions in unit tests.
- Keep tests deterministic and independent of real-time market data.

## Suggested Tooling
- Formatter: `black`
- Linter: `ruff`
- Type checker: `mypy` (or `pyright` if repo standard)

## Minimum PR Quality Bar
- New behavior has tests.
- Existing tests still pass.
- No secrets introduced.
- Public API/CLI changes include concise usage examples in docs/help text.
