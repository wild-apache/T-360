from datetime import UTC, datetime
from decimal import Decimal

from t360.domain import OrderRequest, OrderType, Side, Tick


def test_order_request_validation() -> None:
    order = OrderRequest(
        symbol="NSE:RELIANCE-EQ",
        side=Side.BUY,
        quantity=1,
        order_type=OrderType.MARKET,
    )
    assert order.quantity == 1


def test_tick_model() -> None:
    tick = Tick(
        symbol="NSE:RELIANCE-EQ",
        timestamp=datetime.now(UTC),
        last_price=Decimal("100.50"),
    )
    assert tick.last_price == Decimal("100.50")
