from t360.brokers.base import Broker
from t360.domain import Order


class ExecutionEngine:
    """Deterministic execution boundary. AI never calls a broker directly."""

    def __init__(self, broker: Broker) -> None:
        self.broker = broker

    async def submit(self, order_request) -> Order:
        return await self.broker.place_order(order_request)

    async def cancel(self, broker_order_id: str) -> None:
        await self.broker.cancel_order(broker_order_id)
