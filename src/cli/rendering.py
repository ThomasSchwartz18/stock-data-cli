"""Rich rendering helpers for CLI quote/history output."""

from __future__ import annotations

from rich.columns import Columns
from rich.console import Console
from rich.console import Group
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from src.core.models import HistoryData, QuoteData
from src.utils.formatting import (
    format_currency,
    format_percentage,
    trend_arrow,
    trend_word,
)

SPARK_CHARS = "▁▂▃▄▅▆▇█"


def _trend_style(value: float | int | None) -> str:
    if value is None:
        return "cyan"
    numeric = float(value)
    if numeric > 0:
        return "bold green"
    if numeric < 0:
        return "bold red"
    return "cyan"


def generate_sparkline(values: list[float | int]) -> str:
    """Generate a unicode sparkline for a series of numeric values."""
    if not values:
        return "N/A"
    if len(values) == 1:
        return SPARK_CHARS[-1]

    minimum = min(values)
    maximum = max(values)
    if minimum == maximum:
        return SPARK_CHARS[0] * len(values)

    span = maximum - minimum
    bars: list[str] = []
    for value in values:
        normalized = (value - minimum) / span
        index = round(normalized * (len(SPARK_CHARS) - 1))
        bars.append(SPARK_CHARS[index])
    return "".join(bars)


def _scale_sparkline(sparkline: str, scale: int = 3) -> str:
    """Scale sparkline width by repeating each glyph."""
    if not sparkline or sparkline == "N/A":
        return sparkline
    return "".join(char * scale for char in sparkline)


def build_quote_card(quote: QuoteData) -> Panel:
    """Build a panel-based dashboard card for quote output."""
    trend_style = _trend_style(quote.change_percent)
    change_text = Text(format_percentage(quote.change_percent, with_arrow=True), style=trend_style)
    trend_text = Text(f"{trend_arrow(quote.change_percent)} {trend_word(quote.change_percent)}", style=trend_style)

    meta_table = Table.grid(padding=(0, 2))
    meta_table.add_column(style="cyan")
    meta_table.add_column(style="white")
    meta_table.add_row("Symbol", quote.symbol)
    meta_table.add_row("Name", quote.name)
    meta_table.add_row("Market", quote.market.upper())
    meta_table.add_row("24h", change_text)
    meta_table.add_row("Trend", trend_text)

    price_panel = Panel(
        Text(format_currency(quote.price), justify="center", style="bold white"),
        title="Last Price",
        border_style="cyan",
        padding=(1, 4),
    )

    content = Columns(
        [
            Panel(meta_table, border_style="blue", title="Snapshot"),
            price_panel,
        ],
        equal=True,
        expand=True,
    )

    return Panel(
        Padding(content, (0, 1)),
        title=f"{quote.market.title()} Dashboard",
        border_style=trend_style,
    )


def build_history_table(history: HistoryData, limit: int) -> Panel:
    """Build a Rich panel with history table and a large right-side trendline."""
    points = history.points[-limit:]
    values = [point.price for point in points]
    sparkline = generate_sparkline(values)
    scaled_sparkline = _scale_sparkline(sparkline, scale=3)

    table = Table(
        title=f"History ({history.market} | {history.symbol} | {history.interval})",
        header_style="bold cyan",
    )
    table.add_column("Date", style="blue")
    table.add_column("Price", justify="right")
    table.add_column("Trend", justify="center")

    previous: float | None = None
    for point in points:
        delta = None if previous is None else point.price - previous
        trend = Text(trend_arrow(delta), style=_trend_style(delta))
        table.add_row(point.date, format_currency(point.price), trend)
        previous = point.price

    sparkline_style = "bold green" if values and values[-1] >= values[0] else "bold red"
    sparkline_text = Text(scaled_sparkline, style=sparkline_style, justify="center")
    trend_meta = Text.assemble(
        ("Start: ", "cyan"),
        (format_currency(values[0]) if values else "N/A", "white"),
        ("  End: ", "cyan"),
        (format_currency(values[-1]) if values else "N/A", "white"),
    )
    trend_panel = Panel(
        Group(sparkline_text, Text(" ", style="white"), trend_meta),
        title="Trendline",
        border_style="cyan",
        padding=(1, 1),
    )

    layout = Columns(
        [Panel(table, border_style="blue"), trend_panel],
        expand=True,
        equal=False,
    )
    return Panel(layout, title="Price Action", border_style="blue")


def build_wizard_banner() -> Panel:
    """Build ASCII banner shown at interactive wizard startup."""
    title = Text("Stock Tracker", style="bold cyan", justify="center")
    subtitle = Text("Interactive Wizard • Guided Market Lookup", style="bold blue", justify="center")
    hint = Text("Use arrow keys and Enter to continue", style="cyan", justify="center")
    return Panel(Group(title, subtitle, hint), border_style="cyan", title="Welcome")


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
