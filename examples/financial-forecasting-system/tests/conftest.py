import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


@pytest.fixture
def sample_ohlcv_data():
    """Generate sample OHLCV data for testing."""
    dates = pd.date_range(start="2020-01-01", periods=100, freq="D")
    np.random.seed(42)
    
    base_price = 100
    returns = np.random.normal(0.001, 0.02, 100)
    prices = base_price * (1 + returns).cumprod()
    
    data = pd.DataFrame({
        "date": dates,
        "open": prices * (1 + np.random.normal(0, 0.005, 100)),
        "high": prices * (1 + np.abs(np.random.normal(0, 0.01, 100))),
        "low": prices * (1 - np.abs(np.random.normal(0, 0.01, 100))),
        "close": prices,
        "volume": np.random.randint(1000000, 10000000, 100)
    })
    
    return data


@pytest.fixture
def sample_features(sample_ohlcv_data):
    """Generate sample features for testing."""
    data = sample_ohlcv_data.copy()
    # Add some feature columns
    data["sma_10"] = data["close"].rolling(10).mean()
    data["rsi_14"] = 50 + np.random.normal(0, 10, 100)
    data["returns"] = data["close"].pct_change()
    return data.fillna(method="bfill")


@pytest.fixture
def sample_predictions():
    """Generate sample predictions for testing."""
    return np.random.normal(0, 1, 100)
