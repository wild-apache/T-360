from t360.config import BrokerName, Settings, TradingMode


def test_default_settings_are_backtest_and_upstox() -> None:
    settings = Settings()
    assert settings.trading_mode is TradingMode.BACKTEST
    assert settings.broker is BrokerName.UPSTOX


def test_settings_read_t360_environment(monkeypatch) -> None:
    monkeypatch.setenv("T360_TRADING_MODE", "paper")
    monkeypatch.setenv("T360_BROKER", "fyers")

    settings = Settings()

    assert settings.trading_mode is TradingMode.PAPER
    assert settings.broker is BrokerName.FYERS
