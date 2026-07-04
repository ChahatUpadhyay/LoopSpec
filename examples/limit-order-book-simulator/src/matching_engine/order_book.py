"""Order book implementation with price-time priority."""

import heapq
from collections import defaultdict, deque
from typing import Dict, List, Optional, Tuple
from .types import Order, OrderSide, OrderBookState, Trade
import time


class OrderBook:
    """Limit order book with bid/ask queues and price-time priority."""
    
    def __init__(self):
        """Initialize empty order book."""
        # Bids: max-heap (use negative prices for max-heap behavior in heapq)
        self.bids: Dict[float, deque] = defaultdict(deque)  # price -> queue of orders
        self.bid_prices: List[float] = []  # max-heap of prices
        
        # Asks: min-heap
        self.asks: Dict[float, deque] = defaultdict(deque)  # price -> queue of orders
        self.ask_prices: List[float] = []  # min-heap of prices
        
        # Order tracking
        self.orders: Dict[str, Order] = {}  # order_id -> Order
        
        # Trade tracking
        self.trades: List[Trade] = []
    
    def add_order(self, order: Order) -> None:
        """Add order to the book."""
        self.orders[order.order_id] = order
        
        if order.side == OrderSide.BUY:
            # Add to bids (use negative price for max-heap)
            heapq.heappush(self.bid_prices, -order.price)
            self.bids[order.price].append(order)
        else:
            # Add to asks
            heapq.heappush(self.ask_prices, order.price)
            self.asks[order.price].append(order)
    
    def remove_order(self, order_id: str) -> Optional[Order]:
        """Remove order from the book."""
        if order_id not in self.orders:
            return None
        
        order = self.orders[order_id]
        del self.orders[order_id]
        
        # Remove from price queue
        if order.side == OrderSide.BUY:
            queue = self.bids[order.price]
            # Mark as cancelled in queue (lazy removal)
            for i, o in enumerate(queue):
                if o.order_id == order_id:
                    queue[i] = None
                    break
        else:
            queue = self.asks[order.price]
            for i, o in enumerate(queue):
                if o.order_id == order_id:
                    queue[i] = None
                    break
        
        return order
    
    def get_best_bid(self) -> Optional[float]:
        """Get best bid price."""
        # Clean up empty prices
        while self.bid_prices:
            price = -self.bid_prices[0]  # Convert back from negative
            if price in self.bids and self.bids[price]:
                # Check if queue has valid orders
                queue = self.bids[price]
                # Remove cancelled orders from front
                while queue and queue[0] is None:
                    queue.popleft()
                if queue:
                    return price
            heapq.heappop(self.bid_prices)
            if price in self.bids and not self.bids[price]:
                del self.bids[price]
        return None
    
    def get_best_ask(self) -> Optional[float]:
        """Get best ask price."""
        # Clean up empty prices
        while self.ask_prices:
            price = self.ask_prices[0]
            if price in self.asks and self.asks[price]:
                # Check if queue has valid orders
                queue = self.asks[price]
                # Remove cancelled orders from front
                while queue and queue[0] is None:
                    queue.popleft()
                if queue:
                    return price
            heapq.heappop(self.ask_prices)
            if price in self.asks and not self.asks[price]:
                del self.asks[price]
        return None
    
    def get_best_bid_order(self) -> Optional[Order]:
        """Get best bid order."""
        best_bid = self.get_best_bid()
        if best_bid is None:
            return None
        
        queue = self.bids[best_bid]
        while queue and queue[0] is None:
            queue.popleft()
        
        if queue:
            return queue[0]
        return None
    
    def get_best_ask_order(self) -> Optional[Order]:
        """Get best ask order."""
        best_ask = self.get_best_ask()
        if best_ask is None:
            return None
        
        queue = self.asks[best_ask]
        while queue and queue[0] is None:
            queue.popleft()
        
        if queue:
            return queue[0]
        return None
    
    def get_spread(self) -> Optional[float]:
        """Calculate bid-ask spread."""
        best_bid = self.get_best_bid()
        best_ask = self.get_best_ask()
        
        if best_bid is None or best_ask is None:
            return None
        
        return best_ask - best_bid
    
    def get_mid_price(self) -> Optional[float]:
        """Calculate mid price."""
        best_bid = self.get_best_bid()
        best_ask = self.get_best_ask()
        
        if best_bid is None or best_ask is None:
            return None
        
        return (best_bid + best_ask) / 2
    
    def get_bid_depth(self) -> int:
        """Get total bid volume."""
        total = 0
        for price, queue in self.bids.items():
            for order in queue:
                if order is not None:
                    total += order.remaining_quantity
        return total
    
    def get_ask_depth(self) -> int:
        """Get total ask volume."""
        total = 0
        for price, queue in self.asks.items():
            for order in queue:
                if order is not None:
                    total += order.remaining_quantity
        return total
    
    def get_state(self) -> OrderBookState:
        """Get current order book state."""
        best_bid = self.get_best_bid() or 0.0
        best_ask = self.get_best_ask() or 0.0
        
        return OrderBookState(
            timestamp=time.time(),
            best_bid=best_bid,
            best_ask=best_ask,
            bid_depth=len(self.bids),
            ask_depth=len(self.asks),
            total_bid_volume=self.get_bid_depth(),
            total_ask_volume=self.get_ask_depth()
        )
    
    def validate(self) -> bool:
        """Validate order book state (no negative quantities, no duplicates)."""
        # Check for negative quantities
        for order in self.orders.values():
            if order.quantity < 0 or order.filled_quantity < 0:
                return False
            if order.filled_quantity > order.quantity:
                return False
        
        # Check for duplicate order IDs
        if len(self.orders) != len(set(self.orders.keys())):
            return False
        
        return True
    
    def __repr__(self) -> str:
        """String representation of order book."""
        best_bid = self.get_best_bid()
        best_ask = self.get_best_ask()
        spread = self.get_spread()
        
        return f"OrderBook(best_bid={best_bid}, best_ask={best_ask}, spread={spread})"
