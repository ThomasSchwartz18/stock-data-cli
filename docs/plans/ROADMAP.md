# Project Roadmap: Stock & Crypto CLI Tracker

This document outlines the high-level phases for building the CLI application. AI agents should execute these phases sequentially, creating detailed implementation plans for each phase using the `phase_template.md`.

## Phase 1: Project Bootstrap & CI/CD
**Goal**: Establish the repository foundation, core dependencies, and automated testing pipeline to satisfy course requirements early.
- Define dependencies (`Typer`, `httpx`, `rich`, `pytest`, `python-dotenv`).
- Create the base directory structure (`src/`, `tests/`).
- Implement the entry point (`src/cli/app.py`) with a dummy command.
- Setup `pytest` and create the GitHub Actions workflow (`.github/workflows/test.yml`).
- Draft the initial `README.md`.

## Phase 2: Core API Layer & Utilities
**Goal**: Build a robust, testable foundation for fetching external market data without coupling it to the CLI.
- Implement environment variable loading and configuration (`src/utils/config.py`).
- Create a base HTTP client with timeouts, retry logic, and error handling (`src/core/api_client.py`).
- Implement data formatting utilities for currency and percentages (`src/utils/formatting.py`).
- Write unit tests mocking the API client responses.

## Phase 3: Market Data Integrations & CLI Commands
**Goal**: Connect real data providers (e.g., Yahoo Finance for stocks, CoinGecko for crypto) and wire them to user commands.
- Implement Stock API fetching logic.
- Implement Crypto API fetching logic.
- Create the `quote` and `history` CLI commands (`src/cli/commands/`).
- Ensure all CLI commands gracefully handle invalid tickers and rate limits.
- Write tests asserting CLI output and service logic.

## Phase 4: UI Polish & Rich Integration
**Goal**: Elevate the terminal output to a professional standard using `Rich`, adhering to the `.agent_docs/ui_guidelines.md`.
- Upgrade raw text output to `rich.table.Table` for lists/history.
- Add `rich.status.Status` spinners for network requests.
- Ensure color-coding (green for gains, red for losses) is consistently applied.

## Phase 5: Final Course Audit & Documentation
**Goal**: Guarantee maximum points on the grading rubric.
- Audit `README.md` to ensure it has screenshots, installation guides, and complete usage examples.
- Verify test coverage exceeds the 5-test minimum requirement.
- Student completes the `AGENTS.md` reflection section.

## Phase 6: Interactive Wizard Mode (Bonus UX)
**Goal**: Provide a guided, intuitive decision tree using arrow-key menus so users don't have to memorize long CLI flags.
- Integrate an interactive prompt library (e.g., `questionary` or `InquirerPy`).
- Build an interactive command (e.g., `python -m src.cli.app interactive`) that guides the user through action selection (Quote vs History), market selection, and symbol selection.
- Provide default quick-pick lists (Stocks: AAPL, MSFT, NVDA, SCHD | Crypto: BTC, ETH, XRP, HYPE) with an "Other (Custom Input)" option.
- Wire the interactive selections back into the existing core service layer.

## Phase 7: Advanced UI Polish & Terminal Enhancements
**Goal**: Elevate the visual experience to mimic a professional trading terminal using `Rich` components and ASCII formatting.
- Add Trend Arrows (`▲` / `▼`) and Emojis (📈 / 🪙) to standard output.
- Replace single-row quote tables with styled "Dashboard Cards" using Rich `Panel` and `Columns`.
- Integrate ASCII Sparkline charts into the history table output to visualize trends at a glance.
- Add a stylized ASCII Application Banner to the interactive wizard startup.
