import pytest
import pandas as pd
import numpy as np
from src.models.lstm import LSTMModel


class TestLSTMModel:
    """Tests for LSTM model."""
    
    def test_lstm_training(self):
        """Test LSTM model training."""
        model = LSTMModel(sequence_length=10, lstm_units=10)
        
        X = pd.DataFrame({
            "feature1": np.random.randn(100),
            "feature2": np.random.randn(100)
        })
        y = pd.Series(np.random.randn(100))
        
        fitted = model.train(X, y, epochs=2, verbose=0)
        
        assert fitted is not None
        assert model.model is not None
    
    def test_lstm_prediction(self):
        """Test LSTM model prediction."""
        model = LSTMModel(sequence_length=10, lstm_units=10)
        
        X = pd.DataFrame({
            "feature1": np.random.randn(100),
            "feature2": np.random.randn(100)
        })
        y = pd.Series(np.random.randn(100))
        
        model.train(X, y, epochs=2, verbose=0)
        predictions = model.predict(X)
        
        assert len(predictions) > 0
        assert not np.isnan(predictions).any()
