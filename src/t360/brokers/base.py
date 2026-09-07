from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from t360.domain import Order, OrderRequest, Tick


class Broker(ABC):
    """Broker-neutral interface used by the market and execution engines."""

    name: str

    @abstractmethod
    async def connect(self) -> None:
        ...

    @abstractmethod
    async def disconnect(self) -> None:
        ...

    @abstractmethod
    async def subscribe(self, symbols: list[str]) -> None:
        ...

    @abstractmethod
    async def ticks(self) -> AsyncIterator[Tick]:
        ...

    @abstractmethod
    async def place_order(self, request: OrderRequest) -> Order:
        ...

    @abstractmethod
    async def cancel_order(self, broker_order_id: str) -> None:
        ...

    @abstractmethod
    async def orders(self) -> list[Order]:
        ...

    @abstractmethod
    async def positions(self) -> list[dict]:
        ...
