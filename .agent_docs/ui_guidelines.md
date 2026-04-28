# UI and Rendering Guidelines

## Purpose
Ensure a consistent, accessible, and visually appealing terminal experience across all standard CLI commands and Text-based User Interfaces (TUI).

## Color Palette and Semantic Styling
- **Market Data**: Always use `green` for positive price movement/gains and `red` for negative price movement/losses.
- **System Status**:
  - Success: `bold green`
  - Warning: `bold yellow`
  - Error: `bold red`
  - Info/Context: `cyan` or `blue`
- Rely on standard terminal color names rather than hardcoded hex codes to ensure compatibility across user terminal profiles (light/dark modes).

## Standard CLI Output (Rich)
- **Tabular Data**: Use `rich.table.Table` for lists of market data (e.g., historical price rows or portfolio comparisons). Right-align numeric columns.
- **Loading States**: Always use `rich.status.Status` or `rich.progress.Progress` when making external API calls so the CLI does not appear frozen.
- **Number Formatting**: Standardize financial formats (e.g., `$1,234.56` for fiat, `+5.23%` for percentages). Limit crypto decimals logically based on value (e.g., BTC to 2 decimals, SHIB to 6+).

## TUI Standards (Textual)
- **Universal Keybindings**: Maintain consistent global keybindings across all screens:
  - `q` or `ctrl+c` to quit the application.
  - `?` or `h` to toggle a help menu.
  - Arrow keys or `j`/`k` for scrolling/navigation.
- **Responsive Design**: Ensure layouts adapt gracefully. Test that widgets do not crash if the user's terminal window is resized smaller than 80x24.
- **Styling Structure**: Prefer defining Textual styles via CSS (`.tcss` files) or the `CSS` class attribute rather than inline styling.

## Error Output
- **Expected Errors**: Do not dump raw Python stack traces for operational errors (e.g., missing API keys, rate limits, invalid tickers). 
- **Formatting**: Render user-facing errors inside a `rich.panel.Panel` with a red border. Provide a clear explanation and an actionable next step.
- **Debug Mode**: Only print raw stack traces if an explicit `--debug` flag is passed.