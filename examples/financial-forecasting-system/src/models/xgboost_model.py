import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error, mean_absolute_error
from typing import Tuple, Optional, Dict
import logging

from ..utils.logging import get_logger

logger = get_logger(__name__)


class XGBoostModel:
    """XGBoost model for time series forecasting."""
    
    def __init__(
        self,
        n_estimators: int = 100,
        max_depth: int = 6,
        learning_rate: float = 0.1,
        random_state: int = 42
    ):
        """
        Initialize XGBoost model.
        
        Args:
            n_estimators: Number of trees
            max_depth: Maximum tree depth
            learning_rate: Learning rate
            random_state: Random seed
        """
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.learning_rate = learning_rate
        self.random_state = random_state
        self.model = None
        self.feature_names = None
        
    def train(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        params: Optional[Dict] = None
    ) -> xgb.XGBRegressor:
        """
        Train XGBoost model.
        
        Args:
            X: Feature DataFrame
            y: Target series
            params: Additional XGBoost parameters
        
        Returns:
            Trained XGBoost model
        """
        self.feature_names = X.columns.tolist()
        
        # Default parameters
        model_params = {
            "n_estimators": self.n_estimators,
            "max_depth": self.max_depth,
            "learning_rate": self.learning_rate,
            "random_state": self.random_state,
            "objective": "reg:squarederror",
        }
        
        if params:
            model_params.update(params)
        
        logger.info(f"Training XGBoost with params: {model_params}")
        
        self.model = xgb.XGBRegressor(**model_params)
        self.model.fit(X, y)
        
        logger.info("XGBoost model trained successfully")
        return self.model
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make predictions with trained model.
        
        Args:
            X: Feature DataFrame
        
        Returns:
            Predictions array
        """
        if self.model is None:
            raise ValueError("Model must be trained before prediction")
        
        return self.model.predict(X)
    
    def get_feature_importance(self) -> pd.DataFrame:
        """
        Get feature importance scores.
        
        Returns:
            DataFrame with feature importance
        """
        if self.model is None:
            raise ValueError("Model must be trained before getting feature importance")
        
        importance = self.model.feature_importances_
        df = pd.DataFrame({
            "feature": self.feature_names,
            "importance": importance
        }).sort_values("importance", ascending=False)
        
        return df
    
    def cross_validate(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        n_splits: int = 5
    ) -> Dict[str, float]:
        """
        Perform time series cross-validation.
        
        Args:
            X: Feature DataFrame
            y: Target series
            n_splits: Number of CV splits
        
        Returns:
            Dictionary of CV metrics
        """
        tscv = TimeSeriesSplit(n_splits=n_splits)
        scores = []
        
        for train_idx, val_idx in tscv.split(X):
            X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
            y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
            
            model = xgb.XGBRegressor(
                n_estimators=self.n_estimators,
                max_depth=self.max_depth,
                learning_rate=self.learning_rate,
                random_state=self.random_state,
                objective="reg:squarederror"
            )
            
            model.fit(X_train, y_train)
            predictions = model.predict(X_val)
            
            mse = mean_squared_error(y_val, predictions)
            scores.append(mse)
        
        cv_results = {
            "mean_mse": np.mean(scores),
            "std_mse": np.std(scores),
            "mean_rmse": np.sqrt(np.mean(scores)),
        }
        
        logger.info(f"CV Results: {cv_results}")
        return cv_results
