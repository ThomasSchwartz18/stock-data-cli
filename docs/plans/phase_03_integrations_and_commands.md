# Phase 3: Market Data Integrations & CLI Commands

## Objective
Deliver real user value by wiring stock and crypto provider integrations into production CLI commands. This phase converts the internal API foundation into end-user workflows for quote retrieval and recent history views while preserving robust error handling and testability.

## Required Inputs (Read First)
- `AGENTS.md`
- `docs/plans/ROADMAP.md`
- `.agent_docs/architecture.md`
- `.agent_docs/api_guidelines.md`
- `.agent_docs/security.md`
- `.agent_docs/python_standards.md`
- `.agent_docs/testing_and_changes.md`
- `.agent_docs/documentation_guidelines.md`

## Implementation Scope
In scope:
- Stock provider integration (for example Yahoo Finance adapter).
- Crypto provider integration (for example CoinGecko adapter).
- CLI commands for `quote` and `history` under `src/cli/commands/`.
- Graceful handling of invalid tickers/symbols and provider rate limits.

Out of scope:
- Advanced TUI or heavy visual enhancements (Phase 4).
- Final rubric audit and reflection tasks (Phase 5).

## Tasks
1. Market service and provider adapters
   - Implement/extend `src/core/market_service.py` and provider-specific methods that consume `api_client`.
   - Normalize provider payloads into stable internal structures for command consumption.
   - Acceptance criteria: CLI layer remains provider-agnostic and depends on service outputs only.
2. Stock integration
   - Implement stock quote/history retrieval logic using selected provider endpoints.
   - Handle symbol not found, malformed response, timeout, and rate-limit conditions.
   - Acceptance criteria: valid symbol returns normalized data; invalid symbol returns clear user-facing error.
3. Crypto integration
   - Implement crypto quote/history retrieval logic using selected provider endpoints.
   - Add symbol/name mapping strategy if provider IDs differ from ticker input format.
   - Acceptance criteria: common crypto symbols resolve reliably with predictable fallback/error behavior.
4. CLI commands
   - Add command modules in `src/cli/commands/` for `quote` and `history`.
   - Register commands in the main CLI app and expose necessary flags (for example market type, interval, limit if applicable).
   - Acceptance criteria: commands return consistent exit codes and user-oriented messages.
5. Error UX hardening
   - Convert service exceptions into actionable CLI output.
   - Ensure invalid input, provider failures, and rate limits do not emit raw tracebacks by default.
   - Acceptance criteria: all expected operational failures are handled cleanly.

## Testing Requirements
- Add service tests for both stock and crypto integration logic with mocked API payloads.
- Add CLI tests for:
  - valid quote command
  - valid history command
  - invalid ticker/symbol handling
  - rate-limit and timeout error messages
- Verify tests are deterministic and do not call live APIs.
- Run `pytest -v` locally before phase completion.

## Documentation Requirements
- Update `README.md` Usage and Examples sections with at least 2-3 realistic command samples.
- Document any provider limitations or symbol mapping caveats in Known Limitations.

## AI Agent Audit Checklist
Before marking this phase as complete, an AI agent must verify the following:
- [ ] Code changes align with `.agent_docs/` guidelines.
- [ ] Tests have been written/updated and pass locally.
- [ ] The `README.md` has been updated to reflect any new features, flags, or usage commands.
- [ ] No secrets or sensitive information have been hardcoded.
- [ ] The commit history reflects logical, incremental steps.
- [ ] The CI/CD pipeline on the `main` branch is passing.

## Exit Criteria
- `quote` and `history` commands are fully wired and functional.
- Stock and crypto data paths are implemented through the shared API/service layer.
- Invalid symbols and provider/rate-limit errors are handled gracefully.
- README examples match working command behavior.
- Test suite meaningfully covers service logic and CLI behavior.

## Notes & AI Collaboration Learnings
*Document any challenges, course corrections, or AI collaboration notes here.*
