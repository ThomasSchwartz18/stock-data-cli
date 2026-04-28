"""Quote and history CLI commands."""

from __future__ import annotations

import traceback

import typer
from rich.console import Console

from src.cli.rendering import build_history_table, build_quote_table, render_error_panel
from src.core.api_client import (
    ApiHTTPError,
    ApiRateLimitError,
    ApiResponseError,
    ApiTimeoutError,
)
from src.core.market_service import (
    InvalidMarketError,
    InvalidSymbolError,
    MarketService,
    MarketServiceError,
    SymbolNotFoundError,
)


def get_market_service() -> MarketService:
    """Create the market service for command execution."""
    return MarketService()


def get_console() -> Console:
    """Create the Rich console for user-facing output."""
    return Console()


def _exit_with_error(
    *,
    console: Console,
    title: str,
    message: str,
    next_step: str,
    debug: bool,
    exc: Exception,
) -> None:
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


def quote_command(
    symbol: str = typer.Argument(..., help="Ticker or symbol to query."),
    market: str = typer.Option(
        "stock",
        "--market",
        "-m",
        help="Market type: stock or crypto.",
    ),
    debug: bool = typer.Option(False, "--debug", help="Show traceback for operational errors."),
) -> None:
    """Fetch and print the latest quote for a stock or crypto symbol."""
    console = get_console()
    service = get_market_service()
    try:
        with console.status("[cyan]Fetching quote data...[/cyan]"):
            quote = service.get_quote(symbol=symbol, market=market)
    except InvalidSymbolError as exc:
        _exit_with_error(
            console=console,
            title="Input Error",
            message=f"Invalid symbol: {exc}",
            next_step="Check symbol format and try again.",
            debug=debug,
            exc=exc,
        )
    except InvalidMarketError as exc:
        _exit_with_error(
            console=console,
            title="Input Error",
            message=str(exc),
            next_step="Use '--market stock' or '--market crypto'.",
            debug=debug,
            exc=exc,
        )
    except SymbolNotFoundError as exc:
        _exit_with_error(
            console=console,
            title="Symbol Not Found",
            message=str(exc),
            next_step="Verify the ticker/symbol and retry.",
            debug=debug,
            exc=exc,
        )
    except ApiRateLimitError as exc:
        if exc.retry_after:
            _exit_with_error(
                console=console,
                title="Rate Limit",
                message=f"Rate limited by provider. Retry after {exc.retry_after} seconds.",
                next_step="Wait and retry the command.",
                debug=debug,
                exc=exc,
            )
        else:
            _exit_with_error(
                console=console,
                title="Rate Limit",
                message="Rate limited by provider. Try again shortly.",
                next_step="Retry in a moment.",
                debug=debug,
                exc=exc,
            )
    except ApiTimeoutError as exc:
        _exit_with_error(
            console=console,
            title="Timeout",
            message=f"Request timed out: {exc}",
            next_step="Retry the command or increase timeout configuration.",
            debug=debug,
            exc=exc,
        )
    except (ApiHTTPError, ApiResponseError, MarketServiceError) as exc:
        _exit_with_error(
            console=console,
            title="Provider Error",
            message=f"Unable to fetch quote: {exc}",
            next_step="Retry shortly. If this persists, provider payload/availability may have changed.",
            debug=debug,
            exc=exc,
        )
    finally:
        service.close()

    console.print(build_quote_table(quote))


def history_command(
    symbol: str = typer.Argument(..., help="Ticker or symbol to query."),
    market: str = typer.Option(
        "stock",
        "--market",
        "-m",
        help="Market type: stock or crypto.",
    ),
    range_value: str = typer.Option("7d", "--range", help="Range for historical data, e.g. 7d."),
    interval: str = typer.Option("1d", "--interval", help="Data interval, e.g. 1d."),
    limit: int = typer.Option(7, "--limit", min=1, help="Number of rows to print."),
    debug: bool = typer.Option(False, "--debug", help="Show traceback for operational errors."),
) -> None:
    """Fetch and print recent historical prices."""
    console = get_console()
    service = get_market_service()
    try:
        with console.status("[cyan]Fetching historical data...[/cyan]"):
            history = service.get_history(
                symbol=symbol,
                market=market,
                range_value=range_value,
                interval=interval,
            )
    except InvalidSymbolError as exc:
        _exit_with_error(
            console=console,
            title="Input Error",
            message=f"Invalid symbol: {exc}",
            next_step="Check symbol format and try again.",
            debug=debug,
            exc=exc,
        )
    except InvalidMarketError as exc:
        _exit_with_error(
            console=console,
            title="Input Error",
            message=str(exc),
            next_step="Use '--market stock' or '--market crypto'.",
            debug=debug,
            exc=exc,
        )
    except SymbolNotFoundError as exc:
        _exit_with_error(
            console=console,
            title="Symbol Not Found",
            message=str(exc),
            next_step="Verify the ticker/symbol and retry.",
            debug=debug,
            exc=exc,
        )
    except ApiRateLimitError as exc:
        if exc.retry_after:
            _exit_with_error(
                console=console,
                title="Rate Limit",
                message=f"Rate limited by provider. Retry after {exc.retry_after} seconds.",
                next_step="Wait and retry the command.",
                debug=debug,
                exc=exc,
            )
        else:
            _exit_with_error(
                console=console,
                title="Rate Limit",
                message="Rate limited by provider. Try again shortly.",
                next_step="Retry in a moment.",
                debug=debug,
                exc=exc,
            )
    except ApiTimeoutError as exc:
        _exit_with_error(
            console=console,
            title="Timeout",
            message=f"Request timed out: {exc}",
            next_step="Retry the command or increase timeout configuration.",
            debug=debug,
            exc=exc,
        )
    except (ApiHTTPError, ApiResponseError, MarketServiceError) as exc:
        _exit_with_error(
            console=console,
            title="Provider Error",
            message=f"Unable to fetch history: {exc}",
            next_step="Retry shortly. If this persists, provider payload/availability may have changed.",
            debug=debug,
            exc=exc,
        )
    finally:
        service.close()

    console.print(build_history_table(history, limit=limit))
