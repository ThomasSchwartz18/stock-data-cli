"""Environment-backed application configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


class ConfigError(ValueError):
    """Raised when configuration values are missing or invalid."""


def get_env(name: str, default: str | None = None, required: bool = False) -> str | None:
    """Get an environment variable with optional required enforcement."""
    value = os.getenv(name, default)
    if required and (value is None or value == ""):
        raise ConfigError(f"Missing required environment variable: {name}")
    return value


def _to_float(name: str, raw_value: str, minimum: float = 0.0) -> float:
    try:
        value = float(raw_value)
    except ValueError as exc:
        raise ConfigError(f"Environment variable {name} must be a number.") from exc

    if value < minimum:
        raise ConfigError(f"Environment variable {name} must be >= {minimum}.")
    return value


def _to_int(name: str, raw_value: str, minimum: int = 0) -> int:
    try:
        value = int(raw_value)
    except ValueError as exc:
        raise ConfigError(f"Environment variable {name} must be an integer.") from exc

    if value < minimum:
        raise ConfigError(f"Environment variable {name} must be >= {minimum}.")
    return value


@dataclass(frozen=True)
class AppConfig:
    """Runtime configuration for core API behaviors."""

    request_timeout_seconds: float = 10.0
    max_retries: int = 3
    user_agent: str = "stock-stat-tracker/0.1"
    stock_api_key: str | None = None
    crypto_api_key: str | None = None

    @classmethod
    def from_env(cls) -> "AppConfig":
        """Load environment-backed application configuration."""
        load_dotenv()

        timeout_raw = get_env("REQUEST_TIMEOUT_SECONDS", default="10")
        retries_raw = get_env("MAX_RETRIES", default="3")
        user_agent = get_env("API_USER_AGENT", default="stock-stat-tracker/0.1")

        timeout = _to_float("REQUEST_TIMEOUT_SECONDS", timeout_raw or "10", minimum=0.1)
        max_retries = _to_int("MAX_RETRIES", retries_raw or "3", minimum=0)

        return cls(
            request_timeout_seconds=timeout,
            max_retries=max_retries,
            user_agent=user_agent or "stock-stat-tracker/0.1",
            stock_api_key=get_env("STOCK_API_KEY"),
            crypto_api_key=get_env("CRYPTO_API_KEY"),
        )
