from datetime import UTC, datetime
from decimal import Decimal

import pytest

from t360.brokers.base import Broker
from t360.domain import Order, OrderRequest, OrderStatus, OrderType, Side
from t360.execution.engine import ExecutionEngine


class FakeBroker(Broker):
    name = "fake"

    def __init__(self) -> None:
        self.placed: list[OrderRequest] = []
        self.cancelled: list[str] = []

    async def connect(self) -> None:
        pass

    async def disconnect(self) -> None:
        pass

    async def subscribe(self, symbols: list[str]) -> None:
        pass

    async def ticks(self):
        if False:
            yield

    async def place_order(self, request: OrderRequest) -> Order:
        self.placed.append(request)
        return Order(
            client_order_id="client-1",
            broker_order_id="broker-1",
            request=request,
            status=OrderStatus.NEW,
            updated_at=datetime.now(UTC),
        )

    async def cancel_order(self, broker_order_id: str) -> None:
        self.cancelled.append(broker_order_id)

    async def orders(self) -> list[Order]:
        return []

    async def positions(self) -> list[dict]:
        return []


@pytest.mark.asyncio
async def test_execution_engine_delegates_to_broker() -> None:
    broker = FakeBroker()
    engine = ExecutionEngine(broker)
    request = OrderRequest(
        symbol="NSE:TEST",
        side=Side.BUY,
        quantity=1,
        order_type=OrderType.LIMIT,
        price=Decimal("100.00"),
    )

    order = await engine.submit(request)

    assert order.broker_order_id == "broker-1"
    assert broker.placed == [request]


@pytest.mark.asyncio
async def test_execution_engine_delegates_cancel() -> None:
    broker = FakeBroker()
    engine = ExecutionEngine(broker)

    await engine.cancel("broker-1")

    assert broker.cancelled == ["broker-1"]
