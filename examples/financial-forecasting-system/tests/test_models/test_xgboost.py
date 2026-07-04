import pytest
import pandas as pd
import numpy as np
from src.models.xgboost_model import XGBoostModel


class TestXGBoostModel:
    """Tests for XGBoost model."""
    
    def test_xgboost_training(self):
        """Test XGBoost model training."""
        model = XGBoostModel(n_estimators=10, max_depth=3)
        
        X = pd.DataFrame({
            "feature1": np.random.randn(100),
            "feature2": np.random.randn(100),
            "feature3": np.random.randn(100)
        })
        y = pd.Series(np.random.randn(100))
        
        fitted = model.train(X, y)
        
        assert fitted is not None
        assert model.model is not None
    
    def test_xgboost_prediction(self):
        """Test XGBoost model prediction."""
        model = XGBoostModel(n_estimators=10, max_depth=3)
        
        X = pd.DataFrame({
            "feature1": np.random.randn(100),
            "feature2": np.random.randn(100),
            "feature3": np.random.randn(100)
        })
        y = pd.Series(np.random.randn(100))
        
        model.train(X, y)
        predictions = model.predict(X)
        
        assert len(predictions) == 100
        assert not np.isnan(predictions).any()
    
    def test_xgboost_feature_importance(self):
        """Test XGBoost feature importance."""
        model = XGBoostModel(n_estimators=10, max_depth=3)
        
        X = pd.DataFrame({
            "feature1": np.random.randn(100),
            "feature2": np.random.randn(100),
            "feature3": np.random.randn(100)
        })
        y = pd.Series(np.random.randn(100))
        
        model.train(X, y)
        importance = model.get_feature_importance()
        
        assert len(importance) == 3
        assert "feature" in importance.columns
        assert "importance" in importance.columns
