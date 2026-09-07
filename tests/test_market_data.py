from datetime import UTC, datetime, timedelta

from t360.domain import Candle, Tick
from t360.market_data import CandleBuilder, compute_indicators


def tick(symbol: str, offset_seconds: int, price: float, volume: float = 10) -> Tick:
    return Tick(
        symbol=symbol,
        timestamp=datetime(2026, 1, 1, 9, 15, tzinfo=UTC) + timedelta(seconds=offset_seconds),
        last_price=price,
        volume=volume,
    )


def candle(offset_seconds: int, close: float, volume: float = 10) -> Candle:
    timestamp = datetime(2026, 1, 1, 9, 15, tzinfo=UTC) + timedelta(seconds=offset_seconds)
    return Candle(
        symbol="NSE:TEST",
        timeframe="60s",
        timestamp=timestamp,
        open=close - 1,
        high=close + 1,
        low=close - 2,
        close=close,
        volume=volume,
    )


def test_candle_builder_emits_completed_bucket() -> None:
    builder = CandleBuilder(60)
    assert builder.update(tick("NSE:TEST", 0, 100)) is None
    assert builder.update(tick("NSE:TEST", 30, 105)) is None
    completed = builder.update(tick("NSE:TEST", 60, 110))

    assert completed is not None
    assert completed.open == 100
    assert completed.high == 105
    assert completed.low == 100
    assert completed.close == 105


def test_candle_builder_ignores_out_of_order_ticks() -> None:
    builder = CandleBuilder(60)
    builder.update(tick("NSE:TEST", 30, 100))
    assert builder.update(tick("NSE:TEST", 20, 200)) is None
    assert builder.flush("NSE:TEST")[0].close == 100


def test_indicators_are_deterministic() -> None:
    candles = [candle(i * 60, 100 + i) for i in range(20)]
    snapshot = compute_indicators(candles, period=14)

    assert snapshot.sma == 112.5
    assert snapshot.ema is not None
    assert snapshot.rsi == 100.0
    assert snapshot.atr == 3.0
    assert snapshot.vwap is not None


def test_indicator_empty_input() -> None:
    snapshot = compute_indicators([])
    assert snapshot.sma is None
    assert snapshot.ema is None
    assert snapshot.rsi is None
    assert snapshot.atr is None
    assert snapshot.vwap is None
