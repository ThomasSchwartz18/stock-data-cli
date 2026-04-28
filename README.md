# Stock & Crypto CLI Tracker

![Tests](https://github.com/<your-username>/<your-repo>/actions/workflows/test.yml/badge.svg)

## What It Does
Stock & Crypto CLI Tracker is a Python command line application for checking market data from your terminal. The goal is to provide a clean and reliable workflow for quote lookups, historical snapshots, and market context without leaving the command line.

This project is being built in phased milestones with strong emphasis on testability, modular architecture, and CI/CD automation. Current functionality includes a baseline CLI command used to validate app wiring and delivery pipeline setup.

## Screenshots / GIFs
- Placeholder: `docs/assets/cli-ping-output.png`
- Placeholder: `docs/assets/cli-help-output.png`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
The app reads runtime configuration from environment variables (and supports local `.env` files via `python-dotenv`).

Common variables:
- `REQUEST_TIMEOUT_SECONDS` (default: `10`)
- `MAX_RETRIES` (default: `3`)
- `API_USER_AGENT` (default: `stock-stat-tracker/0.1`)
- `STOCK_API_KEY` (optional, used in provider phases)
- `CRYPTO_API_KEY` (optional, used in provider phases)

## Usage & Examples
Run the baseline command:

```bash
python -m src.cli.app ping
```

Expected output:

```text
pong
```

Show command help:

```bash
python -m src.cli.app --help
```

## Project Structure
```text
.
├── AGENTS.md
├── .agent_docs/
├── docs/plans/
├── src/
│   ├── cli/
│   │   └── app.py
│   ├── core/
│   │   └── api_client.py
│   └── utils/
│       ├── config.py
│       └── formatting.py
├── tests/
│   ├── core/
│   ├── utils/
│   └── test_cli.py
└── .github/workflows/
    └── test.yml
```

## Architecture Notes
- `src/cli/` handles command routing and user interaction.
- `src/core/` contains reusable API client logic with timeout, retry, and normalized error behavior.
- `src/utils/` provides shared config/env parsing and output formatting helpers.
- Tests use mocked HTTP transports; no live external API calls are made in the automated suite.

## Known Limitations & Future Ideas
- Market provider integrations are not implemented yet (planned in upcoming phases).
- Rich output tables and styled status messages are planned for a later UI phase.
- Quote/history commands for stocks and crypto are scheduled for Phase 3.
