"""Arbitrage bot agent that exploits temporary price inefficiencies."""

from typing import List, Optional
from agents.base import BaseAgent
from matching_engine.types import Order, OrderSide, OrderType, OrderBookState


class ArbitrageBot(BaseAgent):
    """Arbitrage bot that detects and trades on price inefficiencies."""
    
    def __init__(
        self,
        agent_id: str,
        min_profit_threshold: float = 0.01,
        base_quantity: int = 100,
        seed: Optional[int] = None
    ):
        """Initialize arbitrage bot.
        
        Args:
            agent_id: Unique identifier
            min_profit_threshold: Minimum profit percentage to trigger trade
            base_quantity: Base order quantity
            seed: Random seed for deterministic behavior
        """
        super().__init__(agent_id, "arbitrage", seed)
        self.min_profit_threshold = min_profit_threshold
        self.base_quantity = base_quantity
    
    def generate_orders(self, order_book_state: OrderBookState, current_time: float) -> List[Order]:
        """Generate orders to exploit arbitrage opportunities.
        
        Args:
            order_book_state: Current order book state
            current_time: Current simulation time
            
        Returns:
            List of orders (at most one per time step)
        """
        orders = []
        
        # Check for crossed markets (arbitrage opportunity)
        if order_book_state.best_bid and order_book_state.best_ask:
            # If best bid > best ask, there's an arbitrage opportunity
            if order_book_state.best_bid > order_book_state.best_ask:
                profit_pct = (order_book_state.best_bid - order_book_state.best_ask) / order_book_state.best_ask
                
                # Add stochastic variation to threshold
                stochastic_threshold = self.min_profit_threshold * (1 + self.rng.gauss(0, 0.1))
                
                if profit_pct > stochastic_threshold:
                    # Execute arbitrage: buy at ask, sell at bid
                    quantity = int(self.base_quantity * (1 + self.rng.gauss(0, 0.2)))
                    quantity = max(1, quantity)
                    
                    # Buy at best ask
                    buy_order = self.create_order(
                        side=OrderSide.BUY,
                        order_type=OrderType.LIMIT,
                        price=order_book_state.best_ask,
                        quantity=quantity,
                        timestamp=current_time
                    )
                    orders.append(buy_order)
                    
                    # Sell at best bid
                    sell_order = self.create_order(
                        side=OrderSide.SELL,
                        order_type=OrderType.LIMIT,
                        price=order_book_state.best_bid,
                        quantity=quantity,
                        timestamp=current_time
                    )
                    orders.append(sell_order)
        
        return orders
