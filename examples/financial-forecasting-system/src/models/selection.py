import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
import logging

from .arima import ARIMAModel, auto_arima
from .xgboost_model import XGBoostModel
from .lstm import LSTMModel
from .transformer import TransformerModel
from ..utils.logging import get_logger

logger = get_logger(__name__)


class ModelSelector:
    """Model selection framework for comparing multiple models."""
    
    def __init__(self):
        self.models = {}
        self.results = {}
        
    def register_model(self, name: str, model: Any) -> None:
        """
        Register a model for comparison.
        
        Args:
            name: Model name
            model: Model instance
        """
        self.models[name] = model
        logger.info(f"Registered model: {name}")
    
    def evaluate_model(
        self,
        model: Any,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_test: pd.DataFrame,
        y_test: pd.Series
    ) -> Dict[str, float]:
        """
        Evaluate a model on test data.
        
        Args:
            model: Model instance
            X_train: Training features
            y_train: Training target
            X_test: Test features
            y_test: Test target
        
        Returns:
            Dictionary of evaluation metrics
        """
        # Train model
        if hasattr(model, "train"):
            model.train(X_train, y_train)
        
        # Make predictions
        predictions = model.predict(X_test)
        
        # Calculate metrics
        mse = np.mean((predictions - y_test.values) ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(predictions - y_test.values))
        
        # Directional accuracy
        direction_actual = np.sign(y_test.values[1:] - y_test.values[:-1])
        direction_pred = np.sign(predictions[1:] - predictions[:-1])
        directional_accuracy = np.mean(direction_actual == direction_pred)
        
        metrics = {
            "mse": mse,
            "rmse": rmse,
            "mae": mae,
            "directional_accuracy": directional_accuracy
        }
        
        return metrics
    
    def select_best_model(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_test: pd.DataFrame,
        y_test: pd.Series,
        metric: str = "directional_accuracy"
    ) -> Tuple[str, Any, Dict[str, float]]:
        """
        Select the best model based on evaluation metrics.
        
        Args:
            X_train: Training features
            y_train: Training target
            X_test: Test features
            y_test: Test target
            metric: Metric to use for selection
        
        Returns:
            Tuple of (best_model_name, best_model, best_metrics)
        """
        logger.info(f"Selecting best model based on {metric}")
        
        best_model_name = None
        best_model = None
        best_score = float("-inf")
        best_metrics = {}
        
        for name, model in self.models.items():
            try:
                metrics = self.evaluate_model(model, X_train, y_train, X_test, y_test)
                self.results[name] = metrics
                
                logger.info(f"{name} - {metric}: {metrics[metric]:.4f}")
                
                if metrics[metric] > best_score:
                    best_score = metrics[metric]
                    best_model_name = name
                    best_model = model
                    best_metrics = metrics
                    
            except Exception as e:
                logger.error(f"Error evaluating {name}: {e}")
                continue
        
        if best_model_name is None:
            raise ValueError("No models could be evaluated successfully")
        
        logger.info(f"Best model: {best_model_name} with {metric}: {best_score:.4f}")
        return best_model_name, best_model, best_metrics
    
    def compare_all_models(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_test: pd.DataFrame,
        y_test: pd.Series
    ) -> pd.DataFrame:
        """
        Compare all registered models.
        
        Args:
            X_train: Training features
            y_train: Training target
            X_test: Test features
            y_test: Test target
        
        Returns:
            DataFrame with comparison results
        """
        results = []
        
        for name, model in self.models.items():
            try:
                metrics = self.evaluate_model(model, X_train, y_train, X_test, y_test)
                metrics["model"] = name
                results.append(metrics)
            except Exception as e:
                logger.error(f"Error evaluating {name}: {e}")
        
        df = pd.DataFrame(results)
        df = df.set_index("model")
        
        return df


def train_and_select(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series
) -> Tuple[Any, str, Dict[str, float]]:
    """
    Train multiple models and select the best one.
    
    Args:
        X_train: Training features
        y_train: Training target
        X_test: Test features
        y_test: Test target
    
    Returns:
        Tuple of (best_model, model_name, metrics)
    """
    selector = ModelSelector()
    
    # Register models
    selector.register_model("arima", ARIMAModel())
    selector.register_model("xgboost", XGBoostModel())
    selector.register_model("lstm", LSTMModel())
    selector.register_model("transformer", TransformerModel())
    
    # Select best model
    best_name, best_model, best_metrics = selector.select_best_model(
        X_train, y_train, X_test, y_test
    )
    
    return best_model, best_name, best_metrics
