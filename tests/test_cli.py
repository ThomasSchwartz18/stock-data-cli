"""CLI tests for the baseline Typer application."""

from __future__ import annotations

from typer.testing import CliRunner

from src.cli.app import app

runner = CliRunner()


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
    assert "No such command" in result.stdout
