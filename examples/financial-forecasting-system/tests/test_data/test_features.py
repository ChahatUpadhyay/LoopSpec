import pytest
import pandas as pd
import numpy as np
from src.data.features import FeatureEngineering, engineer_features


class TestFeatureEngineering:
    """Tests for feature engineering module."""
    
    def test_technical_indicators(self):
        """Test technical indicator computation."""
        fe = FeatureEngineering()
        
        data = pd.DataFrame({
            "open": [100 + i for i in range(100)],
            "high": [105 + i for i in range(100)],
            "low": [95 + i for i in range(100)],
            "close": [100 + i for i in range(100)],
            "volume": [1000000] * 100
        })
        
        result = fe.compute_technical_indicators(data)
        assert fe.indicator_count >= 10
        assert "sma_10" in result.columns
        assert "rsi_14" in result.columns
    
    def test_volatility_features(self):
        """Test volatility feature computation."""
        fe = FeatureEngineering()
        
        data = pd.DataFrame({
            "close": [100 + i + np.random.normal(0, 1) for i in range(100)],
            "high": [105 + i for i in range(100)],
            "low": [95 + i for i in range(100)]
        })
        
        result = fe.compute_volatility_features(data)
        assert "volatility_10" in result.columns
        assert "volatility_20" in result.columns
    
    def test_macro_joins(self):
        """Test macroeconomic data joins."""
        fe = FeatureEngineering()
        
        stock_data = pd.DataFrame({
            "date": pd.date_range("2020-01-01", periods=10),
            "close": [100 + i for i in range(10)]
        })
        
        macro_data = {
            "interest_rate": pd.DataFrame({
                "date": pd.date_range("2020-01-01", periods=10),
                "rate": [0.05] * 10
            }),
            "inflation": pd.DataFrame({
                "date": pd.date_range("2020-01-01", periods=10),
                "cpi": [100 + i for i in range(10)]
            }),
            "gdp": pd.DataFrame({
                "date": pd.date_range("2020-01-01", periods=10),
                "gdp": [20000 + i * 100 for i in range(10)]
            })
        }
        
        result = fe.join_macro_data(stock_data, macro_data)
        assert "rate" in result.columns
        assert "cpi" in result.columns
        assert "gdp" in result.columns
    
    def test_sentiment_features(self):
        """Test sentiment feature integration."""
        fe = FeatureEngineering()
        
        stock_data = pd.DataFrame({
            "date": pd.date_range("2020-01-01", periods=10),
            "close": [100 + i for i in range(10)]
        })
        
        sentiment_data = pd.DataFrame({
            "date": pd.date_range("2020-01-01", periods=10),
            "sentiment": [0.5 + np.random.normal(0, 0.1) for _ in range(10)]
        })
        
        result = fe.add_sentiment_features(stock_data, sentiment_data)
        assert "sentiment" in result.columns
