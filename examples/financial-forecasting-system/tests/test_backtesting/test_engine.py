import pytest
import pandas as pd
import numpy as np
from src.backtesting.engine import BacktestEngine, run_backtest


class TestBacktestEngine:
    """Tests for backtesting engine."""
    
    def test_latency_simulation(self):
        """Test latency simulation."""
        engine = BacktestEngine()
        
        from datetime import datetime, timedelta
        execution_time = datetime(2020, 1, 1, 10, 0, 0)
        
        actual_time = engine.simulate_latency(execution_time, latency_ms=100)
        
        assert actual_time > execution_time
        assert actual_time == execution_time + timedelta(milliseconds=100)
    
    def test_backtest_run(self):
        """Test backtest execution."""
        engine = BacktestEngine(initial_capital=100000)
        
        data = pd.DataFrame({
            "date": pd.date_range("2020-01-01", periods=50),
            "close": [100 + i for i in range(50)]
        })
        
        predictions = np.random.randn(50)
        
        trades_df = engine.run_backtest(data, predictions)
        
        assert trades_df is not None
        assert len(trades_df) >= 0
    
    def test_backtest_metrics(self):
        """Test backtest metrics calculation."""
        engine = BacktestEngine(initial_capital=100000)
        
        trades_df = pd.DataFrame({
            "net_pnl": [100, -50, 200, -30, 150]
        })
        
        metrics = engine.calculate_metrics(trades_df)
        
        assert "total_return" in metrics
        assert "sharpe_ratio" in metrics
        assert "max_drawdown" in metrics
