# Phase 6: Interactive Wizard Mode

## Objective
Create an intuitive, arrow-key-driven interactive menu (wizard) for users who prefer not to type out long command-line arguments. This phase introduces a guided decision tree featuring popular default symbols with fallbacks for custom inputs, drastically improving the CLI's User Experience (UX).

## Phase Status
- [x] Task 1 complete: `questionary` dependency added to requirements
- [x] Task 2 complete: Wizard decision-tree module implemented in `src/cli/wizard.py`
- [x] Task 3 complete: `interactive` command integrated into CLI app and wired to existing service/rendering stack

## Required Inputs (Read First)
- `AGENTS.md`
- `docs/plans/ROADMAP.md`
- `.agent_docs/ui_guidelines.md`
- `.agent_docs/architecture.md`

## Implementation Scope
In scope:
- Adding a library like `questionary` or `InquirerPy` to handle arrow-key navigation in the terminal.
- Creating a new `interactive` (or default `start`) command.
- Building a decision tree: Action (Quote/History) -> Market (Stock/Crypto) -> Symbol (Defaults or Custom) -> Timeframe (if History).
- Default Stock Options: NVDA, AAPL, MSFT, SCHD, Other.
- Default Crypto Options: BTC, ETH, XRP, HYPE, Other.

Out of scope:
- Full-screen Textual UI dashboard (this is just an interactive prompt wizard).
- Changing the core `MarketService` (the wizard should reuse existing methods).

## Tasks
1. **Dependency Addition**
   - Add `questionary` (or equivalent) to `requirements.txt`.
2. **Wizard Logic Construction**
   - Create `src/cli/wizard.py` or a similar dedicated module to house the prompt questions to keep the CLI app lean.
   - Implement the decision trees handling the user's flow.
3. **CLI Integration**
   - Add an `interactive` command in `src/cli/app.py`.
   - Pass the collected wizard answers into the existing `MarketService` methods.
   - Format and render the final outputs using the existing Rich formatting utilities.

## Testing Requirements
- Use `unittest.mock.patch` to simulate user arrow-key selections and ensure the correct service methods are called.
- Ensure the wizard safely exits if the user presses `Ctrl+C` midway through the prompts.

## Documentation Requirements
- Update `README.md` to highlight the new Interactive Wizard as a primary feature.
- Add a screenshot placeholder indicating where the arrow-key menu should be shown.

## AI Agent Audit Checklist
Before marking this phase as complete, verify:
- [x] The interactive prompts work seamlessly with arrow keys.
- [x] Selecting "Other" successfully prompts the user to type in a custom symbol or timeframe.
- [x] The codebase dependencies and `requirements.txt` are updated.

## Notes & AI Collaboration Learnings
*Document any challenges integrating the interactive prompt library with Typer here.*

Implemented behaviors:
- Arrow-key wizard flow: `Action -> Market -> Symbol -> (History options if applicable)`.
- "Other (Custom Input)" prompts for symbol, range, interval, and row limit.
- Graceful Ctrl+C/cancel behavior exits safely with a user-facing cancellation panel.
- Wizard output reuses existing Rich tables and service-layer integrations.
