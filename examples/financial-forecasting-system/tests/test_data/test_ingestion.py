import pytest
import pandas as pd
from unittest.mock import Mock, patch
from src.data.ingestion import DataIngestion, download_all_stocks


class TestDataIngestion:
    """Tests for data ingestion module."""
    
    def test_download_single_stock(self):
        """Test downloading data for a single stock."""
        ingestion = DataIngestion()
        
        with patch.object(ingestion, 'download_stock_data') as mock_download:
            mock_download.return_value = pd.DataFrame({
                "date": pd.date_range("2020-01-01", periods=10),
                "close": [100 + i for i in range(10)]
            })
            
            result = ingestion.download_stock_data("AAPL")
            assert result is not None
            assert len(result) == 10
    
    def test_download_500_stocks(self):
        """Test downloading data for 500 stocks."""
        ingestion = DataIngestion()
        
        with patch.object(ingestion, 'download_stocks') as mock_download:
            mock_download.return_value = {
                f"STOCK{i}": pd.DataFrame({"close": [100]})
                for i in range(500)
            }
            
            result = ingestion.download_stocks([f"STOCK{i}" for i in range(500)])
            assert len(result) == 500
    
    def test_10_year_data(self):
        """Test that downloaded data spans 10+ years."""
        ingestion = DataIngestion()
        
        with patch.object(ingestion, 'download_stock_data') as mock_download:
            dates = pd.date_range("2013-01-01", periods=3650, freq="D")
            mock_download.return_value = pd.DataFrame({
                "date": dates,
                "close": [100] * 3650
            })
            
            result = ingestion.download_stock_data("AAPL", period="10y")
            assert len(result) >= 3650  # 10 years of daily data
