# Phase 2: Core API Layer & Utilities

## Objective
Build a robust internal foundation for external data access and shared formatting logic before adding user-facing market commands. This phase ensures API behavior is centralized, retry-safe, testable, and decoupled from CLI routing. It is the reliability layer that prevents later command features from becoming brittle.

## Required Inputs (Read First)
- `AGENTS.md`
- `docs/plans/ROADMAP.md`
- `.agent_docs/architecture.md`
- `.agent_docs/api_guidelines.md`
- `.agent_docs/security.md`
- `.agent_docs/python_standards.md`
- `.agent_docs/testing_and_changes.md`

## Implementation Scope
In scope:
- Configuration loading for environment variables.
- Reusable HTTP client with timeout/retry/error normalization.
- Shared formatting utilities for currency and percentage display.
- Unit tests for API client and formatting behavior.

Out of scope:
- Provider-specific stock/crypto endpoint integrations.
- Rich table output polish and advanced UI enhancements.

## Tasks
1. Configuration layer
   - Create `src/utils/config.py`.
   - Implement environment variable access with clear validation and defaults.
   - Add explicit errors for missing required variables.
   - Acceptance criteria: config values are loaded without hardcoded secrets.
2. Base API client
   - Create `src/core/api_client.py`.
   - Implement shared HTTP request method(s) with:
     - request timeout
     - retry with exponential backoff and jitter for retryable errors
     - normalized exceptions for timeout/rate-limit/provider failures
   - Acceptance criteria: network behavior is deterministic under mocked responses.
3. Formatting utilities
   - Create `src/utils/formatting.py`.
   - Implement reusable helpers for:
     - currency formatting (for example `$1,234.56`)
     - signed percentage formatting (for example `+2.13%`, `-0.40%`)
   - Acceptance criteria: helpers handle edge cases like `None`, zero, and large values consistently.
4. Package boundaries and imports
   - Ensure CLI modules do not directly instantiate raw HTTP calls.
   - Keep API and formatting logic reusable from future service modules.
   - Acceptance criteria: architecture aligns with `.agent_docs/architecture.md`.

## Testing Requirements
- Add tests for `src/utils/config.py`:
  - required env present/missing behavior
  - safe fallback/default handling
- Add tests for `src/core/api_client.py` with mocked transport:
  - success path
  - timeout and retry behavior
  - non-retryable 4xx handling
  - retryable 5xx and 429 behavior
- Add tests for `src/utils/formatting.py`:
  - positive/negative/zero percentage output
  - currency formatting and rounding
- Run `pytest -v` locally and ensure CI expectations remain valid.

## Documentation Requirements
- Update `README.md` to mention configuration requirements (for example `.env` expectations).
- Add a short architecture note describing separation of CLI, core client, and utilities.

## AI Agent Audit Checklist
Before marking this phase as complete, an AI agent must verify the following:
- [ ] Code changes align with `.agent_docs/` guidelines.
- [ ] Tests have been written/updated and pass locally.
- [ ] The `README.md` has been updated to reflect any new features, flags, or usage commands.
- [ ] No secrets or sensitive information have been hardcoded.
- [ ] The commit history reflects logical, incremental steps.
- [ ] The CI/CD pipeline on the `main` branch is passing.

## Exit Criteria
- `config.py`, `api_client.py`, and `formatting.py` exist and are tested.
- API client includes timeout + retry + normalized error handling.
- External API calls are mock-tested only (no live dependencies in test suite).
- README explains configuration and current architecture at a high level.
- Foundation is ready for provider-specific integration in Phase 3.

## Notes & AI Collaboration Learnings
*Document any challenges, course corrections, or AI collaboration notes here.*
