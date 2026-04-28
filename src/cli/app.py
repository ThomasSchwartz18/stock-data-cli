"""Application entrypoint for the stock and crypto tracker CLI."""

from __future__ import annotations

import typer

from src.cli.commands.market import history_command, quote_command

app = typer.Typer(help="Stock & Crypto CLI Tracker")


@app.callback()
def cli() -> None:
    """Stock & Crypto CLI Tracker command group."""
    return None


@app.command()
def ping() -> None:
    """Basic health command used to verify CLI wiring."""
    typer.echo("pong")


app.command(name="quote")(quote_command)
app.command(name="history")(history_command)


def run() -> None:
    """Run the Typer application."""
    app()


if __name__ == "__main__":
    run()
