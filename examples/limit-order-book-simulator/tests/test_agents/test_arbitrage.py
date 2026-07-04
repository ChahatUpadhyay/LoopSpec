"""Unit tests for arbitrage bot behavior."""

import pytest
from agents.arbitrage import ArbitrageBot
from matching_engine.types import OrderBookState, OrderSide


def test_inefficiency_detection():
    """Test T9: Arbitrage Bot Inefficiency Detection"""
    arb = ArbitrageBot("arb1", min_profit_threshold=0.01, seed=42)
    
    # Create crossed market (arbitrage opportunity)
    state = OrderBookState(
        timestamp=0.0,
        best_bid=101.0,  # Higher than ask
        best_ask=99.0,   # Lower than bid
        bid_depth=5,
        ask_depth=5,
        total_bid_volume=500,
        total_ask_volume=500
    )
    
    # Generate orders
    orders = arb.generate_orders(state, current_time=0.0)
    
    # Should generate buy and sell orders
    assert len(orders) == 2
    assert orders[0].side == OrderSide.BUY
    assert orders[1].side == OrderSide.SELL
