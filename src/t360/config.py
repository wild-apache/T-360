from enum import StrEnum

from pydantic_settings import BaseSettings, SettingsConfigDict


class TradingMode(StrEnum):
    BACKTEST = "backtest"
    PAPER = "paper"
    LIVE = "live"


class BrokerName(StrEnum):
    UPSTOX = "upstox"
    FYERS = "fyers"
    ZERODHA = "zerodha"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="T360_", env_file=".env", extra="ignore")

    env: str = "development"
    log_level: str = "INFO"
    trading_mode: TradingMode = TradingMode.BACKTEST
    broker: BrokerName = BrokerName.UPSTOX
    database_url: str = "sqlite:///./t360.db"
    redis_url: str = "redis://localhost:6379/0"
    ai_provider: str | None = None
    ai_model: str | None = None
    ai_api_key: str | None = None


settings = Settings()
