import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging

from .costs import TransactionCosts
from .risk import RiskManagement
from ..utils.logging import get_logger
from ..utils.config import settings

logger = get_logger(__name__)


class BacktestEngine:
    """Walk-forward backtesting engine with realistic simulation."""
    
    def __init__(
        self,
        initial_capital: float = None,
        commission_per_trade: float = None,
        slippage_percentage: float = None
    ):
        """
        Initialize backtesting engine.
        
        Args:
            initial_capital: Initial capital for backtest
            commission_per_trade: Commission rate
            slippage_percentage: Slippage rate
        """
        self.initial_capital = initial_capital or settings.initial_capital
        self.commission_per_trade = commission_per_trade or settings.commission_per_trade
        self.slippage_percentage = slippage_percentage or settings.slippage_percentage
        
        self.costs = TransactionCosts(self.commission_per_trade, self.slippage_percentage)
        self.risk = RiskManagement(self.initial_capital)
        
        self.trades = []
        self.portfolio_value = []
        
    def simulate_latency(
        self,
        execution_time: datetime,
        latency_ms: int = 100
    ) -> datetime:
        """
        Simulate order execution latency.
        
        Args:
            execution_time: Desired execution time
            latency_ms: Latency in milliseconds
        
        Returns:
            Actual execution time with latency
        """
        return execution_time + timedelta(milliseconds=latency_ms)
    
    def execute_trade(
        self,
        signal: float,
        price: float,
        timestamp: datetime,
        latency_ms: int = 100
    ) -> Optional[Dict]:
        """
        Execute a trade with realistic simulation.
        
        Args:
            signal: Trading signal (-1 to 1)
            price: Execution price
            timestamp: Trade timestamp
            latency_ms: Execution latency
        
        Returns:
            Trade dictionary or None if no trade
        """
        # Apply latency
        execution_time = self.simulate_latency(timestamp, latency_ms)
        
        # Calculate position size
        if abs(signal) < 0.1:  # Minimum signal threshold
            return None
        
        direction = "buy" if signal > 0 else "sell"
        quantity = self.risk.calculate_position_size(signal, price)
        
        if quantity <= 0:
            return None
        
        # Create trade record
        trade = {
            "timestamp": execution_time,
            "direction": direction,
            "price": price,
            "quantity": quantity,
            "signal": signal,
            "latency_ms": latency_ms
        }
        
        self.trades.append(trade)
        logger.info(f"Executed {direction} {quantity} shares at ${price:.2f}")
        
        return trade
    
    def run_backtest(
        self,
        data: pd.DataFrame,
        predictions: np.ndarray,
        latency_ms: int = 100
    ) -> pd.DataFrame:
        """
        Run walk-forward backtest.
        
        Args:
            data: DataFrame with price data
            predictions: Model predictions
            latency_ms: Execution latency
        
        Returns:
            DataFrame with backtest results
        """
        logger.info("Starting backtest")
        
        self.trades = []
        self.portfolio_value = [self.initial_capital]
        
        # Ensure data and predictions align
        if len(data) != len(predictions):
            raise ValueError("Data and predictions must have same length")
        
        # Walk-forward simulation
        for i in range(len(data)):
            row = data.iloc[i]
            prediction = predictions[i]
            
            # Get price
            if "close" in row:
                price = row["close"]
            else:
                price = row.get("price", row.get("mid", 0))
            
            # Get timestamp
            if "date" in row:
                timestamp = pd.to_datetime(row["date"])
            else:
                timestamp = row.name if hasattr(row.name, 'to_pydatetime') else datetime.now()
            
            # Execute trade based on prediction
            trade = self.execute_trade(prediction, price, timestamp, latency_ms)
            
            # Update portfolio value (simplified)
            if trade:
                # Calculate P&L (simplified - would need full position tracking)
                trade["pnl"] = 0  # Placeholder
                self.risk.update_capital(trade["pnl"])
            
            self.portfolio_value.append(self.risk.current_capital)
        
        # Convert trades to DataFrame
        trades_df = pd.DataFrame(self.trades)
        
        # Apply transaction costs
        if not trades_df.empty:
            trades_df = self.costs.apply_slippage(trades_df)
            trades_df = self.costs.apply_commission(trades_df)
        
        logger.info(f"Backtest complete: {len(self.trades)} trades executed")
        return trades_df
    
    def calculate_metrics(
        self,
        trades_df: pd.DataFrame
    ) -> Dict[str, float]:
        """
        Calculate backtest performance metrics.
        
        Args:
            trades_df: DataFrame with trade history
        
        Returns:
            Dictionary with performance metrics
        """
        metrics = self.risk.calculate_portfolio_metrics(trades_df)
        
        # Add additional metrics
        if not trades_df.empty:
            metrics["total_trades"] = len(trades_df)
            metrics["avg_trade_pnl"] = trades_df.get("net_pnl", pd.Series([0])).mean()
            metrics["total_costs"] = self.costs.calculate_total_costs(trades_df)["total_costs"]
        
        return metrics
    
    def generate_report(self, metrics: Dict[str, float]) -> str:
        """
        Generate backtest report.
        
        Args:
            metrics: Performance metrics
        
        Returns:
        """
        report = f"""
        Backtest Report
        ===============
        Total Return: {metrics.get('total_return', 0):.2%}
        Sharpe Ratio: {metrics.get('sharpe_ratio', 0):.2f}
        Max Drawdown: {metrics.get('max_drawdown', 0):.2%}
        Win Rate: {metrics.get('win_rate', 0):.2%}
        Total Trades: {metrics.get('total_trades', 0)}
        Total Costs: ${metrics.get('total_costs', 0):.2f}
        """
        return report


def run_backtest(
    data: pd.DataFrame,
    predictions: np.ndarray,
    initial_capital: float = 100000.0
) -> Tuple[pd.DataFrame, Dict[str, float]]:
    """
    Convenience function to run backtest.
    
    Args:
        data: Price data
        predictions: Model predictions
        initial_capital: Initial capital
    
    Returns:
        Tuple of (trades_df, metrics)
    """
    engine = BacktestEngine(initial_capital=initial_capital)
    trades_df = engine.run_backtest(data, predictions)
    metrics = engine.calculate_metrics(trades_df)
    
    return trades_df, metrics
