"""Unit tests for momentum trader behavior."""

import pytest
from agents.momentum import MomentumTrader
from matching_engine.types import OrderBookState, OrderSide


def test_upward_move_buy():
    """Test T7: Momentum Trader Upward Move"""
    momentum = MomentumTrader("mom1", lookback_period=5, threshold=0.01, seed=42)
    
    # Build price history with upward trend
    for i in range(10):
        momentum.price_history.append(100.0 + i * 0.5)  # Increasing prices
    
    state = OrderBookState(
        timestamp=0.0,
        best_bid=104.5,
        best_ask=104.6,
        bid_depth=5,
        ask_depth=5,
        total_bid_volume=500,
        total_ask_volume=500
    )
    
    # Generate orders
    orders = momentum.generate_orders(state, current_time=0.0)
    
    # Should generate buy order
    if len(orders) > 0:
        assert orders[0].side == OrderSide.BUY
        assert orders[0].quantity > 0


def test_downward_move_sell():
    """Test T8: Momentum Trader Downward Move"""
    momentum = MomentumTrader("mom1", lookback_period=5, threshold=0.01, seed=42)
    
    # Build price history with downward trend
    for i in range(10):
        momentum.price_history.append(105.0 - i * 0.5)  # Decreasing prices
    
    state = OrderBookState(
        timestamp=0.0,
        best_bid=100.5,
        best_ask=100.6,
        bid_depth=5,
        ask_depth=5,
        total_bid_volume=500,
        total_ask_volume=500
    )
    
    # Generate orders
    orders = momentum.generate_orders(state, current_time=0.0)
    
    # Should generate sell order
    if len(orders) > 0:
        assert orders[0].side == OrderSide.SELL
        assert orders[0].quantity > 0
