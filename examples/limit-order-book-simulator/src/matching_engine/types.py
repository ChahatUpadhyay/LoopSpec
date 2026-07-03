"""Core data structures for the limit order book simulator."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from datetime import datetime
import time


class OrderSide(Enum):
    """Order side (buy or sell)."""
    BUY = "buy"
    SELL = "sell"


class OrderType(Enum):
    """Order type (limit, market, cancel, modify)."""
    LIMIT = "limit"
    MARKET = "market"
    CANCEL = "cancel"
    MODIFY = "modify"


class OrderStatus(Enum):
    """Order status."""
    PENDING = "pending"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


@dataclass
class Order:
    """Represents a single order in the system."""
    order_id: str
    agent_id: str
    side: OrderSide
    order_type: OrderType
    price: float
    quantity: int
    timestamp: float = field(default_factory=time.time)
    status: OrderStatus = OrderStatus.PENDING
    filled_quantity: int = 0
    original_order_id: Optional[str] = None  # For modify orders
    
    @property
    def remaining_quantity(self) -> int:
        """Calculate remaining quantity to fill."""
        return self.quantity - self.filled_quantity
    
    @property
    def is_filled(self) -> bool:
        """Check if order is completely filled."""
        return self.remaining_quantity == 0
    
    def __lt__(self, other: 'Order') -> bool:
        """Compare orders for price-time priority.
        
        For buys: higher price first (max-heap behavior)
        For sells: lower price first (min-heap behavior)
        If same price: earlier timestamp first
        """
        if self.side == OrderSide.BUY:
            # Higher price is better for buys
            if self.price != other.price:
                return self.price > other.price
        else:
            # Lower price is better for sells
            if self.price != other.price:
                return self.price < other.price
        
        # Same price: earlier timestamp first
        return self.timestamp < other.timestamp


@dataclass
class Trade:
    """Represents a completed trade."""
    trade_id: str
    buy_order_id: str
    sell_order_id: str
    price: float
    quantity: int
    timestamp: float = field(default_factory=time.time)
    buy_agent_id: str = ""
    sell_agent_id: str = ""


@dataclass
class Agent:
    """Represents a trading agent."""
    agent_id: str
    agent_type: str
    initial_capital: float = 100000.0
    inventory: int = 0
    cash: float = 100000.0
    
    @property
    def pnl(self) -> float:
        """Calculate current PnL."""
        return self.cash - self.initial_capital
    
    @property
    def position_value(self) -> float:
        """Calculate total position value (cash + inventory at current price)."""
        # This requires current market price, which is tracked elsewhere
        return self.cash  # Simplified for now


@dataclass
class OrderBookState:
    """Snapshot of order book state at a point in time."""
    timestamp: float
    best_bid: float
    best_ask: float
    bid_depth: int
    ask_depth: int
    total_bid_volume: int
    total_ask_volume: int
    
    @property
    def mid_price(self) -> Optional[float]:
        """Calculate mid-price (average of best bid and ask)."""
        if self.best_bid and self.best_ask:
            return (self.best_bid + self.best_ask) / 2
        return None
