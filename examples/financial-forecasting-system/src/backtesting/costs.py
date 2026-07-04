import pandas as pd
import numpy as np
from typing import Dict, Optional
import logging

from ..utils.logging import get_logger

logger = get_logger(__name__)


class TransactionCosts:
    """Handle transaction costs including slippage and commissions."""
    
    def __init__(
        self,
        commission_per_trade: float = 0.001,
        slippage_percentage: float = 0.0001
    ):
        """
        Initialize transaction costs.
        
        Args:
            commission_per_trade: Commission rate per trade (as decimal)
            slippage_percentage: Slippage rate (as decimal)
        """
        self.commission_per_trade = commission_per_trade
        self.slippage_percentage = slippage_percentage
        
    def apply_slippage(
        self,
        trades: pd.DataFrame,
        slippage_percentage: Optional[float] = None
    ) -> pd.DataFrame:
        """
        Apply slippage to trade prices.
        
        Args:
            trades: DataFrame with trade data
            slippage_percentage: Custom slippage rate (uses default if None)
        
        Returns:
            DataFrame with slippage-adjusted prices
        """
        df = trades.copy()
        slippage = slippage_percentage or self.slippage_percentage
        
        if "price" not in df.columns:
            raise ValueError("Trades DataFrame must have 'price' column")
        
        # Apply slippage based on trade direction
        if "direction" in df.columns:
            # For buy orders, price increases (worse execution)
            # For sell orders, price decreases (worse execution)
            df["slippage_adjusted_price"] = df["price"] * (
                1 + slippage * np.where(df["direction"] == "buy", 1, -1)
            )
        else:
            # Apply slippage in both directions if no direction specified
            df["slippage_adjusted_price"] = df["price"] * (1 + slippage)
        
        logger.info(f"Applied {slippage*100:.2f}% slippage to {len(df)} trades")
        return df
    
    def apply_commission(
        self,
        trades: pd.DataFrame,
        commission_rate: Optional[float] = None
    ) -> pd.DataFrame:
        """
        Apply commission to trade P&L.
        
        Args:
            trades: DataFrame with trade data
            commission_rate: Custom commission rate (uses default if None)
        
        Returns:
            DataFrame with commission-adjusted P&L
        """
        df = trades.copy()
        commission = commission_rate or self.commission_per_trade
        
        if "price" not in df.columns or "quantity" not in df.columns:
            raise ValueError("Trades DataFrame must have 'price' and 'quantity' columns")
        
        # Calculate trade value
        df["trade_value"] = df["price"] * df["quantity"]
        
        # Calculate commission
        df["commission"] = df["trade_value"] * commission
        
        # Calculate net P&L after commission
        if "pnl" in df.columns:
            df["net_pnl"] = df["pnl"] - df["commission"]
        else:
            df["net_pnl"] = -df["commission"]
        
        logger.info(f"Applied {commission*100:.2f}% commission to {len(df)} trades")
        return df
    
    def calculate_total_costs(
        self,
        trades: pd.DataFrame
    ) -> Dict[str, float]:
        """
        Calculate total transaction costs.
        
        Args:
            trades: DataFrame with trade data
        
        Returns:
            Dictionary with cost breakdown
        """
        if "commission" not in trades.columns:
            trades = self.apply_commission(trades)
        
        total_commission = trades["commission"].sum()
        total_slippage_cost = 0
        
        if "slippage_adjusted_price" in trades.columns and "price" in trades.columns:
            total_slippage_cost = (
                (trades["slippage_adjusted_price"] - trades["price"]) * trades["quantity"]
            ).abs().sum()
        
        total_costs = total_commission + total_slippage_cost
        
        return {
            "total_commission": total_commission,
            "total_slippage_cost": total_slippage_cost,
            "total_costs": total_costs
        }
