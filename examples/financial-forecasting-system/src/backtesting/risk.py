import pandas as pd
import numpy as np
from typing import Optional, Dict
import logging

from ..utils.logging import get_logger

logger = get_logger(__name__)


class RiskManagement:
    """Handle position sizing and stop-loss logic."""
    
    def __init__(
        self,
        initial_capital: float = 100000.0,
        max_position_size: float = 0.1,
        stop_loss_percentage: float = 0.05
    ):
        """
        Initialize risk management parameters.
        
        Args:
            initial_capital: Initial capital
            max_position_size: Maximum position size as fraction of capital
            stop_loss_percentage: Stop-loss percentage
        """
        self.initial_capital = initial_capital
        self.max_position_size = max_position_size
        self.stop_loss_percentage = stop_loss_percentage
        self.current_capital = initial_capital
        
    def calculate_position_size(
        self,
        signal: float,
        price: float,
        strategy: str = "fixed_fractional",
        volatility: Optional[float] = None
    ) -> int:
        """
        Calculate position size based on risk management rules.
        
        Args:
            signal: Trading signal (-1 to 1)
            price: Current price
            strategy: Position sizing strategy
            volatility: Current volatility (for volatility-based sizing)
        
        Returns:
            Number of shares to trade
        """
        max_investment = self.current_capital * self.max_position_size
        
        if strategy == "fixed_fractional":
            # Fixed fraction of capital
            position_value = max_investment * abs(signal)
            shares = int(position_value / price)
            
        elif strategy == "kelly_criterion":
            # Kelly criterion (simplified)
            if volatility is None:
                volatility = 0.2  # Default volatility
            
            win_rate = 0.55  # Assumed win rate
            avg_win_loss_ratio = 1.5  # Assumed win/loss ratio
            
            kelly_fraction = (win_rate * avg_win_loss_ratio - (1 - win_rate)) / avg_win_loss_ratio
            kelly_fraction = max(0, min(kelly_fraction, 0.25))  # Cap at 25%
            
            position_value = self.current_capital * kelly_fraction * abs(signal)
            shares = int(position_value / price)
            
        elif strategy == "volatility_based":
            # Volatility-based position sizing
            if volatility is None:
                volatility = 0.2
            
            target_risk = 0.02  # 2% risk per trade
            position_value = (target_risk * self.current_capital) / volatility
            position_value = min(position_value, max_investment)
            shares = int(position_value / price)
            
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
        
        logger.info(f"Position size: {shares} shares at ${price:.2f}")
        return shares
    
    def check_stop_loss(
        self,
        position: Dict[str, float],
        current_price: float,
        stop_loss_percentage: Optional[float] = None
    ) -> bool:
        """
        Check if stop-loss should be triggered.
        
        Args:
            position: Position dictionary with entry_price, direction, etc.
            current_price: Current market price
            stop_loss_percentage: Custom stop-loss percentage
        
        Returns:
            True if stop-loss should be triggered
        """
        stop_loss = stop_loss_percentage or self.stop_loss_percentage
        
        entry_price = position.get("entry_price", 0)
        direction = position.get("direction", "long")
        
        if direction == "long":
            # For long positions, stop-loss is below entry price
            stop_price = entry_price * (1 - stop_loss)
            triggered = current_price <= stop_price
        else:
            # For short positions, stop-loss is above entry price
            stop_price = entry_price * (1 + stop_loss)
            triggered = current_price >= stop_price
        
        if triggered:
            logger.info(f"Stop-loss triggered at ${current_price:.2f} (stop: ${stop_price:.2f})")
        
        return triggered
    
    def update_capital(self, pnl: float) -> None:
        """
        Update current capital after trade.
        
        Args:
            pnl: Profit/loss from trade
        """
        self.current_capital += pnl
        logger.info(f"Capital updated: ${self.current_capital:.2f} (P&L: ${pnl:.2f})")
    
    def calculate_portfolio_metrics(
        self,
        trades: pd.DataFrame
    ) -> Dict[str, float]:
        """
        Calculate portfolio performance metrics.
        
        Args:
            trades: DataFrame with trade history
        
        Returns:
            Dictionary with portfolio metrics
        """
        if trades.empty:
            return {
                "total_return": 0.0,
                "sharpe_ratio": 0.0,
                "max_drawdown": 0.0,
                "win_rate": 0.0
            }
        
        # Calculate returns
        if "net_pnl" in trades.columns:
            returns = trades["net_pnl"]
        else:
            returns = trades.get("pnl", pd.Series([0]))
        
        total_return = returns.sum() / self.initial_capital
        
        # Calculate Sharpe ratio (simplified)
        if len(returns) > 1:
            sharpe_ratio = returns.mean() / returns.std() * np.sqrt(252) if returns.std() > 0 else 0
        else:
            sharpe_ratio = 0
        
        # Calculate max drawdown
        cumulative = returns.cumsum()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / self.initial_capital
        max_drawdown = drawdown.min()
        
        # Calculate win rate
        winning_trades = (returns > 0).sum()
        total_trades = len(returns)
        win_rate = winning_trades / total_trades if total_trades > 0 else 0
        
        return {
            "total_return": total_return,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": max_drawdown,
            "win_rate": win_rate
        }
