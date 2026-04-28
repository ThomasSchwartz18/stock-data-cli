# AI Agent Standard Operating Procedure

## 1. Project Context
You are an expert Python software engineer acting as an autonomous coding agent for this repository.

Project goals:
- Build and maintain a secure, robust command-line application for stock and crypto market data.
- Support real-time quotes, recent historical data, and practical market summaries.
- Prioritize reliability, input safety, and testability over quick one-off scripts.

Technical defaults:
- Python version: 3.11+
- CLI framework: `Typer` (preferred) or `Click`
- Terminal rendering: `Rich`
- HTTP client: `httpx` (preferred) or `requests`
- Testing: `pytest`

## 2. Directory Decision Tree Routing
Do not guess implementation details. Before coding, route to the appropriate guidance in `.agent_docs/`:

- If planning, reviewing progress, or looking for the current task:
  - Read the active phase document in `docs/plans/`
- If adding or modifying CLI commands, routing, argument parsing, or command wiring:
  - Read `.agent_docs/architecture.md`
- If altering terminal output, formatting data, adding Rich components, or modifying TUI layouts:
  - Read `.agent_docs/ui_guidelines.md`
- If integrating/changing external market data providers or request behavior:
  - Read `.agent_docs/api_guidelines.md`
- If handling credentials, environment variables, user input validation, local files, or logging:
  - Read `.agent_docs/security.md`
- For coding style, typing, test expectations, and quality gates:
  - Read `.agent_docs/python_standards.md`
- For updating the README, writing documentation, or adding screenshots:
  - Read `.agent_docs/documentation_guidelines.md`
- For running the test suite, fixing CI/CD pipeline issues, or managing Git commits:
  - Read `.agent_docs/testing_and_changes.md`
- To review the final project grading rubric and success criteria:
  - Read `.agent_docs/course_requirements.md`

If multiple categories apply, read all relevant files before implementing.

## 3. Required Procedure for Every Prompt
Follow this sequence for every task.

### Step 1: Acknowledge and Analyze
- Restate the user request in implementation terms.
- Identify the affected modules/files.
- List which `.agent_docs/` files are relevant.

### Step 2: Security and Confidence Check
- Security:
  - Refuse unsafe requests (secret exposure, insecure credential handling, dangerous shell execution patterns).
  - Propose a secure alternative when refusing.
- Confidence:
  - Verify you have enough information (provider docs, expected response shape, edge cases).
  - If missing critical details, ask concise clarifying questions before coding.

### Step 3: Plan Implementation
- Provide a short plan with target files and responsibilities.
- Keep CLI layer separated from market data client logic.
- Prefer incremental, reviewable changes.

### Step 4: Implement
- Write code that follows `.agent_docs/python_standards.md`.
- Keep responsibilities separated:
  - CLI parsing and user interaction in CLI modules.
  - External API interaction in dedicated client/service modules.
  - Shared parsing/formatting/validation in utility modules.
- Add or update docstrings and type hints.

### Step 5: Test Strategy and Verification
- Add/update tests for new behavior and edge cases.
- Prefer deterministic unit tests with mocked external API calls.
- Validate failure paths (timeouts, rate limits, invalid ticker input).
- Summarize what was tested and any residual risks.

## 4. Definition of Done
A task is complete only when all apply:
- Code follows routing and standards docs.
- Secrets are handled safely and not hardcoded.
- Errors are handled with actionable user-facing messages.
- User-facing features or CLI commands are documented in `README.md` with usage examples.
- Tests are added/updated and pass locally (or failures are explicitly reported with cause).
- Changes are modular and maintainable.

## 5. Non-Negotiable Rules
- Never hardcode API keys, tokens, or secrets.
- Never log secrets or sensitive raw payloads.
- Never bypass input validation for ticker/symbol parameters.
- Never couple API calls directly inside CLI command bodies when a service/client layer is expected.
- Never merge significant behavior changes without corresponding tests.

## 6. Student AI Collaboration Reflection (Course Requirement)
> **Note to AI Agent:** Do not modify, rewrite, or overwrite this section under any circumstances. This area is strictly reserved for the student to write their personal reflection on using AI tools for their final project submission.

*(Student: Write your reflection on how AI helped, where it steered you wrong, and what you learned here prior to your final submission on May 3, 2026)*
