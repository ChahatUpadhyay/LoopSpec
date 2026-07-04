"""Base agent class for all trading agents."""

from abc import ABC, abstractmethod
from typing import List, Optional
import random
import time
from matching_engine.types import Order, OrderSide, OrderType, Agent


class BaseAgent(ABC):
    """Abstract base class for all trading agents."""
    
    def __init__(self, agent_id: str, agent_type: str, seed: Optional[int] = None):
        """Initialize agent.
        
        Args:
            agent_id: Unique identifier for the agent
            agent_type: Type of agent (market_maker, momentum, etc.)
            seed: Random seed for deterministic behavior
        """
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.seed = seed
        
        # Initialize random number generator
        if seed is not None:
            self.rng = random.Random(seed)
        else:
            self.rng = random.Random()
        
        # Agent state
        self.agent = Agent(agent_id=agent_id, agent_type=agent_type)
        self.order_counter = 0
    
    @abstractmethod
    def generate_orders(self, order_book_state, current_time: float) -> List[Order]:
        """Generate orders based on market conditions.
        
        Args:
            order_book_state: Current state of the order book
            current_time: Current simulation time
            
        Returns:
            List of orders to submit
        """
        pass
    
    def create_order(
        self,
        side: OrderSide,
        order_type: OrderType,
        price: float,
        quantity: int,
        timestamp: Optional[float] = None
    ) -> Order:
        """Create a new order.
        
        Args:
            side: Order side (buy or sell)
            order_type: Order type (limit, market, etc.)
            price: Order price
            quantity: Order quantity
            timestamp: Order timestamp (defaults to current time)
            
        Returns:
            New Order object
        """
        self.order_counter += 1
        order_id = f"{self.agent_id}_order_{self.order_counter}"
        
        return Order(
            order_id=order_id,
            agent_id=self.agent_id,
            side=side,
            order_type=order_type,
            price=price,
            quantity=quantity,
            timestamp=timestamp or time.time()
        )
    
    def update_position(self, trade) -> None:
        """Update agent position after a trade.
        
        Args:
            trade: Executed trade
        """
        if trade.buy_agent_id == self.agent_id:
            # Agent bought
            self.agent.inventory += trade.quantity
            self.agent.cash -= trade.price * trade.quantity
        elif trade.sell_agent_id == self.agent_id:
            # Agent sold
            self.agent.inventory -= trade.quantity
            self.agent.cash += trade.price * trade.quantity
    
    def get_pnl(self) -> float:
        """Get current PnL."""
        return self.agent.pnl
    
    def get_inventory(self) -> int:
        """Get current inventory."""
        return self.agent.inventory
    
    def get_cash(self) -> float:
        """Get current cash."""
        return self.agent.cash
