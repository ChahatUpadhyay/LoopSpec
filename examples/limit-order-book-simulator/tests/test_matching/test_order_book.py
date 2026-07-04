"""Unit tests for order book state management."""

import pytest
import time
from matching_engine.order_book import OrderBook
from matching_engine.types import Order, OrderSide, OrderType, OrderStatus


def test_order_queue():
    """Test T3: Order Queue Maintenance"""
    book = OrderBook()
    
    # Submit multiple orders at same price
    order1 = Order("o1", "a1", OrderSide.BUY, OrderType.LIMIT, 100.0, 50, timestamp=1.0)
    order2 = Order("o2", "a2", OrderSide.BUY, OrderType.LIMIT, 100.0, 30, timestamp=2.0)
    order3 = Order("o3", "a3", OrderSide.BUY, OrderType.LIMIT, 100.0, 20, timestamp=3.0)
    
    book.add_order(order1)
    book.add_order(order2)
    book.add_order(order3)
    
    # Verify queue length
    assert len(book.bids[100.0]) == 3
    
    # Verify order in correct position (FIFO)
    best_order = book.get_best_bid_order()
    assert best_order.order_id == "o1"
    assert best_order.quantity == 50


def test_spread_calculation():
    """Test T4: Bid/Ask Spread Calculation"""
    book = OrderBook()
    
    # Add bid at $99
    bid_order = Order("o1", "a1", OrderSide.BUY, OrderType.LIMIT, 99.0, 100)
    book.add_order(bid_order)
    
    # Add ask at $101
    ask_order = Order("o2", "a2", OrderSide.SELL, OrderType.LIMIT, 101.0, 100)
    book.add_order(ask_order)
    
    # Calculate spread
    spread = book.get_spread()
    assert spread == 2.0


def test_book_consistency():
    """Test T33: No Book Inconsistency"""
    book = OrderBook()
    
    # Add various orders
    for i in range(10):
        bid_order = Order(f"b{i}", f"a{i}", OrderSide.BUY, OrderType.LIMIT, 100.0 - i, 100)
        ask_order = Order(f"s{i}", f"a{i}", OrderSide.SELL, OrderType.LIMIT, 100.0 + i, 100)
        book.add_order(bid_order)
        book.add_order(ask_order)
    
    # Validate book state
    assert book.validate() == True
    
    # No negative quantities
    for order in book.orders.values():
        assert order.quantity >= 0
        assert order.filled_quantity >= 0
        assert order.filled_quantity <= order.quantity


def test_book_depth():
    """Test order book depth tracking."""
    book = OrderBook()
    
    # Add orders at different price levels
    book.add_order(Order("o1", "a1", OrderSide.BUY, OrderType.LIMIT, 99.0, 100))
    book.add_order(Order("o2", "a2", OrderSide.BUY, OrderType.LIMIT, 98.0, 50))
    book.add_order(Order("o3", "a3", OrderSide.SELL, OrderType.LIMIT, 101.0, 75))
    book.add_order(Order("o4", "a4", OrderSide.SELL, OrderType.LIMIT, 102.0, 25))
    
    # Check depth
    assert book.get_bid_depth() == 150
    assert book.get_ask_depth() == 100
