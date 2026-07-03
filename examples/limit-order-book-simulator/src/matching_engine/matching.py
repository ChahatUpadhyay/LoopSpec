"""Order matching engine with price-time priority and partial fills."""

import uuid
from typing import List, Optional, Tuple
from .types import Order, OrderSide, OrderType, OrderStatus, Trade
from .order_book import OrderBook
import time


class MatchingEngine:
    """Order matching engine that processes orders against the order book."""
    
    def __init__(self):
        """Initialize matching engine."""
        self.order_book = OrderBook()
        self.trade_counter = 0
    
    def submit_order(self, order: Order) -> Tuple[List[Trade], Optional[Order]]:
        """Submit order for matching.
        
        Returns:
            Tuple of (list of trades, remaining order if unfilled)
        """
        if order.order_type == OrderType.CANCEL:
            return self._handle_cancel(order)
        elif order.order_type == OrderType.MODIFY:
            return self._handle_modify(order)
        elif order.order_type == OrderType.MARKET:
            return self._handle_market_order(order)
        else:  # LIMIT
            return self._handle_limit_order(order)
    
    def _handle_cancel(self, order: Order) -> Tuple[List[Trade], Optional[Order]]:
        """Handle cancel order."""
        cancelled_order = self.order_book.remove_order(order.original_order_id or order.order_id)
        if cancelled_order:
            cancelled_order.status = OrderStatus.CANCELLED
        return [], None
    
    def _handle_modify(self, order: Order) -> Tuple[List[Trade], Optional[Order]]:
        """Handle modify order (cancel old, add new)."""
        # Cancel original order
        self.order_book.remove_order(order.original_order_id)
        
        # Add new order as limit order
        new_order = Order(
            order_id=order.order_id,
            agent_id=order.agent_id,
            side=order.side,
            order_type=OrderType.LIMIT,
            price=order.price,
            quantity=order.quantity,
            timestamp=order.timestamp
        )
        return self._handle_limit_order(new_order)
    
    def _handle_market_order(self, order: Order) -> Tuple[List[Trade], Optional[Order]]:
        """Handle market order (immediate execution at best available price)."""
        trades = []
        
        if order.side == OrderSide.BUY:
            # Market buy: match against asks (lowest price first)
            while order.remaining_quantity > 0:
                best_ask_order = self.order_book.get_best_ask_order()
                if best_ask_order is None:
                    break  # No more asks available
                
                trade_quantity = min(order.remaining_quantity, best_ask_order.remaining_quantity)
                trade = self._execute_trade(order, best_ask_order, trade_quantity, best_ask_order.price)
                trades.append(trade)
                
                # Update quantities
                order.filled_quantity += trade_quantity
                best_ask_order.filled_quantity += trade_quantity
                
                # Remove filled order from book
                if best_ask_order.is_filled:
                    self.order_book.remove_order(best_ask_order.order_id)
                    best_ask_order.status = OrderStatus.FILLED
        else:
            # Market sell: match against bids (highest price first)
            while order.remaining_quantity > 0:
                best_bid_order = self.order_book.get_best_bid_order()
                if best_bid_order is None:
                    break  # No more bids available
                
                trade_quantity = min(order.remaining_quantity, best_bid_order.remaining_quantity)
                trade = self._execute_trade(best_bid_order, order, trade_quantity, best_bid_order.price)
                trades.append(trade)
                
                # Update quantities
                order.filled_quantity += trade_quantity
                best_bid_order.filled_quantity += trade_quantity
                
                # Remove filled order from book
                if best_bid_order.is_filled:
                    self.order_book.remove_order(best_bid_order.order_id)
                    best_bid_order.status = OrderStatus.FILLED
        
        # Update order status
        if order.is_filled:
            order.status = OrderStatus.FILLED
        elif order.filled_quantity > 0:
            order.status = OrderStatus.PARTIALLY_FILLED
        
        return trades, None if order.is_filled else order
    
    def _handle_limit_order(self, order: Order) -> Tuple[List[Trade], Optional[Order]]:
        """Handle limit order (add to book, match if possible)."""
        trades = []
        
        if order.side == OrderSide.BUY:
            # Limit buy: match against asks at or below limit price
            while order.remaining_quantity > 0:
                best_ask = self.order_book.get_best_ask()
                if best_ask is None or best_ask > order.price:
                    break  # No asks at or below limit price
                
                best_ask_order = self.order_book.get_best_ask_order()
                if best_ask_order is None:
                    break
                
                trade_quantity = min(order.remaining_quantity, best_ask_order.remaining_quantity)
                trade = self._execute_trade(order, best_ask_order, trade_quantity, best_ask)
                trades.append(trade)
                
                # Update quantities
                order.filled_quantity += trade_quantity
                best_ask_order.filled_quantity += trade_quantity
                
                # Remove filled order from book
                if best_ask_order.is_filled:
                    self.order_book.remove_order(best_ask_order.order_id)
                    best_ask_order.status = OrderStatus.FILLED
        else:
            # Limit sell: match against bids at or above limit price
            while order.remaining_quantity > 0:
                best_bid = self.order_book.get_best_bid()
                if best_bid is None or best_bid < order.price:
                    break  # No bids at or above limit price
                
                best_bid_order = self.order_book.get_best_bid_order()
                if best_bid_order is None:
                    break
                
                trade_quantity = min(order.remaining_quantity, best_bid_order.remaining_quantity)
                trade = self._execute_trade(best_bid_order, order, trade_quantity, best_bid)
                trades.append(trade)
                
                # Update quantities
                order.filled_quantity += trade_quantity
                best_bid_order.filled_quantity += trade_quantity
                
                # Remove filled order from book
                if best_bid_order.is_filled:
                    self.order_book.remove_order(best_bid_order.order_id)
                    best_bid_order.status = OrderStatus.FILLED
        
        # Add remaining order to book
        if order.remaining_quantity > 0:
            self.order_book.add_order(order)
            if order.filled_quantity > 0:
                order.status = OrderStatus.PARTIALLY_FILLED
        else:
            order.status = OrderStatus.FILLED
        
        return trades, None if order.is_filled else order
    
    def _execute_trade(self, buy_order: Order, sell_order: Order, quantity: int, price: float) -> Trade:
        """Execute a trade between buy and sell orders."""
        self.trade_counter += 1
        
        trade = Trade(
            trade_id=f"trade_{self.trade_counter}",
            buy_order_id=buy_order.order_id,
            sell_order_id=sell_order.order_id,
            price=price,
            quantity=quantity,
            timestamp=time.time(),
            buy_agent_id=buy_order.agent_id,
            sell_agent_id=sell_order.agent_id
        )
        
        self.order_book.trades.append(trade)
        return trade
    
    def get_trades(self) -> List[Trade]:
        """Get all trades."""
        return self.order_book.trades
    
    def get_order_book(self) -> OrderBook:
        """Get the order book."""
        return self.order_book
