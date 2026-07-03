import pytest
import pandas as pd
import numpy as np
from src.models.arima import ARIMAModel, auto_arima


class TestARIMAModel:
    """Tests for ARIMA model."""
    
    def test_arima_training(self):
        """Test ARIMA model training."""
        model = ARIMAModel(order=(1, 1, 1))
        
        data = pd.Series([100 + i + np.random.normal(0, 1) for i in range(100)])
        fitted = model.train(data)
        
        assert fitted is not None
        assert model.fitted_model is not None
    
    def test_arima_prediction(self):
        """Test ARIMA model prediction."""
        model = ARIMAModel(order=(1, 1, 1))
        
        data = pd.Series([100 + i + np.random.normal(0, 1) for i in range(100)])
        model.train(data)
        
        predictions = model.predict(steps=5)
        
        assert len(predictions) == 5
        assert not np.isnan(predictions).any()
    
    def test_auto_arima(self):
        """Test automatic ARIMA order selection."""
        data = pd.Series([100 + i + np.random.normal(0, 1) for i in range(100)])
        
        model, order = auto_arima(data, max_p=2, max_d=1, max_q=2)
        
        assert model is not None
        assert len(order) == 3
