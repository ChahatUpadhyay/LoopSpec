import pytest
import pandas as pd
import numpy as np
from src.backtesting.risk import RiskManagement


class TestRiskManagement:
    """Tests for risk management module."""
    
    def test_position_sizing(self):
        """Test position sizing calculation."""
        risk = RiskManagement(initial_capital=100000, max_position_size=0.1)
        
        shares = risk.calculate_position_size(signal=0.8, price=100)
        
        assert shares > 0
        assert shares * 100 <= 10000  # Max 10% of capital
    
    def test_stop_loss(self):
        """Test stop-loss trigger."""
        risk = RiskManagement(stop_loss_percentage=0.05)
        
        position = {
            "entry_price": 100,
            "direction": "long"
        }
        
        # Should trigger at 95 (5% below entry)
        assert risk.check_stop_loss(position, 95) == True
        # Should not trigger at 98
        assert risk.check_stop_loss(position, 98) == False
    
    def test_portfolio_metrics(self):
        """Test portfolio metrics calculation."""
        risk = RiskManagement(initial_capital=100000)
        
        trades = pd.DataFrame({
            "net_pnl": [1000, -500, 2000, -300, 1500]
        })
        
        metrics = risk.calculate_portfolio_metrics(trades)
        
        assert "total_return" in metrics
        assert "sharpe_ratio" in metrics
        assert "max_drawdown" in metrics
        assert "win_rate" in metrics
