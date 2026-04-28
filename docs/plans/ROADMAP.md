# Project Roadmap: Stock & Crypto CLI Tracker

This document outlines the high-level phases for building the CLI application. AI agents should execute these phases sequentially, creating detailed implementation plans for each phase using the canonical template at `.agent_docs/phase_template.md`.

## Phase 1: Project Bootstrap & CI/CD
Phase file: `docs/plans/phase_01_setup.md`

**Goal**: Establish the repository foundation, core dependencies, and automated testing pipeline to satisfy course requirements early.
- Define dependencies (`Typer`, `httpx`, `rich`, `pytest`, `python-dotenv`).
- Create the base directory structure (`src/`, `tests/`).
- Implement the entry point (`src/cli/app.py`) with a dummy command.
- Setup `pytest` and create the GitHub Actions workflow (`.github/workflows/test.yml`).
- Draft the initial `README.md`.

## Phase 2: Core API Layer & Utilities
Phase file: `docs/plans/phase_02_core_api_and_utils.md`

**Goal**: Build a robust, testable foundation for fetching external market data without coupling it to the CLI.
- Implement environment variable loading and configuration (`src/utils/config.py`).
- Create a base HTTP client with timeouts, retry logic, and error handling (`src/core/api_client.py`).
- Implement data formatting utilities for currency and percentages (`src/utils/formatting.py`).
- Write unit tests mocking the API client responses.

## Phase 3: Market Data Integrations & CLI Commands
Phase file: `docs/plans/phase_03_integrations_and_commands.md`

**Goal**: Connect real data providers (e.g., Yahoo Finance for stocks, CoinGecko for crypto) and wire them to user commands.
- Implement Stock API fetching logic.
- Implement Crypto API fetching logic.
- Create the `quote` and `history` CLI commands (`src/cli/commands/`).
- Ensure all CLI commands gracefully handle invalid tickers and rate limits.
- Write tests asserting CLI output and service logic.

## Phase 4: UI Polish & Rich Integration
Phase file: `docs/plans/phase_04_ui_polish.md`

**Goal**: Elevate the terminal output to a professional standard using `Rich`, adhering to the `.agent_docs/ui_guidelines.md`.
- Upgrade raw text output to `rich.table.Table` for lists/history.
- Add `rich.status.Status` spinners for network requests.
- Ensure color-coding (green for gains, red for losses) is consistently applied.

## Phase 5: Final Course Audit & Documentation
Phase file: `docs/plans/phase_05_final_audit.md`

**Goal**: Guarantee maximum points on the grading rubric.
- Audit `README.md` to ensure it has screenshots, installation guides, and complete usage examples.
- Verify test coverage exceeds the 5-test minimum requirement.
- Student completes the `AGENTS.md` reflection section.
