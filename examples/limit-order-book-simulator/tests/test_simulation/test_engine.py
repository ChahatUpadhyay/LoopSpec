"""Integration tests for simulation engine."""

import pytest
from simulation.engine import SimulationEngine
from simulation.scenarios import ScenarioManager
from agents.market_maker import MarketMaker
from agents.momentum import MomentumTrader
from agents.retail import RetailTrader


def test_stochastic_behavior():
    """Test T12: Stochastic Agent Behavior"""
    # Run with same seed twice
    engine1 = SimulationEngine(seed=42)
    engine2 = SimulationEngine(seed=42)
    
    # Add same agents
    mm1 = MarketMaker("mm1", seed=42)
    mm2 = MarketMaker("mm1", seed=42)
    engine1.add_agent(mm1)
    engine2.add_agent(mm2)
    
    # Run one step each
    engine1.step()
    engine2.step()
    
    # Should have same order count (deterministic with same seed)
    assert engine1.get_order_count() == engine2.get_order_count()


def test_deterministic_replay():
    """Test T32: Deterministic Replay"""
    # Run simulation with seed 42 twice
    engine1 = ScenarioManager(seed=42).create_normal_market_engine(seed=42)
    engine2 = ScenarioManager(seed=42).create_normal_market_engine(seed=42)
    
    # Run both for same number of steps
    steps = 100
    for _ in range(steps):
        engine1.step()
        engine2.step()
    
    # Should have identical results
    assert engine1.get_order_count() == engine2.get_order_count()
    assert engine1.get_trade_count() == engine2.get_trade_count()


def test_price_emergence():
    """Test T17: Price Emergence from Order Flow"""
    # Run simulation with different seeds
    engine1 = ScenarioManager(seed=1).create_normal_market_engine(seed=1)
    engine2 = ScenarioManager(seed=2).create_normal_market_engine(seed=2)
    
    # Run both
    for _ in range(100):
        engine1.step()
        engine2.step()
    
    # Get final states
    state1 = engine1.get_order_book_state()
    state2 = engine2.get_order_book_state()
    
    # Different seeds should produce different prices
    # (at least one of bid/ask should differ)
    assert state1.best_bid != state2.best_bid or state1.best_ask != state2.best_ask
