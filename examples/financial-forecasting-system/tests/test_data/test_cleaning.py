import pytest
import pandas as pd
import numpy as np
from src.data.cleaning import DataCleaning, clean_stock_data


class TestDataCleaning:
    """Tests for data cleaning module."""
    
    def test_handle_missing_data(self):
        """Test handling of missing data."""
        cleaner = DataCleaning()
        
        data = pd.DataFrame({
            "close": [100, np.nan, 102, np.nan, 104]
        })
        
        result = cleaner.handle_missing_data(data)
        assert result.isnull().sum().sum() == 0
        assert len(result) == 5
    
    def test_stock_split_adjustment(self):
        """Test stock split adjustment."""
        cleaner = DataCleaning()
        
        data = pd.DataFrame({
            "date": pd.date_range("2020-01-01", periods=5),
            "close": [200, 200, 100, 100, 100]  # 2:1 split at day 3
        })
        
        split_ratios = {pd.Timestamp("2020-01-03"): 2.0}
        result = cleaner.adjust_for_splits(data, split_ratios)
        
        # Prices before split should be halved
        assert result.loc[0, "close"] == 100
        assert result.loc[1, "close"] == 100
        # Prices after split should be unchanged
        assert result.loc[2, "close"] == 100
    
    def test_dividend_adjustment(self):
        """Test dividend adjustment."""
        cleaner = DataCleaning()
        
        data = pd.DataFrame({
            "date": pd.date_range("2020-01-01", periods=5),
            "close": [100, 101, 102, 103, 104]
        })
        
        dividend_data = pd.DataFrame({
            "date": pd.date_range("2020-01-01", periods=5),
            "dividend": [0, 0, 1.0, 0, 0]
        })
        
        result = cleaner.adjust_for_dividends(data, dividend_data)
        assert "total_return" in result.columns
    
    def test_remove_outliers(self):
        """Test outlier removal."""
        cleaner = DataCleaning()
        
        data = pd.DataFrame({
            "close": [100, 101, 102, 1000, 103]  # 1000 is an outlier
        })
        
        result = cleaner.remove_outliers(data, columns=["close"])
        assert result.loc[3, "close"] != 1000  # Outlier should be removed
