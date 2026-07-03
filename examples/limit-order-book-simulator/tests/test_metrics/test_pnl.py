"""Unit tests for PnL accounting."""

import pytest
from metrics.pnl import PnLTracker
from matching_engine.types import Agent, Trade


def test_pnl_tracking():
    """Test T21: PnL Tracking by Agent"""
    tracker = PnLTracker()
    
    # Add agent
    agent = Agent(agent_id="agent1", agent_type="test", initial_capital=100000.0)
    tracker.add_agent(agent)
    
    # Record a trade (agent buys 100 shares at $100)
    trade = Trade(
        trade_id="t1",
        buy_order_id="o1",
        sell_order_id="o2",
        price=100.0,
        quantity=100,
        buy_agent_id="agent1",
        sell_agent_id="agent2"
    )
    tracker.record_trade(trade, current_price=100.0)
    
    # Record PnL
    tracker.record_pnl("agent1", current_price=100.0, timestamp=0.0)
    
    # PnL should be -$10,000 (spent on shares)
    pnl = tracker.get_pnl("agent1")
    assert pnl == -10000.0


def test_price_conservation():
    """Test T34: Price Conservation"""
    tracker = PnLTracker()
    
    # Add two agents
    agent1 = Agent(agent_id="agent1", agent_type="test", initial_capital=100000.0)
    agent2 = Agent(agent_id="agent2", agent_type="test", initial_capital=100000.0)
    tracker.add_agent(agent1)
    tracker.add_agent(agent2)
    
    # Record a trade
    trade = Trade(
        trade_id="t1",
        buy_order_id="o1",
        sell_order_id="o2",
        price=100.0,
        quantity=100,
        buy_agent_id="agent1",
        sell_agent_id="agent2"
    )
    tracker.record_trade(trade, current_price=100.0)
    
    # Record PnL
    tracker.record_pnl("agent1", current_price=100.0, timestamp=0.0)
    tracker.record_pnl("agent2", current_price=100.0, timestamp=0.0)
    
    # Total value should be conserved
    total_value = tracker.get_total_value(current_price=100.0)
    initial_total = 200000.0
    
    # Allow for small floating-point error
    assert abs(total_value - initial_total) < initial_total * 0.0001


def test_pnl_balance():
    """Test T37: PnL Accounting Balances"""
    tracker = PnLTracker()
    
    # Add two agents
    agent1 = Agent(agent_id="agent1", agent_type="test", initial_capital=100000.0)
    agent2 = Agent(agent_id="agent2", agent_type="test", initial_capital=100000.0)
    tracker.add_agent(agent1)
    tracker.add_agent(agent2)
    
    # Record a trade
    trade = Trade(
        trade_id="t1",
        buy_order_id="o1",
        sell_order_id="o2",
        price=100.0,
        quantity=100,
        buy_agent_id="agent1",
        sell_agent_id="agent2"
    )
    tracker.record_trade(trade, current_price=100.0)
    
    # Record PnL
    tracker.record_pnl("agent1", current_price=100.0, timestamp=0.0)
    tracker.record_pnl("agent2", current_price=100.0, timestamp=0.0)
    
    # Sum of PnL should be ~0 (zero-sum game)
    all_pnl = tracker.get_all_pnl()
    total_pnl = sum(all_pnl.values())
    
    assert abs(total_pnl) < 0.01  # Allow for floating-point precision
