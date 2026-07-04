import pytest
import pandas as pd
import numpy as np
from src.models.selection import ModelSelector


class TestModelSelection:
    """Tests for model selection framework."""
    
    def test_model_selection(self):
        """Test model selection framework."""
        selector = ModelSelector()
        
        X_train = pd.DataFrame({
            "feature1": np.random.randn(80),
            "feature2": np.random.randn(80)
        })
        y_train = pd.Series(np.random.randn(80))
        
        X_test = pd.DataFrame({
            "feature1": np.random.randn(20),
            "feature2": np.random.randn(20)
        })
        y_test = pd.Series(np.random.randn(20))
        
        # Register a simple mock model
        class MockModel:
            def train(self, X, y):
                return self
            def predict(self, X):
                return np.random.randn(len(X))
        
        selector.register_model("mock", MockModel())
        
        best_name, best_model, best_metrics = selector.select_best_model(
            X_train, y_train, X_test, y_test
        )
        
        assert best_name == "mock"
        assert best_model is not None
        assert "directional_accuracy" in best_metrics
