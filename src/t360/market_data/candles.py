from collections import OrderedDict
from datetime import datetime, timedelta, timezone

from t360.domain import Candle, Tick


class CandleBuilder:
    """Build fixed-time OHLCV candles from ordered ticks."""

    def __init__(self, timeframe_seconds: int = 60) -> None:
        if timeframe_seconds <= 0:
            raise ValueError("timeframe_seconds must be positive")
        self.timeframe_seconds = timeframe_seconds
        self._active: dict[str, Candle] = {}
        self._last_timestamp: dict[str, datetime] = {}
        self._history: dict[str, OrderedDict[datetime, Candle]] = {}

    def update(self, tick: Tick) -> Candle | None:
        timestamp = self._normalize_timestamp(tick.timestamp)
        if timestamp < self._last_timestamp.get(tick.symbol, timestamp):
            return None
        self._last_timestamp[tick.symbol] = timestamp
        bucket = self._bucket_start(timestamp)
        current = self._active.get(tick.symbol)

        if current is None:
            self._active[tick.symbol] = self._new_candle(tick, bucket)
            return None

        if bucket == current.timestamp:
            self._active[tick.symbol] = self._extend(current, tick)
            return None

        completed = current
        self._store(completed)
        self._active[tick.symbol] = self._new_candle(tick, bucket)
        return completed

    def flush(self, symbol: str | None = None) -> list[Candle]:
        symbols = [symbol] if symbol else list(self._active)
        completed: list[Candle] = []
        for item in symbols:
            candle = self._active.pop(item, None)
            if candle is not None:
                self._store(candle)
                completed.append(candle)
        return completed

    def history(self, symbol: str, limit: int = 200) -> list[Candle]:
        if limit <= 0:
            return []
        values = list(self._history.get(symbol, {}).values())
        return values[-limit:]

    def _store(self, candle: Candle) -> None:
        history = self._history.setdefault(candle.symbol, OrderedDict())
        history[candle.timestamp] = candle
        while len(history) > 5000:
            history.popitem(last=False)

    def _bucket_start(self, timestamp: datetime) -> datetime:
        epoch = int(timestamp.timestamp())
        bucket = epoch - epoch % self.timeframe_seconds
        return datetime.fromtimestamp(bucket, tz=timezone.utc)

    @staticmethod
    def _normalize_timestamp(timestamp: datetime) -> datetime:
        if timestamp.tzinfo is None:
            return timestamp.replace(tzinfo=timezone.utc)
        return timestamp.astimezone(timezone.utc)

    def _new_candle(self, tick: Tick, bucket: datetime) -> Candle:
        return Candle(
            symbol=tick.symbol,
            timeframe=f"{self.timeframe_seconds}s",
            timestamp=bucket,
            open=tick.last_price,
            high=tick.last_price,
            low=tick.last_price,
            close=tick.last_price,
            volume=tick.volume,
        )

    @staticmethod
    def _extend(candle: Candle, tick: Tick) -> Candle:
        return candle.model_copy(
            update={
                "high": max(candle.high, tick.last_price),
                "low": min(candle.low, tick.last_price),
                "close": tick.last_price,
                "volume": max(candle.volume, tick.volume),
            }
        )
