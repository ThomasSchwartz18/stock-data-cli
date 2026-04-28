"""Unit tests for environment-backed config loading."""

from __future__ import annotations

import pytest

from src.utils.config import AppConfig, ConfigError, get_env


def test_get_env_returns_default_when_not_set(monkeypatch: pytest.MonkeyPatch) -> None:
    """Default values should be returned for missing optional env vars."""
    monkeypatch.delenv("MISSING_KEY", raising=False)
    assert get_env("MISSING_KEY", default="fallback") == "fallback"


def test_get_env_raises_for_missing_required(monkeypatch: pytest.MonkeyPatch) -> None:
    """Missing required env vars should raise ConfigError."""
    monkeypatch.delenv("REQUIRED_KEY", raising=False)

    with pytest.raises(ConfigError):
        get_env("REQUIRED_KEY", required=True)


def test_app_config_from_env_reads_values(monkeypatch: pytest.MonkeyPatch) -> None:
    """AppConfig should parse expected values from environment variables."""
    monkeypatch.setenv("REQUEST_TIMEOUT_SECONDS", "15")
    monkeypatch.setenv("MAX_RETRIES", "4")
    monkeypatch.setenv("API_USER_AGENT", "custom-agent/1.0")
    monkeypatch.setenv("STOCK_API_KEY", "stock-key")
    monkeypatch.setenv("CRYPTO_API_KEY", "crypto-key")

    config = AppConfig.from_env()

    assert config.request_timeout_seconds == 15.0
    assert config.max_retries == 4
    assert config.user_agent == "custom-agent/1.0"
    assert config.stock_api_key == "stock-key"
    assert config.crypto_api_key == "crypto-key"


def test_app_config_from_env_rejects_invalid_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    """Invalid numeric env values should raise ConfigError."""
    monkeypatch.setenv("REQUEST_TIMEOUT_SECONDS", "not-a-number")

    with pytest.raises(ConfigError):
        AppConfig.from_env()
