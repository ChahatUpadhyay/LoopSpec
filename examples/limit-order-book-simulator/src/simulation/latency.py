"""Latency simulation for network, execution, and cancellation delays."""

import random
import time
from typing import Optional, Dict
from dataclasses import dataclass


@dataclass
class LatencyProfile:
    """Latency profile for an agent."""
    network_delay_ms: float = 10.0
    execution_delay_ms: float = 5.0
    cancellation_delay_ms: float = 3.0


class LatencySimulator:
    """Simulates latency for order submission, execution, and cancellation."""
    
    def __init__(self, seed: Optional[int] = None):
        """Initialize latency simulator.
        
        Args:
            seed: Random seed for deterministic behavior
        """
        self.seed = seed
        if seed is not None:
            self.rng = random.Random(seed)
        else:
            self.rng = random.Random()
        
        # Agent latency profiles
        self.profiles: Dict[str, LatencyProfile] = {}
    
    def set_profile(self, agent_id: str, profile: LatencyProfile) -> None:
        """Set latency profile for an agent.
        
        Args:
            agent_id: Agent identifier
            profile: Latency profile
        """
        self.profiles[agent_id] = profile
    
    def get_profile(self, agent_id: str) -> LatencyProfile:
        """Get latency profile for an agent.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            Latency profile (default if not set)
        """
        return self.profiles.get(agent_id, LatencyProfile())
    
    def apply_network_delay(self, agent_id: str, submission_time: float) -> float:
        """Apply network delay to order submission.
        
        Args:
            agent_id: Agent identifier
            submission_time: Original submission time
            
        Returns:
            Adjusted submission time with network delay
        """
        profile = self.get_profile(agent_id)
        
        # Add stochastic variation (±20%)
        delay = profile.network_delay_ms * (1 + self.rng.gauss(0, 0.2))
        delay = max(0, delay)  # Ensure non-negative
        
        return submission_time + delay / 1000.0  # Convert ms to seconds
    
    def apply_execution_delay(self, agent_id: str, receipt_time: float) -> float:
        """Apply execution delay to order matching.
        
        Args:
            agent_id: Agent identifier
            receipt_time: Time order was received by matching engine
            
        Returns:
            Adjusted execution time with execution delay
        """
        profile = self.get_profile(agent_id)
        
        # Add stochastic variation (±20%)
        delay = profile.execution_delay_ms * (1 + self.rng.gauss(0, 0.2))
        delay = max(0, delay)  # Ensure non-negative
        
        return receipt_time + delay / 1000.0  # Convert ms to seconds
    
    def apply_cancellation_delay(self, agent_id: str, submission_time: float) -> float:
        """Apply cancellation delay to cancel orders.
        
        Args:
            agent_id: Agent identifier
            submission_time: Time cancel order was submitted
            
        Returns:
            Adjusted cancellation time with cancellation delay
        """
        profile = self.get_profile(agent_id)
        
        # Add stochastic variation (±20%)
        delay = profile.cancellation_delay_ms * (1 + self.rng.gauss(0, 0.2))
        delay = max(0, delay)  # Ensure non-negative
        
        return submission_time + delay / 1000.0  # Convert ms to seconds
