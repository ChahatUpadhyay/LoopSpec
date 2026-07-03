"""Metrics collection for spread, depth, slippage, and fill ratio."""

from typing import List, Dict, Optional
from dataclasses import dataclass, field
from collections import deque
import time
from matching_engine.types import OrderBookState, Trade, Order


@dataclass
class SpreadSnapshot:
    """Snapshot of spread at a point in time."""
    timestamp: float
    spread: float
    bid: float
    ask: float


@dataclass
class DepthSnapshot:
    """Snapshot of order book depth at a point in time."""
    timestamp: float
    bid_depth: int
    ask_depth: int
    total_bid_volume: int
    total_ask_volume: int


@dataclass
class SlippageRecord:
    """Record of slippage for a market order."""
    timestamp: float
    order_id: str
    expected_price: float
    actual_price: float
    slippage_pct: float


@dataclass
class FillRatioRecord:
    """Record of fill ratio for a limit order."""
    timestamp: float
    order_id: str
    total_quantity: int
    filled_quantity: float
    fill_ratio: float


class MetricsTracker:
    """Tracks market metrics including spread, depth, slippage, and fill ratio."""
    
    def __init__(self, max_history: int = 10000):
        """Initialize metrics tracker.
        
        Args:
            max_history: Maximum number of snapshots to keep
        """
        self.max_history = max_history
        
        # Spread history
        self.spread_history: deque = deque(maxlen=max_history)
        
        # Depth history
        self.depth_history: deque = deque(maxlen=max_history)
        
        # Slippage records
        self.slippage_records: List[SlippageRecord] = []
        
        # Fill ratio records
        self.fill_ratio_records: List[FillRatioRecord] = []
        
        # Agent inventory tracking
        self.agent_inventory: Dict[str, int] = {}
    
    def record_spread(self, order_book_state: OrderBookState) -> None:
        """Record current spread.
        
        Args:
            order_book_state: Current order book state
        """
        if order_book_state.best_bid and order_book_state.best_ask:
            spread = order_book_state.best_ask - order_book_state.best_bid
            snapshot = SpreadSnapshot(
                timestamp=order_book_state.timestamp,
                spread=spread,
                bid=order_book_state.best_bid,
                ask=order_book_state.best_ask
            )
            self.spread_history.append(snapshot)
    
    def record_depth(self, order_book_state: OrderBookState) -> None:
        """Record current order book depth.
        
        Args:
            order_book_state: Current order book state
        """
        snapshot = DepthSnapshot(
            timestamp=order_book_state.timestamp,
            bid_depth=order_book_state.bid_depth,
            ask_depth=order_book_state.ask_depth,
            total_bid_volume=order_book_state.total_bid_volume,
            total_ask_volume=order_book_state.total_ask_volume
        )
        self.depth_history.append(snapshot)
    
    def record_slippage(
        self,
        order_id: str,
        expected_price: float,
        actual_price: float
    ) -> None:
        """Record slippage for a market order.
        
        Args:
            order_id: Order identifier
            expected_price: Expected execution price
            actual_price: Actual execution price
        """
        if expected_price > 0:
            slippage_pct = abs(actual_price - expected_price) / expected_price
        else:
            slippage_pct = 0.0
        
        record = SlippageRecord(
            timestamp=time.time(),
            order_id=order_id,
            expected_price=expected_price,
            actual_price=actual_price,
            slippage_pct=slippage_pct
        )
        self.slippage_records.append(record)
    
    def record_fill_ratio(self, order: Order) -> None:
        """Record fill ratio for a limit order.
        
        Args:
            order: Order to record
        """
        if order.quantity > 0:
            fill_ratio = order.filled_quantity / order.quantity
        else:
            fill_ratio = 0.0
        
        record = FillRatioRecord(
            timestamp=time.time(),
            order_id=order.order_id,
            total_quantity=order.quantity,
            filled_quantity=order.filled_quantity,
            fill_ratio=fill_ratio
        )
        self.fill_ratio_records.append(record)
    
    def record_inventory(self, agent_id: str, inventory: int) -> None:
        """Record agent inventory.
        
        Args:
            agent_id: Agent identifier
            inventory: Current inventory
        """
        self.agent_inventory[agent_id] = inventory
    
    def get_average_spread(self) -> Optional[float]:
        """Calculate average spread over history."""
        if not self.spread_history:
            return None
        
        total_spread = sum(s.spread for s in self.spread_history)
        return total_spread / len(self.spread_history)
    
    def get_average_slippage(self) -> Optional[float]:
        """Calculate average slippage percentage."""
        if not self.slippage_records:
            return None
        
        total_slippage = sum(r.slippage_pct for r in self.slippage_records)
        return total_slippage / len(self.slippage_records)
    
    def get_average_fill_ratio(self) -> Optional[float]:
        """Calculate average fill ratio."""
        if not self.fill_ratio_records:
            return None
        
        total_fill_ratio = sum(r.fill_ratio for r in self.fill_ratio_records)
        return total_fill_ratio / len(self.fill_ratio_records)
    
    def get_inventory_risk(self, agent_id: str, price_volatility: float) -> Optional[float]:
        """Calculate inventory risk for an agent.
        
        Args:
            agent_id: Agent identifier
            price_volatility: Current price volatility
            
        Returns:
            Inventory risk metric
        """
        if agent_id not in self.agent_inventory:
            return None
        
        inventory = self.agent_inventory[agent_id]
        # Risk = |inventory| * volatility
        return abs(inventory) * price_volatility
    
    def get_spread_history(self) -> List[SpreadSnapshot]:
        """Get spread history."""
        return list(self.spread_history)
    
    def get_depth_history(self) -> List[DepthSnapshot]:
        """Get depth history."""
        return list(self.depth_history)
    
    def get_slippage_records(self) -> List[SlippageRecord]:
        """Get slippage records."""
        return self.slippage_records
    
    def get_fill_ratio_records(self) -> List[FillRatioRecord]:
        """Get fill ratio records."""
        return self.fill_ratio_records
