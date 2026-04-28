# Phase Planning Template (AI-Driven)

Use this template when drafting a new `docs/plans/phase_XX_*.md` file.

## Header
- `# Phase [X]: [Phase Name]`
- One sentence tying this phase to the roadmap and end goal of the Stock/Crypto CLI.

## Objective
- 2-4 sentences that define:
  - What user-visible capability is unlocked.
  - What internal architecture is established.
  - Why this phase matters to course grading criteria.

## Required Inputs (Read First)
- List all docs the agent must read before coding (for example: `AGENTS.md`, `ROADMAP.md`, and relevant files in `.agent_docs/`).

## Implementation Scope
- Explicitly list what is in scope and out of scope.
- Include paths/modules the agent is expected to touch.

## Task Breakdown
Use numbered tasks with clear output expectations:
1. Task name
2. Files to create/update
3. Implementation requirements
4. Acceptance criteria

## Testing Requirements
- Define the exact tests to add or update.
- Include success criteria for local `pytest -v` and CI workflow checks.
- Require mocked external API calls for deterministic tests.

## Documentation Requirements
- State exact `README.md` sections to update.
- If UI changed, instruct placement of screenshots under `docs/assets/`.

## AI Agent Audit Checklist
Before marking a phase complete, verify:
- [ ] Scope matches this phase and roadmap objective.
- [ ] Code changes align with all relevant `.agent_docs/` guidance files.
- [ ] Tests were added/updated and pass locally.
- [ ] CI/CD pipeline remains green.
- [ ] `README.md` and usage examples reflect delivered behavior.
- [ ] No secrets/sensitive information were hardcoded or logged.
- [ ] Changes are modular with clear separation of CLI/core/utils responsibilities.
- [ ] Commit history reflects logical incremental work.

## Exit Criteria
- List 3-6 measurable completion conditions that define "phase done."

## Notes & AI Collaboration Learnings
- Reserve space for implementation notes, tradeoffs, and follow-up items that help final reflection writing in `AGENTS.md`.
