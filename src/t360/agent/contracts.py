from typing import Literal

from pydantic import BaseModel, Field


class TradingDecision(BaseModel):
    """Structured output expected from the AI decision layer."""

    action: Literal["BUY", "SELL", "HOLD"]
    symbol: str
    quantity: int = Field(default=0, ge=0)
    order_type: Literal["MARKET", "LIMIT"] | None = None
    entry_price: float | None = None
    thesis: str


class MarketSnapshot(BaseModel):
    symbol: str
    last_price: float
    timeframe: str
    indicators: dict[str, float] = Field(default_factory=dict)
    context: dict[str, str | float | int] = Field(default_factory=dict)
