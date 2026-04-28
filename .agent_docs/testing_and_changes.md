# Testing Suite and Change Management Guidelines

## Purpose
Ensure a meaningful commit history, a robust CI/CD pipeline, and a healthy test suite in accordance with the course requirements.

## Test Suite Management
- **Coverage Rule**: The course requires at least 5 tests covering core logic. Our goal is to exceed this by ensuring every command, utility, and API client has explicit test coverage.
- **Execution**: Agents should instruct the user to run `pytest -v` locally before finalizing any code changes.
- **Mocks & Fixtures**: External API endpoints must be mocked (e.g., using `pytest-mock`, `respx`, or `responses`). Never hit live production APIs during automated test execution.

## CI/CD Pipeline Maintenance
- The GitHub Actions workflow in `.github/workflows/` must remain green.
- If a change requires a new dependency, explicitly flag that `requirements.txt` (or equivalent) and the CI/CD configuration must be updated.
- If the CI/CD pipeline fails, an agent's top priority must be to diagnose and fix the failing test before adding new features.

## Commit History & Change Management
- **Commit Early and Often**: Do not batch massive changes into a single final commit.
- **Logical Steps**: Break down features into smaller commits (e.g., "Add API client for crypto", "Add tests for API client", "Wire CLI command to API client").
- **Commit Message Format**:
  - Use clear, imperative mood summaries (e.g., "Add timeout handling to Yahoo Finance client").
  - Include context in the body if the change is complex.
- **Agent Requirement**: After completing a logical task, AI agents should provide the user with the exact `git add` and `git commit` commands to execute.

## Refactoring
- When altering existing application behavior, always run the test suite *before* making the change to establish a baseline, and *after* to verify no regressions occurred.