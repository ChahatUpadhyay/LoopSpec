"""Retail trader agent with random small orders."""

from typing import List, Optional
from agents.base import BaseAgent
from matching_engine.types import Order, OrderSide, OrderType, OrderBookState


class RetailTrader(BaseAgent):
    """Retail trader that submits random small orders."""
    
    def __init__(
        self,
        agent_id: str,
        max_quantity: int = 10,
        order_probability: float = 0.1,
        seed: Optional[int] = None
    ):
        """Initialize retail trader.
        
        Args:
            agent_id: Unique identifier
            max_quantity: Maximum order quantity
            order_probability: Probability of submitting an order each step
            seed: Random seed for deterministic behavior
        """
        super().__init__(agent_id, "retail", seed)
        self.max_quantity = max_quantity
        self.order_probability = order_probability
    
    def generate_orders(self, order_book_state: OrderBookState, current_time: float) -> List[Order]:
        """Generate random small orders.
        
        Args:
            order_book_state: Current order book state
            current_time: Current simulation time
            
        Returns:
            List of orders (at most one per time step)
        """
        orders = []
        
        # Decide whether to submit an order
        if self.rng.random() > self.order_probability:
            return orders
        
        # Random side
        side = OrderSide.BUY if self.rng.random() < 0.5 else OrderSide.SELL
        
        # Random quantity
        quantity = self.rng.randint(1, self.max_quantity)
        
        # Get current price
        current_price = (order_book_state.best_bid + order_book_state.best_ask) / 2 if order_book_state.best_bid and order_book_state.best_ask else 100.0
        
        # Random order type (mostly limit, occasional market)
        order_type = OrderType.MARKET if self.rng.random() < 0.1 else OrderType.LIMIT
        
        # For limit orders, add price offset
        if order_type == OrderType.LIMIT:
            price_offset = self.rng.gauss(0, current_price * 0.01)
            price = current_price + price_offset
            price = round(max(0.01, price), 2)
        else:
            price = current_price
        
        # Create order
        order = self.create_order(
            side=side,
            order_type=order_type,
            price=price,
            quantity=quantity,
            timestamp=current_time
        )
        orders.append(order)
        
        return orders
