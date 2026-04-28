"""Quote and history CLI commands."""

from __future__ import annotations

import typer

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
from src.utils.formatting import format_currency, format_percentage


def get_market_service() -> MarketService:
    """Create the market service for command execution."""
    return MarketService()


def quote_command(
    symbol: str = typer.Argument(..., help="Ticker or symbol to query."),
    market: str = typer.Option(
        "stock",
        "--market",
        "-m",
        help="Market type: stock or crypto.",
    ),
) -> None:
    """Fetch and print the latest quote for a stock or crypto symbol."""
    service = get_market_service()
    try:
        quote = service.get_quote(symbol=symbol, market=market)
    except InvalidSymbolError as exc:
        typer.echo(f"Invalid symbol: {exc}", err=True)
        raise typer.Exit(1) from exc
    except InvalidMarketError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(1) from exc
    except SymbolNotFoundError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(1) from exc
    except ApiRateLimitError as exc:
        if exc.retry_after:
            typer.echo(
                f"Rate limited by provider. Retry after {exc.retry_after} seconds.",
                err=True,
            )
        else:
            typer.echo("Rate limited by provider. Try again shortly.", err=True)
        raise typer.Exit(1) from exc
    except ApiTimeoutError as exc:
        typer.echo(f"Request timed out: {exc}", err=True)
        raise typer.Exit(1) from exc
    except (ApiHTTPError, ApiResponseError, MarketServiceError) as exc:
        typer.echo(f"Unable to fetch quote: {exc}", err=True)
        raise typer.Exit(1) from exc
    finally:
        service.close()

    typer.echo(f"Market: {quote.market}")
    typer.echo(f"Symbol: {quote.symbol}")
    typer.echo(f"Name: {quote.name}")
    typer.echo(f"Price: {format_currency(quote.price)}")
    typer.echo(f"24h Change: {format_percentage(quote.change_percent)}")


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
) -> None:
    """Fetch and print recent historical prices."""
    service = get_market_service()
    try:
        history = service.get_history(
            symbol=symbol,
            market=market,
            range_value=range_value,
            interval=interval,
        )
    except InvalidSymbolError as exc:
        typer.echo(f"Invalid symbol: {exc}", err=True)
        raise typer.Exit(1) from exc
    except InvalidMarketError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(1) from exc
    except SymbolNotFoundError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(1) from exc
    except ApiRateLimitError as exc:
        if exc.retry_after:
            typer.echo(
                f"Rate limited by provider. Retry after {exc.retry_after} seconds.",
                err=True,
            )
        else:
            typer.echo("Rate limited by provider. Try again shortly.", err=True)
        raise typer.Exit(1) from exc
    except ApiTimeoutError as exc:
        typer.echo(f"Request timed out: {exc}", err=True)
        raise typer.Exit(1) from exc
    except (ApiHTTPError, ApiResponseError, MarketServiceError) as exc:
        typer.echo(f"Unable to fetch history: {exc}", err=True)
        raise typer.Exit(1) from exc
    finally:
        service.close()

    points_to_show = history.points[-limit:]
    typer.echo(f"Market: {history.market}")
    typer.echo(f"Symbol: {history.symbol}")
    typer.echo(f"Interval: {history.interval}")
    typer.echo("History:")
    for point in points_to_show:
        typer.echo(f"- {point.date}: {format_currency(point.price)}")
