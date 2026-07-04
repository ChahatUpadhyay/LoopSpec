import pytest
import pandas as pd
import numpy as np
from src.models.transformer import TransformerModel


class TestTransformerModel:
    """Tests for Transformer model."""
    
    def test_transformer_training(self):
        """Test Transformer model training."""
        model = TransformerModel(sequence_length=10, d_model=32)
        
        X = pd.DataFrame({
            "feature1": np.random.randn(100),
            "feature2": np.random.randn(100)
        })
        y = pd.Series(np.random.randn(100))
        
        fitted = model.train(X, y, epochs=2, verbose=0)
        
        assert fitted is not None
        assert model.model is not None
    
    def test_transformer_prediction(self):
        """Test Transformer model prediction."""
        model = TransformerModel(sequence_length=10, d_model=32)
        
        X = pd.DataFrame({
            "feature1": np.random.randn(100),
            "feature2": np.random.randn(100)
        })
        y = pd.Series(np.random.randn(100))
        
        model.train(X, y, epochs=2, verbose=0)
        predictions = model.predict(X)
        
        assert len(predictions) > 0
        assert not np.isnan(predictions).any()
