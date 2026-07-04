"""Main simulation engine for the limit order book simulator."""

import time
from typing import List, Dict, Optional
from matching_engine.matching import MatchingEngine
from matching_engine.types import OrderBookState, Trade
from agents.base import BaseAgent
from simulation.latency import LatencySimulator, LatencyProfile


class SimulationEngine:
    """Main simulation engine that orchestrates agents and matching."""
    
    def __init__(self, seed: Optional[int] = None):
        """Initialize simulation engine.
        
        Args:
            seed: Random seed for deterministic behavior
        """
        self.seed = seed
        self.matching_engine = MatchingEngine()
        self.latency_simulator = LatencySimulator(seed)
        self.agents: List[BaseAgent] = []
        self.current_time = 0.0
        self.time_step = 0.001  # 1ms per step
        self.order_count = 0
        self.trade_count = 0
    
    def add_agent(self, agent: BaseAgent, latency_profile: Optional[LatencyProfile] = None) -> None:
        """Add an agent to the simulation.
        
        Args:
            agent: Agent to add
            latency_profile: Latency profile for the agent
        """
        self.agents.append(agent)
        if latency_profile:
            self.latency_simulator.set_profile(agent.agent_id, latency_profile)
    
    def step(self) -> List[Trade]:
        """Execute one simulation step.
        
        Returns:
            List of trades executed in this step
        """
        trades = []
        
        # Get current order book state
        order_book = self.matching_engine.get_order_book()
        order_book_state = order_book.get_state()
        
        # Collect orders from all agents
        all_orders = []
        for agent in self.agents:
            agent_orders = agent.generate_orders(order_book_state, self.current_time)
            all_orders.extend(agent_orders)
        
        # Process orders with latency
        for order in all_orders:
            # Apply network delay
            adjusted_time = self.latency_simulator.apply_network_delay(
                order.agent_id,
                self.current_time
            )
            order.timestamp = adjusted_time
            
            # Submit order to matching engine
            new_trades, remaining = self.matching_engine.submit_order(order)
            trades.extend(new_trades)
            self.order_count += 1
        
        # Update agent positions based on trades
        for trade in trades:
            for agent in self.agents:
                agent.update_position(trade)
        
        # Update counters
        self.trade_count += len(trades)
        self.current_time += self.time_step
        
        return trades
    
    def run(self, num_steps: int) -> List[Trade]:
        """Run simulation for a specified number of steps.
        
        Args:
            num_steps: Number of simulation steps
            
        Returns:
            List of all trades executed
        """
        all_trades = []
        
        for _ in range(num_steps):
            step_trades = self.step()
            all_trades.extend(step_trades)
        
        return all_trades
    
    def get_order_book_state(self) -> OrderBookState:
        """Get current order book state."""
        return self.matching_engine.get_order_book().get_state()
    
    def get_trades(self) -> List[Trade]:
        """Get all trades."""
        return self.matching_engine.get_trades()
    
    def get_order_count(self) -> int:
        """Get total number of orders processed."""
        return self.order_count
    
    def get_trade_count(self) -> int:
        """Get total number of trades executed."""
        return self.trade_count
    
    def reset(self) -> None:
        """Reset simulation to initial state."""
        self.matching_engine = MatchingEngine()
        self.current_time = 0.0
        self.order_count = 0
        self.trade_count = 0
        
        # Reset agents
        for agent in self.agents:
            agent.agent.inventory = 0
            agent.agent.cash = agent.agent.initial_capital
