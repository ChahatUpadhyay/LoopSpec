"""Market maker agent that maintains spread and balances inventory."""

from typing import List, Optional
from agents.base import BaseAgent
from matching_engine.types import Order, OrderSide, OrderType, OrderBookState


class MarketMaker(BaseAgent):
    """Market maker agent that provides liquidity by quoting on both sides."""
    
    def __init__(
        self,
        agent_id: str,
        target_spread: float = 0.10,
        base_quantity: int = 100,
        inventory_threshold: int = 1000,
        seed: Optional[int] = None
    ):
        """Initialize market maker.
        
        Args:
            agent_id: Unique identifier
            target_spread: Target bid-ask spread
            base_quantity: Base order quantity
            inventory_threshold: Inventory level at which to adjust quotes
            seed: Random seed for deterministic behavior
        """
        super().__init__(agent_id, "market_maker", seed)
        self.target_spread = target_spread
        self.base_quantity = base_quantity
        self.inventory_threshold = inventory_threshold
    
    def generate_orders(self, order_book_state: OrderBookState, current_time: float) -> List[Order]:
        """Generate orders to maintain spread and balance inventory.
        
        Args:
            order_book_state: Current order book state
            current_time: Current simulation time
            
        Returns:
            List of orders (typically one bid and one ask)
        """
        orders = []
        
        # Calculate reference price (mid price or last trade price)
        if order_book_state.best_bid and order_book_state.best_ask:
            reference_price = (order_book_state.best_bid + order_book_state.best_ask) / 2
        elif order_book_state.best_bid:
            reference_price = order_book_state.best_bid
        elif order_book_state.best_ask:
            reference_price = order_book_state.best_ask
        else:
            reference_price = 100.0  # Default starting price
        
        # Adjust quotes based on inventory
        inventory_skew = self.agent.inventory / self.inventory_threshold
        price_adjustment = inventory_skew * self.target_spread * 0.5
        
        # Calculate bid and ask prices
        bid_price = reference_price - self.target_spread / 2 - price_adjustment
        ask_price = reference_price + self.target_spread / 2 - price_adjustment
        
        # Add stochastic variation
        bid_price += self.rng.gauss(0, self.target_spread * 0.1)
        ask_price += self.rng.gauss(0, self.target_spread * 0.1)
        
        # Ensure bid < ask
        if bid_price >= ask_price:
            bid_price = ask_price - self.target_spread
        
        # Calculate quantities based on inventory
        if self.agent.inventory > self.inventory_threshold:
            # Long inventory: reduce bid size, increase ask size
            bid_qty = int(self.base_quantity * (1 - inventory_skew * 0.5))
            ask_qty = int(self.base_quantity * (1 + inventory_skew * 0.5))
        elif self.agent.inventory < -self.inventory_threshold:
            # Short inventory: increase bid size, reduce ask size
            bid_qty = int(self.base_quantity * (1 + abs(inventory_skew) * 0.5))
            ask_qty = int(self.base_quantity * (1 - abs(inventory_skew) * 0.5))
        else:
            # Balanced inventory
            bid_qty = self.base_quantity
            ask_qty = self.base_quantity
        
        # Ensure minimum quantity
        bid_qty = max(1, bid_qty)
        ask_qty = max(1, ask_qty)
        
        # Create bid order
        bid_order = self.create_order(
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            price=round(bid_price, 2),
            quantity=bid_qty,
            timestamp=current_time
        )
        orders.append(bid_order)
        
        # Create ask order
        ask_order = self.create_order(
            side=OrderSide.SELL,
            order_type=OrderType.LIMIT,
            price=round(ask_price, 2),
            quantity=ask_qty,
            timestamp=current_time
        )
        orders.append(ask_order)
        
        return orders
