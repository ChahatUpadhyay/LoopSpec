import pandas as pd
import numpy as np
import pandas_ta as ta
from typing import Optional, Dict, List
import logging

from ..utils.logging import get_logger

logger = get_logger(__name__)


class FeatureEngineering:
    """Handle feature engineering for financial time series."""
    
    def __init__(self):
        self.indicator_count = 0
    
    def compute_technical_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Compute technical indicators using pandas-ta.
        
        Args:
            data: DataFrame with OHLCV data
        
        Returns:
            DataFrame with technical indicators
        """
        df = data.copy()
        
        # Ensure required columns exist
        required_cols = ["open", "high", "low", "close", "volume"]
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        
        # Moving Averages
        df["sma_10"] = ta.sma(df["close"], length=10)
        df["sma_20"] = ta.sma(df["close"], length=20)
        df["sma_50"] = ta.sma(df["close"], length=50)
        df["ema_12"] = ta.ema(df["close"], length=12)
        df["ema_26"] = ta.ema(df["close"], length=26)
        
        # RSI
        df["rsi_14"] = ta.rsi(df["close"], length=14)
        
        # MACD
        macd = ta.macd(df["close"])
        df["macd"] = macd["MACD_12_26_9"]
        df["macd_signal"] = macd["MACDh_12_26_9"]
        df["macd_hist"] = macd["MACDs_12_26_9"]
        
        # Bollinger Bands
        bb = ta.bbands(df["close"], length=20)
        df["bb_upper"] = bb["BBU_20_2.0"]
        df["bb_middle"] = bb["BBM_20_2.0"]
        df["bb_lower"] = bb["BBL_20_2.0"]
        df["bb_width"] = (df["bb_upper"] - df["bb_lower"]) / df["bb_middle"]
        
        # ATR (Average True Range)
        df["atr_14"] = ta.atr(df["high"], df["low"], df["close"], length=14)
        
        # Stochastic Oscillator
        stoch = ta.stoch(df["high"], df["low"], df["close"])
        df["stoch_k"] = stoch["STOCHk_14_3_3"]
        df["stoch_d"] = stoch["STOCHd_14_3_3"]
        
        # Volume indicators
        df["volume_sma_20"] = ta.sma(df["volume"], length=20)
        df["volume_ratio"] = df["volume"] / df["volume_sma_20"]
        
        # Price momentum
        df["momentum_10"] = ta.mom(df["close"], length=10)
        df["roc_10"] = ta.roc(df["close"], length=10)
        
        # Count indicators
        self.indicator_count = len([col for col in df.columns if col not in required_cols])
        logger.info(f"Computed {self.indicator_count} technical indicators")
        
        return df
    
    def compute_volatility_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Compute volatility clustering features.
        
        Args:
            data: DataFrame with OHLCV data
        
        Returns:
            DataFrame with volatility features
        """
        df = data.copy()
        
        # Realized volatility (rolling standard deviation of returns)
        if "close" in df.columns:
            df["returns"] = df["close"].pct_change()
            df["volatility_10"] = df["returns"].rolling(window=10).std()
            df["volatility_20"] = df["returns"].rolling(window=20).std()
            df["volatility_50"] = df["returns"].rolling(window=50).std()
            
            # GARCH-like features (simplified)
            df["volatility_ratio"] = df["volatility_10"] / df["volatility_50"]
            df["volatility_trend"] = df["volatility_10"] - df["volatility_20"]
            
            # Parkinson's volatility estimator
            if "high" in df.columns and "low" in df.columns:
                df["parkinson_vol"] = np.sqrt(
                    (1 / (4 * np.log(2))) * 
                    np.log(df["high"] / df["low"])**2
                )
        
        logger.info("Computed volatility features")
        return df
    
    def join_macro_data(
        self,
        stock_data: pd.DataFrame,
        macro_data: Dict[str, pd.DataFrame] = None
    ) -> pd.DataFrame:
        """
        Join macroeconomic data to stock data.
        
        Args:
            stock_data: DataFrame with stock data
            macro_data: Dictionary of macro indicator name -> DataFrame
        
        Returns:
            DataFrame with macro data joined
        """
        df = stock_data.copy()
        
        if macro_data is None or len(macro_data) == 0:
            logger.info("No macro data to join")
            return df
        
        # Ensure date column exists
        if "date" not in df.columns:
            df = df.reset_index()
            df = df.rename(columns={df.columns[0]: "date"})
        
        df["date"] = pd.to_datetime(df["date"])
        
        # Join each macro indicator
        for indicator_name, macro_df in macro_data.items():
            if "date" in macro_df.columns:
                macro_df["date"] = pd.to_datetime(macro_df["date"])
                df = df.merge(macro_df, on="date", how="left")
                logger.info(f"Joined {indicator_name} to stock data")
        
        return df
    
    def add_sentiment_features(
        self,
        stock_data: pd.DataFrame,
        sentiment_data: pd.DataFrame = None
    ) -> pd.DataFrame:
        """
        Add sentiment features to stock data.
        
        Args:
            stock_data: DataFrame with stock data
            sentiment_data: DataFrame with sentiment scores
        
        Returns:
            DataFrame with sentiment features
        """
        df = stock_data.copy()
        
        if sentiment_data is None or sentiment_data.empty:
            logger.info("No sentiment data to add")
            return df
        
        # Ensure date column exists
        if "date" not in df.columns:
            df = df.reset_index()
            df = df.rename(columns={df.columns[0]: "date"})
        
        df["date"] = pd.to_datetime(df["date"])
        
        if "date" in sentiment_data.columns:
            sentiment_data["date"] = pd.to_datetime(sentiment_data["date"])
            df = df.merge(sentiment_data, on="date", how="left")
            logger.info("Added sentiment features")
        
        return df
    
    def create_lag_features(
        self,
        data: pd.DataFrame,
        columns: List[str] = None,
        lags: List[int] = [1, 2, 3, 5, 10]
    ) -> pd.DataFrame:
        """
        Create lag features for time series.
        
        Args:
            data: DataFrame with time series data
            columns: Columns to create lags for
            lags: Lag periods to create
        
        Returns:
            DataFrame with lag features
        """
        df = data.copy()
        
        if columns is None:
            columns = ["close", "volume", "returns"]
        
        columns = [col for col in columns if col in df.columns]
        
        for col in columns:
            for lag in lags:
                df[f"{col}_lag_{lag}"] = df[col].shift(lag)
        
        logger.info(f"Created lag features for {len(columns)} columns")
        return df
    
    def create_rolling_features(
        self,
        data: pd.DataFrame,
        columns: List[str] = None,
        windows: List[int] = [5, 10, 20, 50]
    ) -> pd.DataFrame:
        """
        Create rolling window features.
        
        Args:
            data: DataFrame with time series data
            columns: Columns to create rolling features for
            windows: Window sizes
        
        Returns:
            DataFrame with rolling features
        """
        df = data.copy()
        
        if columns is None:
            columns = ["close", "volume"]
        
        columns = [col for col in columns if col in df.columns]
        
        for col in columns:
            for window in windows:
                df[f"{col}_mean_{window}"] = df[col].rolling(window=window).mean()
                df[f"{col}_std_{window}"] = df[col].rolling(window=window).std()
                df[f"{col}_min_{window}"] = df[col].rolling(window=window).min()
                df[f"{col}_max_{window}"] = df[col].rolling(window=window).max()
        
        logger.info(f"Created rolling features for {len(columns)} columns")
        return df
    
    def engineer_features(
        self,
        data: pd.DataFrame,
        technical: bool = True,
        volatility: bool = True,
        lags: bool = True,
        rolling: bool = True
    ) -> pd.DataFrame:
        """
        Apply complete feature engineering pipeline.
        
        Args:
            data: Cleaned DataFrame
            technical: Compute technical indicators
            volatility: Compute volatility features
            lags: Create lag features
            rolling: Create rolling features
        
        Returns:
            DataFrame with all features
        """
        logger.info("Starting feature engineering pipeline")
        
        if technical:
            data = self.compute_technical_indicators(data)
        
        if volatility:
            data = self.compute_volatility_features(data)
        
        if lags:
            data = self.create_lag_features(data)
        
        if rolling:
            data = self.create_rolling_features(data)
        
        # Remove rows with NaN from lag/rolling features
        data = data.dropna()
        
        logger.info(f"Feature engineering complete: {len(data)} rows, {len(data.columns)} features")
        return data


def engineer_features(data: pd.DataFrame) -> pd.DataFrame:
    """
    Convenience function for feature engineering.
    
    Args:
        data: Cleaned DataFrame
    
    Returns:
        DataFrame with engineered features
    """
    fe = FeatureEngineering()
    return fe.engineer_features(data)
