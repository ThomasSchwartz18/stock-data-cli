# Phase 4: UI Polish & Rich Integration

## Objective
Upgrade plain CLI output into a professional, readable terminal interface using Rich components and consistent semantic styling. This phase focuses on user experience, output clarity, and accessibility without changing core data correctness.

## Required Inputs (Read First)
- `AGENTS.md`
- `docs/plans/ROADMAP.md`
- `.agent_docs/ui_guidelines.md`
- `.agent_docs/architecture.md`
- `.agent_docs/python_standards.md`
- `.agent_docs/testing_and_changes.md`
- `.agent_docs/documentation_guidelines.md`

## Implementation Scope
In scope:
- Rich table rendering for quote/history outputs.
- Loading states via `rich.status.Status` or progress indicators around API calls.
- Consistent gain/loss color coding and error panel formatting.

Out of scope:
- New provider integrations or significant business logic expansion.
- Final grading audit and submission checklist tasks.

## Tasks
1. Table-driven output rendering
   - Replace raw text blocks with `rich.table.Table` where tabular data is shown.
   - Right-align numeric fields and keep column names consistent across commands.
   - Acceptance criteria: quote/history outputs are visually structured and scan-friendly.
2. Semantic styling consistency
   - Apply green for gains and red for losses across all relevant outputs.
   - Standardize success/warning/error/info styles per `.agent_docs/ui_guidelines.md`.
   - Acceptance criteria: style choices are consistent and meaningful throughout commands.
3. Loading and network state UX
   - Add `rich.status.Status` or progress feedback during network requests.
   - Ensure loading indicators terminate cleanly on success or failure.
   - Acceptance criteria: CLI never appears frozen during request latency.
4. Error rendering improvements
   - Present expected operational errors in a `rich.panel.Panel` with actionable text.
   - Keep stack traces hidden unless a `--debug` flag is enabled.
   - Acceptance criteria: failure output is human-readable and non-noisy.
5. Optional UI abstraction cleanup
   - If output logic is duplicated, extract helper renderers under `src/utils/` or `src/cli/`.
   - Acceptance criteria: command files stay focused on routing and orchestration.

## Testing Requirements
- Update CLI tests to assert key output markers/labels compatible with Rich rendering.
- Add tests for positive/negative styling logic if exposed via formatting helpers.
- Add tests for error panel behavior for expected failures.
- Run `pytest -v` locally and ensure CI remains green.

## Documentation Requirements
- Update `README.md` screenshots/GIF placeholders and usage output examples.
- Instruct user to capture new terminal screenshots into `docs/assets/`.

## AI Agent Audit Checklist
Before marking this phase as complete, an AI agent must verify the following:
- [ ] Code changes align with `.agent_docs/` guidelines.
- [ ] Tests have been written/updated and pass locally.
- [ ] The `README.md` has been updated to reflect any new features, flags, or usage commands.
- [ ] No secrets or sensitive information have been hardcoded.
- [ ] The commit history reflects logical, incremental steps.
- [ ] The CI/CD pipeline on the `main` branch is passing.

## Exit Criteria
- Major CLI outputs use Rich tables/panels with consistent semantic styling.
- Network request states show clear progress/spinner feedback.
- Expected errors are presented as user-friendly messages, not raw tracebacks.
- Documentation includes updated usage context and screenshot instructions.
- UX quality aligns with `.agent_docs/ui_guidelines.md`.

## Notes & AI Collaboration Learnings
*Document any challenges, course corrections, or AI collaboration notes here.*
