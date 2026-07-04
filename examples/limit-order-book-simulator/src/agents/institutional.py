"""Institutional trader agent with TWAP and VWAP execution algorithms."""

from typing import List, Optional, Literal
from agents.base import BaseAgent
from matching_engine.types import Order, OrderSide, OrderType, OrderBookState


class InstitutionalTrader(BaseAgent):
    """Institutional trader with TWAP and VWAP execution algorithms."""
    
    def __init__(
        self,
        agent_id: str,
        algorithm: Literal["twap", "vwap"] = "twap",
        total_quantity: int = 10000,
        time_window: int = 100,
        seed: Optional[int] = None
    ):
        """Initialize institutional trader.
        
        Args:
            agent_id: Unique identifier
            algorithm: Execution algorithm (twap or vwap)
            total_quantity: Total quantity to execute
            time_window: Number of time steps to execute over
            seed: Random seed for deterministic behavior
        """
        super().__init__(agent_id, "institutional", seed)
        self.algorithm = algorithm
        self.total_quantity = total_quantity
        self.time_window = time_window
        self.remaining_quantity = total_quantity
        self.current_step = 0
        self.side = OrderSide.BUY if self.rng.random() < 0.5 else OrderSide.SELL
    
    def generate_orders(self, order_book_state: OrderBookState, current_time: float) -> List[Order]:
        """Generate orders based on execution algorithm.
        
        Args:
            order_book_state: Current order book state
            current_time: Current simulation time
            
        Returns:
            List of orders (at most one per time step)
        """
        orders = []
        
        # Check if execution is complete
        if self.remaining_quantity <= 0 or self.current_step >= self.time_window:
            return orders
        
        # Calculate target quantity for this step
        if self.algorithm == "twap":
            # Time-Weighted Average Price: execute evenly over time
            target_quantity = self.total_quantity / self.time_window
        else:  # vwap
            # Volume-Weighted Average Price: execute weighted by volume
            total_volume = order_book_state.total_bid_volume + order_book_state.total_ask_volume
            if total_volume > 0:
                volume_weight = order_book_state.total_bid_volume / total_volume if self.side == OrderSide.BUY else order_book_state.total_ask_volume / total_volume
                target_quantity = (self.total_quantity / self.time_window) * (1 + volume_weight)
            else:
                target_quantity = self.total_quantity / self.time_window
        
        # Add stochastic variation
        stochastic_quantity = int(target_quantity * (1 + self.rng.gauss(0, 0.1)))
        stochastic_quantity = max(1, min(stochastic_quantity, self.remaining_quantity))
        
        # Get current price
        current_price = (order_book_state.best_bid + order_book_state.best_ask) / 2 if order_book_state.best_bid and order_book_state.best_ask else 100.0
        
        # Create order
        order = self.create_order(
            side=self.side,
            order_type=OrderType.LIMIT,
            price=current_price,
            quantity=stochastic_quantity,
            timestamp=current_time
        )
        orders.append(order)
        
        # Update state
        self.remaining_quantity -= stochastic_quantity
        self.current_step += 1
        
        return orders
