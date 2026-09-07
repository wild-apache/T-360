from dataclasses import dataclass
from itertools import pairwise

from t360.domain import Candle


@dataclass(frozen=True, slots=True)
class IndicatorSnapshot:
    sma: float | None = None
    ema: float | None = None
    rsi: float | None = None
    atr: float | None = None
    vwap: float | None = None


def compute_indicators(candles: list[Candle], period: int = 14) -> IndicatorSnapshot:
    """Compute deterministic indicators from chronological candles."""
    if period <= 0:
        raise ValueError("period must be positive")
    if not candles:
        return IndicatorSnapshot()

    ordered = sorted(candles, key=lambda candle: candle.timestamp)
    closes = [float(c.close) for c in ordered]
    sma = sum(closes[-period:]) / min(period, len(closes))
    ema = _ema(closes, period)
    rsi = _rsi(closes, period)
    atr = _atr(ordered, period)
    vwap = _vwap(ordered)
    return IndicatorSnapshot(sma=sma, ema=ema, rsi=rsi, atr=atr, vwap=vwap)


def _ema(values: list[float], period: int) -> float | None:
    if not values:
        return None
    alpha = 2.0 / (period + 1)
    result = values[0]
    for value in values[1:]:
        result = alpha * value + (1.0 - alpha) * result
    return result


def _rsi(values: list[float], period: int) -> float | None:
    if len(values) < 2:
        return None
    deltas = [curr - prev for prev, curr in pairwise(values)]
    window = deltas[-period:]
    gains = sum(max(delta, 0.0) for delta in window) / len(window)
    losses = sum(max(-delta, 0.0) for delta in window) / len(window)
    if losses == 0:
        return 100.0 if gains > 0 else 50.0
    return 100.0 - (100.0 / (1.0 + gains / losses))


def _atr(candles: list[Candle], period: int) -> float | None:
    if not candles:
        return None
    true_ranges: list[float] = []
    previous_close: float | None = None
    for candle in candles:
        high = float(candle.high)
        low = float(candle.low)
        close = float(candle.close)
        if previous_close is None:
            true_range = high - low
        else:
            true_range = max(high - low, abs(high - previous_close), abs(low - previous_close))
        true_ranges.append(true_range)
        previous_close = close
    return sum(true_ranges[-period:]) / min(period, len(true_ranges))


def _vwap(candles: list[Candle]) -> float | None:
    total_volume = sum(max(c.volume, 0) for c in candles)
    if total_volume == 0:
        return None
    weighted = sum(
        ((float(c.high) + float(c.low) + float(c.close)) / 3.0) * max(c.volume, 0)
        for c in candles
    )
    return weighted / total_volume
