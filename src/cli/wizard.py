"""Interactive wizard command flow for guided market lookups."""

from __future__ import annotations

import traceback
from typing import Any, Sequence

import typer
from rich.panel import Panel

from src.cli.commands.market import get_console, get_market_service
from src.cli.rendering import (
    build_history_table,
    build_quote_card,
    build_wizard_banner,
    render_error_panel,
)
from src.core.api_client import (
    ApiHTTPError,
    ApiRateLimitError,
    ApiResponseError,
    ApiTimeoutError,
)
from src.core.market_service import (
    InvalidMarketError,
    InvalidSymbolError,
    MarketServiceError,
    SymbolNotFoundError,
)

try:
    import questionary
except ImportError:  # pragma: no cover - exercised in runtime environments only
    questionary = None  # type: ignore[assignment]

OTHER_CHOICE = "Other (Custom Input)"
ACTION_CHOICES = ["Quote", "History"]
MARKET_CHOICES = ["stock", "crypto"]
DEFAULT_STOCK_SYMBOLS = ["NVDA", "AAPL", "MSFT", "SCHD", OTHER_CHOICE]
DEFAULT_CRYPTO_SYMBOLS = ["BTC", "ETH", "XRP", "HYPE", OTHER_CHOICE]
HISTORY_RANGE_CHOICES = ["1d", "7d", "30d", "90d", OTHER_CHOICE]
HISTORY_INTERVAL_CHOICES = ["1d", "1h", OTHER_CHOICE]
HISTORY_LIMIT_CHOICES = ["5", "10", "20", OTHER_CHOICE]


class WizardCancelled(RuntimeError):
    """Raised when user cancels the wizard mid-flow."""


def ask_select(message: str, choices: Sequence[str]) -> str | None:
    """Prompt for a single selection using arrow-key menu navigation."""
    if questionary is None:
        raise RuntimeError("questionary dependency is not installed.")
    return questionary.select(
        message,
        choices=list(choices),
        use_arrow_keys=True,
        instruction="Use arrow keys to move and Enter to confirm.",
    ).ask()


def ask_text(message: str, default: str = "") -> str | None:
    """Prompt for text input and return the response."""
    if questionary is None:
        raise RuntimeError("questionary dependency is not installed.")
    return questionary.text(message, default=default).ask()


def _required_answer(answer: str | None) -> str:
    if answer is None:
        raise WizardCancelled("User cancelled interactive wizard.")
    return answer


def _resolve_symbol(market: str) -> str:
    choices = DEFAULT_STOCK_SYMBOLS if market == "stock" else DEFAULT_CRYPTO_SYMBOLS
    selected = _required_answer(ask_select("Choose a symbol:", choices))
    if selected != OTHER_CHOICE:
        return selected.upper()

    custom_symbol = _required_answer(ask_text("Enter custom symbol:"))
    return custom_symbol.strip().upper()


def _resolve_history_options() -> tuple[str, str, int]:
    range_value = _required_answer(ask_select("Choose a history range:", HISTORY_RANGE_CHOICES))
    if range_value == OTHER_CHOICE:
        range_value = _required_answer(ask_text("Enter custom range (e.g., 14d):", default="7d")).strip()

    interval = _required_answer(ask_select("Choose a history interval:", HISTORY_INTERVAL_CHOICES))
    if interval == OTHER_CHOICE:
        interval = _required_answer(ask_text("Enter custom interval (e.g., 1d):", default="1d")).strip()

    limit_text = _required_answer(ask_select("Choose number of rows to display:", HISTORY_LIMIT_CHOICES))
    if limit_text == OTHER_CHOICE:
        limit_text = _required_answer(ask_text("Enter custom row limit:", default="7")).strip()

    try:
        limit = int(limit_text)
    except ValueError as exc:
        raise InvalidSymbolError("Row limit must be a valid integer.") from exc
    if limit <= 0:
        raise InvalidSymbolError("Row limit must be greater than zero.")

    return range_value, interval, limit


def _exit_with_error(
    *,
    title: str,
    message: str,
    next_step: str,
    debug: bool,
    exc: Exception,
) -> None:
    console = get_console()
    render_error_panel(
        console=console,
        title=title,
        message=message,
        next_step=next_step,
    )
    if debug:
        console.print("[bold yellow]Debug traceback:[/bold yellow]")
        console.print(traceback.format_exc())
    raise typer.Exit(1) from exc


def interactive_command(
    debug: bool = typer.Option(False, "--debug", help="Show traceback for operational errors."),
) -> None:
    """Run an interactive wizard for quote/history requests."""
    console = get_console()
    if questionary is None:
        render_error_panel(
            console=console,
            title="Missing Dependency",
            message="Interactive mode requires 'questionary' to be installed.",
            next_step="Run 'pip install -r requirements.txt' and try again.",
        )
        raise typer.Exit(1)

    console.print(build_wizard_banner())

    service = get_market_service()
    try:
        action = _required_answer(ask_select("Choose an action:", ACTION_CHOICES))
        market = _required_answer(ask_select("Choose a market:", MARKET_CHOICES))
        symbol = _resolve_symbol(market=market)

        if action == "Quote":
            with console.status("[cyan]Fetching quote data...[/cyan]"):
                quote = service.get_quote(symbol=symbol, market=market)
            console.print(build_quote_card(quote))
            return

        range_value, interval, limit = _resolve_history_options()
        with console.status("[cyan]Fetching historical data...[/cyan]"):
            history = service.get_history(
                symbol=symbol,
                market=market,
                range_value=range_value,
                interval=interval,
            )
        console.print(build_history_table(history, limit=limit))
    except WizardCancelled as exc:
        console.print(
            Panel(
                "[bold yellow]Interactive wizard cancelled by user.[/bold yellow]\n"
                "[cyan]No request was sent.[/cyan]",
                title="Cancelled",
                border_style="bold yellow",
            )
        )
        raise typer.Exit(0) from exc
    except InvalidSymbolError as exc:
        _exit_with_error(
            title="Input Error",
            message=f"Invalid symbol/input: {exc}",
            next_step="Adjust your selections and try again.",
            debug=debug,
            exc=exc,
        )
    except InvalidMarketError as exc:
        _exit_with_error(
            title="Input Error",
            message=str(exc),
            next_step="Choose 'stock' or 'crypto'.",
            debug=debug,
            exc=exc,
        )
    except SymbolNotFoundError as exc:
        _exit_with_error(
            title="Symbol Not Found",
            message=str(exc),
            next_step="Try a different symbol.",
            debug=debug,
            exc=exc,
        )
    except ApiRateLimitError as exc:
        if exc.retry_after:
            _exit_with_error(
                title="Rate Limit",
                message=f"Rate limited by provider. Retry after {exc.retry_after} seconds.",
                next_step="Wait before trying again.",
                debug=debug,
                exc=exc,
            )
        _exit_with_error(
            title="Rate Limit",
            message="Rate limited by provider. Try again shortly.",
            next_step="Retry in a moment.",
            debug=debug,
            exc=exc,
        )
    except ApiTimeoutError as exc:
        _exit_with_error(
            title="Timeout",
            message=f"Request timed out: {exc}",
            next_step="Retry or increase timeout settings.",
            debug=debug,
            exc=exc,
        )
    except (ApiHTTPError, ApiResponseError, MarketServiceError) as exc:
        _exit_with_error(
            title="Provider Error",
            message=f"Unable to complete interactive request: {exc}",
            next_step="Retry shortly and verify provider availability.",
            debug=debug,
            exc=exc,
        )
    finally:
        service.close()
