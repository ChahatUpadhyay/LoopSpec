import pytest
import pandas as pd
import numpy as np
from src.backtesting.costs import TransactionCosts


class TestTransactionCosts:
    """Tests for transaction costs module."""
    
    def test_slippage(self):
        """Test slippage application."""
        costs = TransactionCosts(slippage_percentage=0.001)
        
        trades = pd.DataFrame({
            "price": [100, 101, 102],
            "direction": ["buy", "sell", "buy"]
        })
        
        result = costs.apply_slippage(trades)
        
        assert "slippage_adjusted_price" in result.columns
        # Buy orders should have higher prices
        assert result.loc[0, "slippage_adjusted_price"] > 100
    
    def test_commission(self):
        """Test commission application."""
        costs = TransactionCosts(commission_per_trade=0.001)
        
        trades = pd.DataFrame({
            "price": [100, 101, 102],
            "quantity": [10, 10, 10]
        })
        
        result = costs.apply_commission(trades)
        
        assert "commission" in result.columns
        assert "net_pnl" in result.columns
        assert (result["commission"] > 0).all()
    
    def test_total_costs(self):
        """Test total cost calculation."""
        costs = TransactionCosts()
        
        trades = pd.DataFrame({
            "price": [100, 101, 102],
            "quantity": [10, 10, 10]
        })
        
        trades = costs.apply_commission(trades)
        total_costs = costs.calculate_total_costs(trades)
        
        assert "total_commission" in total_costs
        assert "total_costs" in total_costs
