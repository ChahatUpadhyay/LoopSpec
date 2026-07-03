"""Market scenarios for volatility regimes, liquidity droughts, flash crashes, and news shocks."""

from typing import List, Optional
from enum import Enum
from simulation.engine import SimulationEngine
from agents.base import BaseAgent
from agents.market_maker import MarketMaker
from agents.momentum import MomentumTrader
from agents.arbitrage import ArbitrageBot
from agents.institutional import InstitutionalTrader
from agents.retail import RetailTrader
from simulation.latency import LatencyProfile


class MarketScenario(Enum):
    """Market scenario types."""
    NORMAL = "normal"
    HIGH_VOLATILITY = "high_volatility"
    LOW_LIQUIDITY = "low_liquidity"
    FLASH_CRASH = "flash_crash"
    NEWS_SHOCK = "news_shock"


class ScenarioManager:
    """Manages market scenarios and their parameters."""
    
    def __init__(self, seed: Optional[int] = None):
        """Initialize scenario manager.
        
        Args:
            seed: Random seed for deterministic behavior
        """
        self.seed = seed
        self.current_scenario = MarketScenario.NORMAL
        self.scenario_start_time = 0.0
    
    def set_scenario(self, scenario: MarketScenario, current_time: float) -> None:
        """Set current market scenario.
        
        Args:
            scenario: Scenario to activate
            current_time: Current simulation time
        """
        self.current_scenario = scenario
        self.scenario_start_time = current_time
    
    def get_volatility_multiplier(self) -> float:
        """Get volatility multiplier based on current scenario."""
        if self.current_scenario == MarketScenario.HIGH_VOLATILITY:
            return 3.0
        elif self.current_scenario == MarketScenario.FLASH_CRASH:
            return 5.0
        elif self.current_scenario == MarketScenario.NEWS_SHOCK:
            return 2.0
        else:
            return 1.0
    
    def get_liquidity_multiplier(self) -> float:
        """Get liquidity multiplier based on current scenario."""
        if self.current_scenario == MarketScenario.LOW_LIQUIDITY:
            return 0.3
        elif self.current_scenario == MarketScenario.FLASH_CRASH:
            return 0.5
        else:
            return 1.0
    
    def create_flash_crash_engine(
        self,
        num_market_makers: int = 5,
        num_momentum: int = 3,
        num_arbitrage: int = 2,
        num_retail: int = 20,
        seed: Optional[int] = None
    ) -> SimulationEngine:
        """Create simulation engine configured for flash crash scenario.
        
        Args:
            num_market_makers: Number of market maker agents
            num_momentum: Number of momentum trader agents
            num_arbitrage: Number of arbitrage bot agents
            num_retail: Number of retail trader agents
            seed: Random seed
            
        Returns:
            Configured simulation engine
        """
        engine = SimulationEngine(seed)
        
        # Create market makers (with reduced liquidity during flash crash)
        for i in range(num_market_makers):
            agent = MarketMaker(
                agent_id=f"mm_{i}",
                target_spread=0.15,  # Wider spread
                base_quantity=50,  # Lower quantity
                seed=seed + i if seed else None
            )
            latency = LatencyProfile(network_delay_ms=15.0, execution_delay_ms=8.0)
            engine.add_agent(agent, latency)
        
        # Create momentum traders (will amplify the crash)
        for i in range(num_momentum):
            agent = MomentumTrader(
                agent_id=f"momentum_{i}",
                lookback_period=5,
                threshold=0.02,  # More sensitive
                base_quantity=100,
                seed=seed + i + 100 if seed else None
            )
            latency = LatencyProfile(network_delay_ms=10.0, execution_delay_ms=5.0)
            engine.add_agent(agent, latency)
        
        # Create arbitrage bots
        for i in range(num_arbitrage):
            agent = ArbitrageBot(
                agent_id=f"arb_{i}",
                min_profit_threshold=0.02,
                base_quantity=50,
                seed=seed + i + 200 if seed else None
            )
            latency = LatencyProfile(network_delay_ms=8.0, execution_delay_ms=3.0)
            engine.add_agent(agent, latency)
        
        # Create retail traders (panic selling)
        for i in range(num_retail):
            agent = RetailTrader(
                agent_id=f"retail_{i}",
                max_quantity=20,
                order_probability=0.3,  # Higher activity
                seed=seed + i + 300 if seed else None
            )
            latency = LatencyProfile(network_delay_ms=20.0, execution_delay_ms=10.0)
            engine.add_agent(agent, latency)
        
        return engine
    
    def create_normal_market_engine(
        self,
        num_market_makers: int = 5,
        num_momentum: int = 3,
        num_arbitrage: int = 2,
        num_institutional: int = 2,
        num_retail: int = 20,
        seed: Optional[int] = None
    ) -> SimulationEngine:
        """Create simulation engine configured for normal market conditions.
        
        Args:
            num_market_makers: Number of market maker agents
            num_momentum: Number of momentum trader agents
            num_arbitrage: Number of arbitrage bot agents
            num_institutional: Number of institutional trader agents
            num_retail: Number of retail trader agents
            seed: Random seed
            
        Returns:
            Configured simulation engine
        """
        engine = SimulationEngine(seed)
        
        # Create market makers
        for i in range(num_market_makers):
            agent = MarketMaker(
                agent_id=f"mm_{i}",
                target_spread=0.10,
                base_quantity=100,
                seed=seed + i if seed else None
            )
            latency = LatencyProfile(network_delay_ms=10.0, execution_delay_ms=5.0)
            engine.add_agent(agent, latency)
        
        # Create momentum traders
        for i in range(num_momentum):
            agent = MomentumTrader(
                agent_id=f"momentum_{i}",
                lookback_period=10,
                threshold=0.01,
                base_quantity=50,
                seed=seed + i + 100 if seed else None
            )
            latency = LatencyProfile(network_delay_ms=10.0, execution_delay_ms=5.0)
            engine.add_agent(agent, latency)
        
        # Create arbitrage bots
        for i in range(num_arbitrage):
            agent = ArbitrageBot(
                agent_id=f"arb_{i}",
                min_profit_threshold=0.01,
                base_quantity=100,
                seed=seed + i + 200 if seed else None
            )
            latency = LatencyProfile(network_delay_ms=8.0, execution_delay_ms=3.0)
            engine.add_agent(agent, latency)
        
        # Create institutional traders
        for i in range(num_institutional):
            agent = InstitutionalTrader(
                agent_id=f"inst_{i}",
                algorithm="twap" if i % 2 == 0 else "vwap",
                total_quantity=5000,
                time_window=100,
                seed=seed + i + 300 if seed else None
            )
            latency = LatencyProfile(network_delay_ms=12.0, execution_delay_ms=6.0)
            engine.add_agent(agent, latency)
        
        # Create retail traders
        for i in range(num_retail):
            agent = RetailTrader(
                agent_id=f"retail_{i}",
                max_quantity=10,
                order_probability=0.1,
                seed=seed + i + 400 if seed else None
            )
            latency = LatencyProfile(network_delay_ms=15.0, execution_delay_ms=7.0)
            engine.add_agent(agent, latency)
        
        return engine
