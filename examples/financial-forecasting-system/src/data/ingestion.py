import yfinance as yf
import pandas as pd
from typing import List, Optional
from datetime import datetime, timedelta
import time
import logging

from ..utils.config import settings
from ..utils.logging import get_logger

logger = get_logger(__name__)


class DataIngestion:
    """Handle data ingestion from Yahoo Finance and Alpha Vantage."""
    
    def __init__(self):
        self.rate_limit_delay = 0.5  # Delay between API calls to respect rate limits
        self.max_retries = 3
        
    def download_stock_data(
        self,
        symbol: str,
        period: str = "10y",
        interval: str = "1d"
    ) -> Optional[pd.DataFrame]:
        """
        Download OHLCV data for a single stock.
        
        Args:
            symbol: Stock ticker symbol
            period: Time period (1y, 2y, 5y, 10y, etc.)
            interval: Data interval (1d, 1wk, 1mo)
        
        Returns:
            DataFrame with OHLCV data or None if failed
        """
        for attempt in range(self.max_retries):
            try:
                ticker = yf.Ticker(symbol)
                data = ticker.history(period=period, interval=interval)
                
                if data.empty:
                    logger.warning(f"No data returned for {symbol}")
                    return None
                
                # Reset index to make Date a column
                data = data.reset_index()
                data.columns = [col.lower() for col in data.columns]
                
                logger.info(f"Downloaded {len(data)} rows for {symbol}")
                return data
                
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed for {symbol}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.rate_limit_delay * (attempt + 1))
                else:
                    logger.error(f"Failed to download data for {symbol} after {self.max_retries} attempts")
                    return None
        
        return None
    
    def download_stocks(
        self,
        symbols: List[str],
        period: str = "10y",
        interval: str = "1d"
    ) -> dict:
        """
        Download OHLCV data for multiple stocks.
        
        Args:
            symbols: List of stock ticker symbols
            period: Time period
            interval: Data interval
        
        Returns:
            Dictionary mapping symbols to DataFrames
        """
        data_dict = {}
        successful = 0
        failed = 0
        
        logger.info(f"Starting download for {len(symbols)} stocks")
        
        for i, symbol in enumerate(symbols):
            logger.info(f"Downloading {symbol} ({i+1}/{len(symbols)})")
            
            data = self.download_stock_data(symbol, period, interval)
            
            if data is not None:
                data_dict[symbol] = data
                successful += 1
            else:
                failed += 1
            
            # Rate limiting
            time.sleep(self.rate_limit_delay)
        
        logger.info(f"Download complete: {successful} successful, {failed} failed")
        return data_dict
    
    def get_sp500_symbols(self) -> List[str]:
        """
        Get list of S&P 500 stock symbols.
        
        Returns:
            List of stock symbols
        """
        # Common S&P 500 symbols (subset for demonstration)
        # In production, this would fetch from a reliable source
        symbols = [
            "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "BRK.B",
            "JPM", "JNJ", "V", "PG", "XOM", "UNH", "HD", "MA", "BAC", "PFE",
            "CVX", "KO", "PEP", "COST", "MRK", "ABT", "AVGO", "CSCO", "LLY",
            "DHR", "ADBE", "CRM", "MCD", "NKE", "WMT", "ACN", "LIN", "ORCL",
            "CMCSA", "WFC", "QCOM", "IBM", "TXN", "NFLX", "CAT", "HON", "AMD",
            "INTC", "RTX", "VZ", "DIS", "BA", "GE", "MMM", "UPS", "GS", "BLK"
        ]
        
        # In production, would fetch full 500 stocks
        # For this implementation, we'll use a subset that can be downloaded quickly
        return symbols[:100]  # Limit to 100 for faster testing
    
    def save_data(self, data_dict: dict, output_path: str) -> None:
        """
        Save downloaded data to disk.
        
        Args:
            data_dict: Dictionary of symbol -> DataFrame
            output_path: Directory to save data
        """
        import os
        os.makedirs(output_path, exist_ok=True)
        
        for symbol, data in data_dict.items():
            filename = f"{output_path}/{symbol}.csv"
            data.to_csv(filename, index=False)
            logger.info(f"Saved {symbol} data to {filename}")


def download_all_stocks(
    num_stocks: int = None,
    period: str = "10y",
    interval: str = "1d"
) -> dict:
    """
    Download data for all configured stocks.
    
    Args:
        num_stocks: Number of stocks to download (default from settings)
        period: Time period
        interval: Data interval
    
    Returns:
        Dictionary of downloaded data
    """
    ingestion = DataIngestion()
    
    n = num_stocks or settings.num_stocks
    symbols = ingestion.get_sp500_symbols()[:n]
    
    data_dict = ingestion.download_stocks(symbols, period, interval)
    
    # Save to configured path
    ingestion.save_data(data_dict, settings.data_path)
    
    return data_dict
