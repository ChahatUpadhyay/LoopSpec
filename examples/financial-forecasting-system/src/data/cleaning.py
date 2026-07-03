import pandas as pd
import numpy as np
from typing import Optional, Tuple
import logging

from ..utils.logging import get_logger

logger = get_logger(__name__)


class DataCleaning:
    """Handle data cleaning, missing values, splits, and dividends."""
    
    def __init__(self):
        self.fill_method = "ffill"  # Forward fill for missing values
    
    def handle_missing_data(
        self,
        data: pd.DataFrame,
        method: str = "ffill"
    ) -> pd.DataFrame:
        """
        Handle missing data in OHLCV dataset.
        
        Args:
            data: DataFrame with OHLCV data
            method: Fill method (ffill, bfill, interpolate, drop)
        
        Returns:
            Cleaned DataFrame
        """
        df = data.copy()
        
        # Check for missing values
        missing_count = df.isnull().sum()
        if missing_count.sum() > 0:
            logger.info(f"Missing values found: {missing_count.to_dict()}")
        
        # Handle missing values based on method
        if method == "ffill":
            df = df.fillna(method="ffill").fillna(method="bfill")
        elif method == "bfill":
            df = df.fillna(method="bfill").fillna(method="ffill")
        elif method == "interpolate":
            df = df.interpolate(method="time")
        elif method == "drop":
            df = df.dropna()
        else:
            raise ValueError(f"Unknown fill method: {method}")
        
        # If still have missing values, drop rows
        if df.isnull().sum().sum() > 0:
            logger.warning("Still have missing values after fill, dropping rows")
            df = df.dropna()
        
        logger.info(f"Cleaned data: {len(df)} rows after handling missing values")
        return df
    
    def adjust_for_splits(
        self,
        data: pd.DataFrame,
        split_ratios: dict = None
    ) -> pd.DataFrame:
        """
        Adjust prices for stock splits.
        
        Args:
            data: DataFrame with OHLCV data
            split_ratios: Dictionary of date -> split ratio
        
        Returns:
            DataFrame with split-adjusted prices
        """
        df = data.copy()
        
        if split_ratios is None or len(split_ratios) == 0:
            logger.info("No split adjustments needed")
            return df
        
        # Ensure date column is datetime
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
        else:
            df = df.rename(columns={df.columns[0]: "date"})
            df["date"] = pd.to_datetime(df["date"])
        
        # Apply split adjustments
        for split_date, ratio in split_ratios.items():
            split_date = pd.to_datetime(split_date)
            mask = df["date"] < split_date
            
            # Adjust price columns
            price_cols = ["open", "high", "low", "close"]
            for col in price_cols:
                if col in df.columns:
                    df.loc[mask, col] = df.loc[mask, col] / ratio
            
            # Adjust volume
            if "volume" in df.columns:
                df.loc[mask, "volume"] = df.loc[mask, "volume"] * ratio
            
            logger.info(f"Applied split adjustment: {split_date} ratio {ratio}")
        
        return df
    
    def adjust_for_dividends(
        self,
        data: pd.DataFrame,
        dividend_data: pd.DataFrame = None
    ) -> pd.DataFrame:
        """
        Adjust returns for dividends.
        
        Args:
            data: DataFrame with OHLCV data
            dividend_data: DataFrame with dividend payments
        
        Returns:
            DataFrame with dividend-adjusted returns
        """
        df = data.copy()
        
        if dividend_data is None or dividend_data.empty:
            logger.info("No dividend adjustments needed")
            return df
        
        # Calculate total return including dividends
        if "close" in df.columns:
            df["daily_return"] = df["close"].pct_change()
            
            # Add dividend yield to return on dividend days
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
                dividend_data["date"] = pd.to_datetime(dividend_data["date"])
                
                # Merge dividend data
                df = df.merge(dividend_data, on="date", how="left")
                
                if "dividend" in df.columns:
                    df["dividend"] = df["dividend"].fillna(0)
                    df["total_return"] = df["daily_return"] + (df["dividend"] / df["close"])
                    logger.info("Added dividend-adjusted returns")
        
        return df
    
    def remove_outliers(
        self,
        data: pd.DataFrame,
        columns: list = None,
        method: str = "iqr",
        threshold: float = 3.0
    ) -> pd.DataFrame:
        """
        Remove outliers from data.
        
        Args:
            data: DataFrame with OHLCV data
            columns: Columns to check for outliers
            method: Outlier detection method (iqr, zscore)
            threshold: Threshold for outlier detection
        
        Returns:
            DataFrame with outliers removed
        """
        df = data.copy()
        
        if columns is None:
            columns = ["open", "high", "low", "close", "volume"]
        
        columns = [col for col in columns if col in df.columns]
        
        if method == "iqr":
            for col in columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                
                outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
                if outliers > 0:
                    logger.info(f"Removed {outliers} outliers from {col} using IQR method")
                    df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        
        elif method == "zscore":
            for col in columns:
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                outliers = (z_scores > threshold).sum()
                if outliers > 0:
                    logger.info(f"Removed {outliers} outliers from {col} using Z-score method")
                    df = df[z_scores <= threshold]
        
        return df
    
    def clean_data(
        self,
        data: pd.DataFrame,
        handle_missing: bool = True,
        handle_splits: bool = False,
        handle_dividends: bool = False,
        remove_outliers: bool = True
    ) -> pd.DataFrame:
        """
        Apply all cleaning steps to data.
        
        Args:
            data: Raw DataFrame
            handle_missing: Handle missing values
            handle_splits: Adjust for stock splits
            handle_dividends: Adjust for dividends
            remove_outliers: Remove outliers
        
        Returns:
            Cleaned DataFrame
        """
        logger.info("Starting data cleaning process")
        
        if handle_missing:
            data = self.handle_missing_data(data)
        
        if handle_splits:
            data = self.adjust_for_splits(data)
        
        if handle_dividends:
            data = self.adjust_for_dividends(data)
        
        if remove_outliers:
            data = self.remove_outliers(data)
        
        logger.info(f"Data cleaning complete: {len(data)} rows")
        return data


def clean_stock_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Convenience function to clean stock data.
    
    Args:
        data: Raw DataFrame
    
    Returns:
        Cleaned DataFrame
    """
    cleaner = DataCleaning()
    return cleaner.clean_data(data)
