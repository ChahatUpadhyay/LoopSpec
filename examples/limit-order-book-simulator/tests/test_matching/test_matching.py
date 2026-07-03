"""Unit tests for order matching logic."""

import pytest
import time
from matching_engine.matching import MatchingEngine
from matching_engine.types import Order, OrderSide, OrderType, OrderStatus


def test_price_time_priority():
    """Test T1: Price-Time Priority Matching"""
    engine = MatchingEngine()
    
    # Submit orders at same price with different timestamps
    order1 = Order("o1", "a1", OrderSide.SELL, OrderType.LIMIT, 100.0, 50, timestamp=1.0)
    order2 = Order("o2", "a2", OrderSide.SELL, OrderType.LIMIT, 100.0, 30, timestamp=2.0)
    order3 = Order("o3", "a3", OrderSide.SELL, OrderType.LIMIT, 100.0, 20, timestamp=3.0)
    
    engine.submit_order(order1)
    engine.submit_order(order2)
    engine.submit_order(order3)
    
    # Submit market buy order
    market_order = Order("m1", "buyer", OrderSide.BUY, OrderType.MARKET, 0, 100)
    trades, remaining = engine.submit_order(market_order)
    
    # Verify trades matched in timestamp order
    assert len(trades) == 3
    assert trades[0].sell_order_id == "o1"  # Oldest first
    assert trades[1].sell_order_id == "o2"
    assert trades[2].sell_order_id == "o3"


def test_partial_fill():
    """Test T2: Partial Fill Execution"""
    engine = MatchingEngine()
    
    # Add limit sell order for 100 shares at $100
    limit_order = Order("o1", "seller", OrderSide.SELL, OrderType.LIMIT, 100.0, 100)
    engine.submit_order(limit_order)
    
    # Submit market buy order for 150 shares
    market_order = Order("m1", "buyer", OrderSide.BUY, OrderType.MARKET, 0, 150)
    trades, remaining = engine.submit_order(market_order)
    
    # Verify partial fill
    assert len(trades) == 1
    assert trades[0].quantity == 100
    assert remaining is not None
    assert remaining.remaining_quantity == 50


def test_limit_order_matching():
    """Test limit order matching logic."""
    engine = MatchingEngine()
    
    # Add limit sell at $105
    sell_order = Order("s1", "seller", OrderSide.SELL, OrderType.LIMIT, 105.0, 100)
    engine.submit_order(sell_order)
    
    # Add limit buy at $100 (should not match)
    buy_order = Order("b1", "buyer", OrderSide.BUY, OrderType.LIMIT, 100.0, 50)
    trades, remaining = engine.submit_order(buy_order)
    
    # Should not match (buy price < sell price)
    assert len(trades) == 0
    assert remaining is not None
    
    # Add limit buy at $110 (should match)
    buy_order2 = Order("b2", "buyer2", OrderSide.BUY, OrderType.LIMIT, 110.0, 50)
    trades2, remaining2 = engine.submit_order(buy_order2)
    
    # Should match
    assert len(trades2) == 1
    assert trades2[0].price == 105.0


def test_cancel_order():
    """Test order cancellation."""
    engine = MatchingEngine()
    
    # Add order
    order = Order("o1", "agent", OrderSide.BUY, OrderType.LIMIT, 100.0, 100)
    engine.submit_order(order)
    
    # Cancel order
    cancel_order = Order("c1", "agent", OrderSide.BUY, OrderType.CANCEL, 0, 0, original_order_id="o1")
    trades, remaining = engine.submit_order(cancel_order)
    
    # Verify order removed
    assert engine.get_order_book().get_best_bid() is None


def test_value_conservation():
    """Test T34: Price Conservation"""
    engine = MatchingEngine()
    
    # Add orders
    buy_order = Order("b1", "buyer", OrderSide.BUY, OrderType.LIMIT, 100.0, 100)
    sell_order = Order("s1", "seller", OrderSide.SELL, OrderType.LIMIT, 100.0, 100)
    
    engine.submit_order(buy_order)
    engine.submit_order(sell_order)
    
    # Get trades
    trades = engine.get_trades()
    
    # Verify trade value
    assert len(trades) == 1
    assert trades[0].price == 100.0
    assert trades[0].quantity == 100
