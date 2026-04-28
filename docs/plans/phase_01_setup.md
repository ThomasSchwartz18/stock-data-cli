# Phase 1: Project Bootstrap & CI/CD

## Objective
Establish the project baseline so every later phase can ship quickly and safely. This phase creates the runtime dependencies, CLI skeleton, initial tests, and CI workflow required for reliable iteration. Completing this phase early de-risks grading criteria around repository quality, tests, and automation.

## Phase Status
- [x] Task 1 complete: Dependency and environment baseline
- [x] Task 2 complete: CLI skeleton and package layout
- [x] Task 3 complete: Initial test suite and test command
- [x] Task 4 complete: CI/CD workflow created
- [x] Task 5 complete: README baseline initialized

## Required Inputs (Read First)
- `AGENTS.md`
- `docs/plans/ROADMAP.md`
- `.agent_docs/architecture.md`
- `.agent_docs/python_standards.md`
- `.agent_docs/testing_and_changes.md`
- `.agent_docs/documentation_guidelines.md`
- `.agent_docs/course_requirements.md`

## Implementation Scope
In scope:
- Project skeleton, dependency setup, base CLI entrypoint, smoke tests, CI workflow, and README scaffold.
- Initial module boundaries under `src/` and `tests/`.

Out of scope:
- Real market data providers.
- Rich UI polish and advanced command features.

## Tasks
1. Dependency and environment baseline
   - Create `requirements.txt` (or equivalent lock strategy) containing: `typer`, `httpx`, `rich`, `pytest`, `pytest-mock`, `python-dotenv`.
   - Add `.gitignore` entries for `.env`, virtual environments, and Python cache artifacts.
   - Acceptance criteria: fresh virtual environment installs all dependencies without manual edits.
2. CLI skeleton and package layout
   - Create `src/cli/app.py` with a basic Typer app and a lightweight `ping` or `hello` command.
   - Create minimal package files such as `src/__init__.py` and `src/cli/__init__.py`.
   - Acceptance criteria: command runs locally and returns deterministic output.
3. Initial test suite and test command
   - Create `tests/test_cli.py` with Typer `CliRunner` coverage for baseline command behavior.
   - Add at least 2-3 tests in this phase to establish test style (success path, help path, invalid invocation path).
   - Acceptance criteria: `pytest -v` passes locally with deterministic results.
4. CI/CD workflow
   - Create `.github/workflows/test.yml` to run test suite on pushes to `main` and pull requests.
   - Include checkout, Python setup, dependency install, and test execution steps.
   - Acceptance criteria: workflow is valid YAML and runs without manual interaction.
5. README baseline
   - Initialize `README.md` sections defined in `.agent_docs/documentation_guidelines.md`.
   - Include at least one command example that matches implemented CLI behavior.
   - Acceptance criteria: a new contributor can run the baseline command from README steps.

## Testing Requirements
- Add CLI tests using `CliRunner` for command output and exit code.
- Run `pytest -v` locally before considering this phase complete.
- Ensure CI workflow executes the same test command used locally.

## Documentation Requirements
- Update `README.md` installation and usage sections to match current project state.
- If command output visuals are added, note placeholder screenshot location at `docs/assets/`.

## AI Agent Audit Checklist
Before marking this phase as complete, an AI agent must verify the following:
- [x] Code changes align with `.agent_docs/` guidelines.
- [x] Tests have been written/updated and pass locally.
- [x] The `README.md` has been updated to reflect any new features, flags, or usage commands.
- [x] No secrets or sensitive information have been hardcoded.
- [ ] The commit history reflects logical, incremental steps.
- [ ] The CI/CD pipeline on the `main` branch is passing.

## Exit Criteria
- Baseline CLI command is runnable from `src/cli/app.py`.
- `pytest -v` passes locally.
- GitHub Actions workflow runs tests on push/PR.
- README contains install + usage baseline content consistent with current code.
- Repo is ready for API-layer implementation without structural rework.

## Notes & AI Collaboration Learnings
*Document any challenges, course corrections, or AI collaboration notes here. This will make it significantly easier to write your final course reflection in `AGENTS.md` at the end of the project.*
