"""Momentum trader agent that follows price trends."""

from typing import List, Optional
from collections import deque
from agents.base import BaseAgent
from matching_engine.types import Order, OrderSide, OrderType, OrderBookState


class MomentumTrader(BaseAgent):
    """Momentum trader that buys upward moves and sells downward moves."""
    
    def __init__(
        self,
        agent_id: str,
        lookback_period: int = 10,
        threshold: float = 0.01,
        base_quantity: int = 50,
        seed: Optional[int] = None
    ):
        """Initialize momentum trader.
        
        Args:
            agent_id: Unique identifier
            lookback_period: Number of time steps to look back for trend
            threshold: Price change threshold to trigger trades
            base_quantity: Base order quantity
            seed: Random seed for deterministic behavior
        """
        super().__init__(agent_id, "momentum", seed)
        self.lookback_period = lookback_period
        self.threshold = threshold
        self.base_quantity = base_quantity
        self.price_history = deque(maxlen=lookback_period)
    
    def generate_orders(self, order_book_state: OrderBookState, current_time: float) -> List[Order]:
        """Generate orders based on price momentum.
        
        Args:
            order_book_state: Current order book state
            current_time: Current simulation time
            
        Returns:
            List of orders (at most one per time step)
        """
        orders = []
        
        # Get current price
        current_price = order_book_state.mid_price if hasattr(order_book_state, 'mid_price') else None
        if current_price is None:
            current_price = (order_book_state.best_bid + order_book_state.best_ask) / 2 if order_book_state.best_bid and order_book_state.best_ask else None
        
        if current_price is None:
            return orders
        
        # Add to price history
        self.price_history.append(current_price)
        
        # Need enough history to calculate trend
        if len(self.price_history) < self.lookback_period:
            return orders
        
        # Calculate price change over lookback period
        old_price = self.price_history[0]
        price_change = (current_price - old_price) / old_price
        
        # Add stochastic variation to threshold
        stochastic_threshold = self.threshold * (1 + self.rng.gauss(0, 0.2))
        
        # Generate order based on trend
        if price_change > stochastic_threshold:
            # Upward trend: buy
            quantity = int(self.base_quantity * (1 + self.rng.gauss(0, 0.3)))
            quantity = max(1, quantity)
            
            order = self.create_order(
                side=OrderSide.BUY,
                order_type=OrderType.MARKET,
                price=current_price,
                quantity=quantity,
                timestamp=current_time
            )
            orders.append(order)
        elif price_change < -stochastic_threshold:
            # Downward trend: sell
            quantity = int(self.base_quantity * (1 + self.rng.gauss(0, 0.3)))
            quantity = max(1, quantity)
            
            order = self.create_order(
                side=OrderSide.SELL,
                order_type=OrderType.MARKET,
                price=current_price,
                quantity=quantity,
                timestamp=current_time
            )
            orders.append(order)
        
        return orders
