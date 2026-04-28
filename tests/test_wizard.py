"""Tests for interactive wizard command flow."""

from __future__ import annotations

from dataclasses import dataclass

import pytest
from typer.testing import CliRunner

from src.cli.app import app
from src.cli import wizard
from src.core.models import HistoryData, HistoryPoint, QuoteData

runner = CliRunner()


def _combined_output(result: object) -> str:
    stderr = ""
    stderr_bytes = getattr(result, "stderr_bytes", None)
    if stderr_bytes:
        stderr = stderr_bytes.decode()
    return getattr(result, "output", "") + getattr(result, "stdout", "") + stderr


@dataclass
class _FakeMarketService:
    quote_value: QuoteData | None = None
    history_value: HistoryData | None = None
    quote_called_with: tuple[str, str] | None = None
    history_called_with: tuple[str, str, str, str] | None = None
    closed: bool = False

    def close(self) -> None:
        self.closed = True

    def get_quote(self, symbol: str, market: str) -> QuoteData:
        self.quote_called_with = (symbol, market)
        assert self.quote_value is not None
        return self.quote_value

    def get_history(
        self,
        symbol: str,
        market: str,
        range_value: str = "7d",
        interval: str = "1d",
    ) -> HistoryData:
        self.history_called_with = (symbol, market, range_value, interval)
        assert self.history_value is not None
        return self.history_value


def test_interactive_quote_default_flow(monkeypatch: pytest.MonkeyPatch) -> None:
    """Interactive wizard should fetch quote for default arrow-key selections."""
    fake_service = _FakeMarketService(
        quote_value=QuoteData(
            market="stock",
            symbol="AAPL",
            name="Apple Inc.",
            price=190.12,
            change_percent=0.5,
        )
    )
    select_answers = iter(["Quote", "stock", "AAPL"])
    monkeypatch.setattr(wizard, "questionary", object())
    monkeypatch.setattr(wizard, "ask_select", lambda _message, _choices: next(select_answers))
    monkeypatch.setattr(wizard, "get_market_service", lambda: fake_service)

    result = runner.invoke(app, ["interactive"])

    assert result.exit_code == 0
    output = _combined_output(result)
    assert "Quote" in output
    assert "AAPL" in output
    assert "$190.12" in output
    assert fake_service.quote_called_with == ("AAPL", "stock")
    assert fake_service.closed is True


def test_interactive_history_other_prompts(monkeypatch: pytest.MonkeyPatch) -> None:
    """Selecting Other should prompt for custom symbol/timeframe inputs."""
    fake_service = _FakeMarketService(
        history_value=HistoryData(
            market="crypto",
            symbol="HYPE",
            name="hype-token",
            currency="USD",
            interval="1d",
            points=[
                HistoryPoint(date="2026-04-26", price=1.11),
                HistoryPoint(date="2026-04-27", price=1.22),
                HistoryPoint(date="2026-04-28", price=1.33),
            ],
        )
    )
    select_answers = iter(
        [
            "History",
            "crypto",
            wizard.OTHER_CHOICE,
            wizard.OTHER_CHOICE,
            wizard.OTHER_CHOICE,
            wizard.OTHER_CHOICE,
        ]
    )
    text_answers = iter(["hype", "14d", "1d", "2"])

    monkeypatch.setattr(wizard, "questionary", object())
    monkeypatch.setattr(wizard, "ask_select", lambda _message, _choices: next(select_answers))
    monkeypatch.setattr(wizard, "ask_text", lambda _message, default="": next(text_answers))
    monkeypatch.setattr(wizard, "get_market_service", lambda: fake_service)

    result = runner.invoke(app, ["interactive"])

    assert result.exit_code == 0
    output = _combined_output(result)
    assert "History (crypto | HYPE" in output
    assert "| 1d)" in output
    assert "$1.22" in output
    assert "$1.33" in output
    assert fake_service.history_called_with == ("HYPE", "crypto", "14d", "1d")
    assert fake_service.closed is True


def test_interactive_ctrl_c_safe_exit(monkeypatch: pytest.MonkeyPatch) -> None:
    """Wizard should safely exit when prompt returns None (Ctrl+C behavior)."""
    fake_service = _FakeMarketService(
        quote_value=QuoteData(
            market="stock",
            symbol="AAPL",
            name="Apple Inc.",
            price=190.12,
            change_percent=0.5,
        )
    )

    monkeypatch.setattr(wizard, "questionary", object())
    monkeypatch.setattr(wizard, "ask_select", lambda _message, _choices: None)
    monkeypatch.setattr(wizard, "get_market_service", lambda: fake_service)

    result = runner.invoke(app, ["interactive"])

    assert result.exit_code == 0
    output = _combined_output(result)
    assert "Cancelled" in output
    assert "Interactive wizard cancelled by user" in output
    assert fake_service.closed is True
