from abc import ABC, abstractmethod

from t360.domain import Candle, OrderRequest


class Strategy(ABC):
    """Pure strategy contract: market inputs in, intents out."""

    name: str

    @abstractmethod
    def on_candle(self, candle: Candle) -> list[OrderRequest]:
        ...
