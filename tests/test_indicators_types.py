from datetime import UTC, datetime

from t360.domain import Candle
from t360.market_data import compute_indicators


def test_indicator_snapshot_uses_float_values_for_decimal_candles() -> None:
    candle = Candle(
        symbol="NSE:TEST",
        timeframe="60s",
        timestamp=datetime(2026, 1, 1, 9, 15, tzinfo=UTC),
        open="100.10",
        high="101.10",
        low="99.10",
        close="100.10",
        volume=100,
    )

    snapshot = compute_indicators([candle])

    assert snapshot.sma == 100.10
    assert isinstance(snapshot.sma, float)
    assert snapshot.atr == 2.0
    assert snapshot.vwap == 100.1
