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
│   └── cli/
│       └── app.py
├── tests/
│   └── test_cli.py
└── .github/workflows/
    └── test.yml
```

## Known Limitations & Future Ideas
- Market provider integrations are not implemented yet (planned in upcoming phases).
- Rich output tables and styled status messages are planned for a later UI phase.
- Quote/history commands for stocks and crypto are scheduled for Phase 3.
