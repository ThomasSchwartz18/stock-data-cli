# Phase 7: Advanced UI Polish & Terminal Enhancements

## Objective
Elevate the application's visual appeal to mimic a professional trading terminal. This phase focuses purely on presentation layer enhancements—Dashboard Cards, Sparklines, Banners, and Emojis—without altering the core service logic. This directly contributes to a high-quality user experience and strong "Code Quality" grading marks.

## Phase Status
- [x] Task 1 complete: Trend arrows and market emojis integrated into renderers
- [x] Task 2 complete: Quote output refactored from table to dashboard card panel layout
- [x] Task 3 complete: History sparkline generation and display added
- [x] Task 4 complete: Interactive wizard startup banner added

## Required Inputs (Read First)
- `AGENTS.md`
- `docs/plans/ROADMAP.md`
- `.agent_docs/ui_guidelines.md`
- `src/cli/rendering.py`

## Implementation Scope
In scope:
- Refactoring how `QuoteData` is displayed (Card/Panel instead of Table).
- Enhancing how `HistoryData` is displayed (adding ASCII sparklines).
- Adding emojis and trend arrows to text output.
- Displaying an ASCII banner in the interactive wizard.
- Modifying `src/cli/rendering.py`, `src/cli/wizard.py`, and `src/utils/formatting.py`.

Out of scope:
- Changes to `src/core/market_service.py` or `api_client.py`.
- Implementing full-screen Textual TUI applications.

## Tasks
1. **Trend Arrows & Emojis**
   - Update formatters and renderers to append `▲` (green) or `▼` (red) based on positive/negative percentage changes.
   - Add market indicator emojis (e.g., 📈 for stock, 🪙 for crypto) to output titles.
2. **Dashboard Cards for Quotes**
   - Refactor `build_quote_table` into a new `build_quote_card` function.
   - Use Rich's `Panel` and `Columns` to center the price and emphasize the symbol/name.
   - Color the card border based on the 24h change (green for up, red for down).
3. **History Sparklines**
   - Create a utility in `src/cli/rendering.py` to generate an ASCII sparkline (using ` ▂▃▄▅▆▇█`) from the list of historical prices.
   - Inject this sparkline either above or inside the existing `build_history_table`.
4. **Interactive Application Banner**
   - Print a stylized ASCII art banner (e.g., using `pyfiglet` or Rich text styling) at the beginning of `interactive_command` in `src/cli/wizard.py`.

## Testing Requirements
- Update existing CLI tests in `tests/test_cli.py` or create new rendering tests to ensure the new components do not crash.
- Ensure `pytest -v` runs cleanly. (Note: output string matching tests may need to be updated to account for new Unicode characters/panels).

## Documentation Requirements
- Update the `README.md` Screenshots section. Take new screenshots of the Dashboard Cards and Sparklines and place them in `docs/assets/`.

## AI Agent Audit Checklist
Before marking this phase as complete, verify:
- [x] Quotes render as stylized Panels/Cards rather than generic Tables.
- [x] History output includes a visual sparkline.
- [x] The interactive wizard displays a welcome banner.
- [x] Existing tests have been updated to pass with the new UI formats.

## Notes & AI Collaboration Learnings
- Reused existing service-layer methods so this phase stayed presentation-only.
- Updated CLI and wizard tests to assert resilient substrings due Rich wrapping behavior with emojis/panels.
