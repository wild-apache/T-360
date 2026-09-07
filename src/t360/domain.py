from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, Field


class Side(StrEnum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(StrEnum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"


class OrderStatus(StrEnum):
    NEW = "NEW"
    OPEN = "OPEN"
    PARTIAL = "PARTIAL"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"


class Tick(BaseModel):
    symbol: str
    timestamp: datetime
    last_price: Decimal
    volume: int | None = None
    bid: Decimal | None = None
    ask: Decimal | None = None


class Candle(BaseModel):
    symbol: str
    timeframe: str
    timestamp: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int = 0


class OrderRequest(BaseModel):
    symbol: str
    side: Side
    quantity: int = Field(gt=0)
    order_type: OrderType
    price: Decimal | None = None
    trigger_price: Decimal | None = None
    tag: str = "t360"


class Order(BaseModel):
    client_order_id: str
    broker_order_id: str | None = None
    request: OrderRequest
    status: OrderStatus
    filled_quantity: int = 0
    average_price: Decimal | None = None
    updated_at: datetime
