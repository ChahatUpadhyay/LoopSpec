"""Unit tests for market maker behavior."""

import pytest
from agents.market_maker import MarketMaker
from matching_engine.types import OrderBookState, OrderSide


def test_spread_maintenance():
    """Test T5: Market Maker Spread Maintenance"""
    mm = MarketMaker("mm1", target_spread=0.10, base_quantity=100, seed=42)
    
    # Create order book state
    state = OrderBookState(
        timestamp=0.0,
        best_bid=99.95,
        best_ask=100.05,
        bid_depth=5,
        ask_depth=5,
        total_bid_volume=500,
        total_ask_volume=500
    )
    
    # Generate orders
    orders = mm.generate_orders(state, current_time=0.0)
    
    # Should generate bid and ask orders
    assert len(orders) == 2
    assert orders[0].side == OrderSide.BUY
    assert orders[1].side == OrderSide.SELL
    
    # Check spread is close to target
    spread = orders[1].price - orders[0].price
    assert 0.08 <= spread <= 0.12  # Allow for stochastic variation


def test_inventory_balancing():
    """Test T6: Market Maker Inventory Balancing"""
    mm = MarketMaker("mm1", target_spread=0.10, base_quantity=100, inventory_threshold=1000, seed=42)
    
    # Set long inventory
    mm.agent.inventory = 1500
    
    state = OrderBookState(
        timestamp=0.0,
        best_bid=100.0,
        best_ask=100.10,
        bid_depth=5,
        ask_depth=5,
        total_bid_volume=500,
        total_ask_volume=500
    )
    
    # Generate orders
    orders = mm.generate_orders(state, current_time=0.0)
    
    # Bid price should be lowered to encourage selling
    bid_order = orders[0]
    assert bid_order.side == OrderSide.BUY
    # With long inventory, bid should be lower than reference
    assert bid_order.price < 100.0
