"""CLI tests for the baseline Typer application."""

from __future__ import annotations

from dataclasses import dataclass

import pytest
from typer.testing import CliRunner

from src.cli.commands import market as market_commands
from src.cli.app import app
from src.core.api_client import ApiRateLimitError
from src.core.market_service import InvalidSymbolError
from src.core.models import HistoryData, HistoryPoint, QuoteData

runner = CliRunner()


def _combined_output(result: object) -> str:
    stderr = ""
    stderr_bytes = getattr(result, "stderr_bytes", None)
    if stderr_bytes:
        stderr = stderr_bytes.decode()
    return getattr(result, "output", "") + getattr(result, "stdout", "") + stderr


def test_ping_command_returns_pong() -> None:
    """The baseline health command should print pong and exit cleanly."""
    result = runner.invoke(app, ["ping"])
    assert result.exit_code == 0
    assert "pong" in result.stdout


def test_help_output_includes_app_description() -> None:
    """Root help should include project-level description text."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Stock & Crypto CLI Tracker" in result.stdout


def test_invalid_command_returns_non_zero_exit() -> None:
    """Unknown commands should fail with a usage hint."""
    result = runner.invoke(app, ["not-a-command"])
    assert result.exit_code != 0
    output = _combined_output(result)
    assert "No such command" in output or "Got unexpected extra argument" in output


@dataclass
class _FakeMarketService:
    quote_value: QuoteData | None = None
    history_value: HistoryData | None = None
    quote_error: Exception | None = None
    history_error: Exception | None = None
    closed: bool = False

    def close(self) -> None:
        self.closed = True

    def get_quote(self, symbol: str, market: str) -> QuoteData:
        assert symbol
        assert market
        if self.quote_error:
            raise self.quote_error
        assert self.quote_value is not None
        return self.quote_value

    def get_history(
        self,
        symbol: str,
        market: str,
        range_value: str = "7d",
        interval: str = "1d",
    ) -> HistoryData:
        assert symbol
        assert market
        assert range_value
        assert interval
        if self.history_error:
            raise self.history_error
        assert self.history_value is not None
        return self.history_value


def test_quote_command_success(monkeypatch: pytest.MonkeyPatch) -> None:
    """Quote command should render normalized quote details."""
    fake_service = _FakeMarketService(
        quote_value=QuoteData(
            market="stock",
            symbol="AAPL",
            name="Apple Inc.",
            price=182.55,
            currency="USD",
            change_percent=1.1,
        )
    )
    monkeypatch.setattr(market_commands, "get_market_service", lambda: fake_service)

    result = runner.invoke(app, ["quote", "AAPL", "--market", "stock"])

    assert result.exit_code == 0
    output = _combined_output(result)
    assert "Quote" in output
    assert "AAPL" in output
    assert "$182.55" in output
    assert "+1.10%" in output
    assert fake_service.closed is True


def test_history_command_success(monkeypatch: pytest.MonkeyPatch) -> None:
    """History command should render recent historical rows."""
    fake_service = _FakeMarketService(
        history_value=HistoryData(
            market="crypto",
            symbol="BTC",
            name="bitcoin",
            currency="USD",
            interval="1d",
            points=[
                HistoryPoint(date="2026-04-25", price=93000.0),
                HistoryPoint(date="2026-04-26", price=94000.0),
                HistoryPoint(date="2026-04-27", price=95000.0),
            ],
        )
    )
    monkeypatch.setattr(market_commands, "get_market_service", lambda: fake_service)

    result = runner.invoke(
        app,
        ["history", "BTC", "--market", "crypto", "--range", "7d", "--interval", "1d", "--limit", "2"],
    )

    assert result.exit_code == 0
    output = _combined_output(result)
    assert "History (crypto | BTC | 1d)" in output
    assert "2026-04-26" in output
    assert "$94,000.00" in output
    assert "2026-04-27" in output
    assert "$95,000.00" in output
    assert fake_service.closed is True


def test_quote_command_invalid_symbol(monkeypatch: pytest.MonkeyPatch) -> None:
    """Invalid symbol errors should return non-zero and user-facing output."""
    fake_service = _FakeMarketService(
        quote_error=InvalidSymbolError("bad input"),
    )
    monkeypatch.setattr(market_commands, "get_market_service", lambda: fake_service)

    result = runner.invoke(app, ["quote", "bad!!", "--market", "stock"])

    assert result.exit_code == 1
    output = _combined_output(result)
    assert "Input Error" in output
    assert "Invalid symbol" in output


def test_history_command_rate_limited(monkeypatch: pytest.MonkeyPatch) -> None:
    """Rate limit errors should return non-zero with retry guidance."""
    fake_service = _FakeMarketService(
        history_error=ApiRateLimitError("too many requests", retry_after="30"),
    )
    monkeypatch.setattr(market_commands, "get_market_service", lambda: fake_service)

    result = runner.invoke(app, ["history", "AAPL", "--market", "stock"])

    assert result.exit_code == 1
    output = _combined_output(result)
    assert "Rate Limit" in output
    assert "Retry after 30 seconds" in output
