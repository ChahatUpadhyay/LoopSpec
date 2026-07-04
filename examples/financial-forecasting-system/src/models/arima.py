import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from typing import Tuple, Optional, Dict
import logging
import warnings

from ..utils.logging import get_logger

logger = get_logger(__name__)
warnings.filterwarnings("ignore")


class ARIMAModel:
    """ARIMA model for time series forecasting."""
    
    def __init__(self, order: Tuple[int, int, int] = (1, 1, 1)):
        """
        Initialize ARIMA model.
        
        Args:
            order: ARIMA order (p, d, q)
        """
        self.order = order
        self.model = None
        self.fitted_model = None
        
    def train(
        self,
        data: pd.Series,
        order: Optional[Tuple[int, int, int]] = None
    ) -> ARIMA:
        """
        Train ARIMA model on time series data.
        
        Args:
            data: Time series data
            order: ARIMA order (uses default if not provided)
        
        Returns:
            Trained ARIMA model
        """
        if order is None:
            order = self.order
        
        logger.info(f"Training ARIMA model with order {order}")
        
        # Fit ARIMA model
        self.model = ARIMA(data, order=order)
        self.fitted_model = self.model.fit()
        
        logger.info(f"ARIMA model trained. AIC: {self.fitted_model.aic:.2f}")
        return self.fitted_model
    
    def predict(
        self,
        steps: int = 1,
        return_conf_int: bool = False
    ) -> np.ndarray:
        """
        Make predictions with trained model.
        
        Args:
            steps: Number of steps to forecast
            return_conf_int: Whether to return confidence intervals
        
        Returns:
            Predictions array
        """
        if self.fitted_model is None:
            raise ValueError("Model must be trained before prediction")
        
        result = self.fitted_model.forecast(steps=steps)
        
        if return_conf_int:
            forecast = self.fitted_model.get_forecast(steps=steps)
            return forecast.predicted_mean, forecast.conf_int()
        
        return result
    
    def get_summary(self) -> str:
        """Get model summary statistics."""
        if self.fitted_model is None:
            return "Model not trained"
        return str(self.fitted_model.summary())


def auto_arima(
    data: pd.Series,
    max_p: int = 3,
    max_d: int = 2,
    max_q: int = 3
) -> Tuple[ARIMAModel, Tuple[int, int, int]]:
    """
    Automatically select best ARIMA order using AIC.
    
    Args:
        data: Time series data
        max_p: Maximum AR order
        max_d: Maximum differencing order
        max_q: Maximum MA order
    
    Returns:
        Tuple of (trained model, best order)
    """
    best_aic = float("inf")
    best_order = (1, 1, 1)
    best_model = None
    
    logger.info("Running auto-ARIMA to find best order")
    
    for p in range(max_p + 1):
        for d in range(max_d + 1):
            for q in range(max_q + 1):
                try:
                    model = ARIMAModel(order=(p, d, q))
                    fitted = model.train(data)
                    
                    if fitted.aic < best_aic:
                        best_aic = fitted.aic
                        best_order = (p, d, q)
                        best_model = model
                        
                except Exception as e:
                    logger.debug(f"Failed to fit ARIMA({p},{d},{q}): {e}")
                    continue
    
    logger.info(f"Best ARIMA order: {best_order} with AIC: {best_aic:.2f}")
    return best_model, best_order
