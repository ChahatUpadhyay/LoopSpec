"""PnL accounting with balance verification."""

from typing import Dict, Optional
from dataclasses import dataclass
from matching_engine.types import Agent, Trade


@dataclass
class PnLRecord:
    """Record of PnL for an agent at a point in time."""
    agent_id: str
    timestamp: float
    cash: float
    inventory: int
    inventory_value: float
    total_value: float
    pnl: float


class PnLTracker:
    """Tracks PnL for all agents and verifies balance conservation."""
    
    def __init__(self):
        """Initialize PnL tracker."""
        self.agents: Dict[str, Agent] = {}
        self.pnl_history: Dict[str, list] = {}
        self.initial_total_value: float = 0.0
        self.agent_positions: Dict[str, Dict] = {}  # Track cash and inventory separately
    
    def add_agent(self, agent: Agent) -> None:
        """Add an agent to track.
        
        Args:
            agent: Agent to track
        """
        self.agents[agent.agent_id] = agent
        self.pnl_history[agent.agent_id] = []
        # Initialize position tracking with default values
        self.agent_positions[agent.agent_id] = {
            'cash': 100000.0,  # Default initial capital
            'inventory': 0
        }
    
    def record_trade(self, trade: Trade, current_price: float) -> None:
        """Record a trade and update agent positions.
        
        Args:
            trade: Executed trade
            current_price: Current market price for inventory valuation
        """
        # Update buyer
        if trade.buy_agent_id in self.agent_positions:
            self.agent_positions[trade.buy_agent_id]['inventory'] += trade.quantity
            self.agent_positions[trade.buy_agent_id]['cash'] -= trade.price * trade.quantity
        
        # Update seller
        if trade.sell_agent_id in self.agent_positions:
            self.agent_positions[trade.sell_agent_id]['inventory'] -= trade.quantity
            self.agent_positions[trade.sell_agent_id]['cash'] += trade.price * trade.quantity
    
    def record_pnl(self, agent_id: str, current_price: float, timestamp: float) -> None:
        """Record PnL for an agent.
        
        Args:
            agent_id: Agent identifier
            current_price: Current market price
            timestamp: Current time
        """
        if agent_id not in self.agent_positions:
            return
        
        pos = self.agent_positions[agent_id]
        agent = self.agents[agent_id]
        inventory_value = pos['inventory'] * current_price
        total_value = pos['cash'] + inventory_value
        pnl = total_value - 100000.0  # Default initial capital
        
        record = PnLRecord(
            agent_id=agent_id,
            timestamp=timestamp,
            cash=pos['cash'],
            inventory=pos['inventory'],
            inventory_value=inventory_value,
            total_value=total_value,
            pnl=pnl
        )
        
        self.pnl_history[agent_id].append(record)
    
    def get_pnl(self, agent_id: str) -> Optional[float]:
        """Get current PnL for an agent.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            Current PnL
        """
        if agent_id not in self.agent_positions:
            return None
        
        pos = self.agent_positions[agent_id]
        inventory_value = pos['inventory'] * 100.0
        total_value = pos['cash'] + inventory_value
        return total_value - 100000.0
    
    def get_all_pnl(self) -> Dict[str, float]:
        """Get PnL for all agents.
        
        Returns:
            Dictionary mapping agent_id to PnL
        """
        result = {}
        for agent_id, pos in self.agent_positions.items():
            agent = self.agents[agent_id]
            inventory_value = pos['inventory'] * 100.0  # Use current price
            total_value = pos['cash'] + inventory_value
            result[agent_id] = total_value - 100000.0  # Default initial capital
        return result
    
    def verify_balance_conservation(self, tolerance: float = 0.01) -> bool:
        """Verify that total value is conserved (zero-sum PnL).
        
        Args:
            tolerance: Acceptable deviation from zero
            
        Returns:
            True if balance is conserved within tolerance
        """
        all_pnl = self.get_all_pnl()
        total_pnl = sum(all_pnl.values())
        return abs(total_pnl) < tolerance
    
    def get_total_value(self, current_price: float) -> float:
        """Calculate total value across all agents.
        
        Args:
            current_price: Current market price
            
        Returns:
            Total value
        """
        total = 0.0
        for pos in self.agent_positions.values():
            inventory_value = pos['inventory'] * current_price
            total += pos['cash'] + inventory_value
        
        return total
    
    def get_pnl_history(self, agent_id: str) -> list:
        """Get PnL history for an agent.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            List of PnL records
        """
        return self.pnl_history.get(agent_id, [])
