"""Rich rendering helpers for CLI quote/history output."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from src.core.models import HistoryData, QuoteData
from src.utils.formatting import format_currency, format_percentage


def build_quote_table(quote: QuoteData) -> Table:
    """Build a Rich table for quote output."""
    table = Table(title="Quote", header_style="bold cyan")
    table.add_column("Market", style="cyan")
    table.add_column("Symbol", style="cyan")
    table.add_column("Name", style="blue")
    table.add_column("Price", justify="right")
    table.add_column("24h Change", justify="right")

    change_text = Text(format_percentage(quote.change_percent))
    if quote.change_percent is not None:
        if quote.change_percent > 0:
            change_text.stylize("bold green")
        elif quote.change_percent < 0:
            change_text.stylize("bold red")
        else:
            change_text.stylize("cyan")

    table.add_row(
        quote.market,
        quote.symbol,
        quote.name,
        format_currency(quote.price),
        change_text,
    )
    return table


def build_history_table(history: HistoryData, limit: int) -> Table:
    """Build a Rich table for historical price output."""
    table = Table(
        title=f"History ({history.market} | {history.symbol} | {history.interval})",
        header_style="bold cyan",
    )
    table.add_column("Date", style="blue")
    table.add_column("Price", justify="right")

    for point in history.points[-limit:]:
        table.add_row(point.date, format_currency(point.price))

    return table


def render_error_panel(
    console: Console,
    title: str,
    message: str,
    next_step: str,
) -> None:
    """Render an expected operational error as a Rich panel."""
    panel = Panel(
        f"[bold red]{message}[/bold red]\n[cyan]{next_step}[/cyan]",
        title=title,
        border_style="bold red",
    )
    console.print(panel)
