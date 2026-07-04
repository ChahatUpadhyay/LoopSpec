import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple
from scipy import stats
import logging

from ..utils.logging import get_logger

logger = get_logger(__name__)


class DriftDetector:
    """Detect data drift and prediction drift."""
    
    def __init__(self, threshold: float = 0.05):
        """
        Initialize drift detector.
        
        Args:
            threshold: Statistical significance threshold for drift detection
        """
        self.threshold = threshold
        
    def detect_data_drift(
        self,
        reference_data: pd.DataFrame,
        current_data: pd.DataFrame,
        columns: Optional[list] = None
    ) -> Dict[str, float]:
        """
        Detect data drift between reference and current datasets.
        
        Args:
            reference_data: Reference dataset (training data)
            current_data: Current dataset (new data)
            columns: Columns to check (uses all if None)
        
        Returns:
            Dictionary with drift scores for each column
        """
        if columns is None:
            columns = reference_data.columns.tolist()
        
        drift_scores = {}
        
        for col in columns:
            if col not in current_data.columns:
                continue
            
            ref_values = reference_data[col].dropna()
            curr_values = current_data[col].dropna()
            
            if len(ref_values) == 0 or len(curr_values) == 0:
                continue
            
            # Kolmogorov-Smirnov test for distribution difference
            ks_statistic, p_value = stats.ks_2samp(ref_values, curr_values)
            
            drift_scores[col] = {
                "ks_statistic": ks_statistic,
                "p_value": p_value,
                "drift_detected": p_value < self.threshold
            }
            
            if drift_scores[col]["drift_detected"]:
                logger.warning(f"Data drift detected in {col}: p-value={p_value:.4f}")
        
        return drift_scores
    
    def detect_prediction_drift(
        self,
        reference_predictions: np.ndarray,
        current_predictions: np.ndarray
    ) -> Dict[str, float]:
        """
        Detect prediction drift between reference and current predictions.
        
        Args:
            reference_predictions: Reference predictions
            current_predictions: Current predictions
        
        Returns:
            Dictionary with drift metrics
        """
        # Calculate statistical tests
        ks_statistic, p_value = stats.ks_2samp(reference_predictions, current_predictions)
        
        # Calculate mean shift
        mean_shift = np.mean(current_predictions) - np.mean(reference_predictions)
        
        # Calculate variance shift
        var_shift = np.var(current_predictions) - np.var(reference_predictions)
        
        drift_metrics = {
            "ks_statistic": ks_statistic,
            "p_value": p_value,
            "mean_shift": mean_shift,
            "variance_shift": var_shift,
            "drift_detected": p_value < self.threshold
        }
        
        if drift_metrics["drift_detected"]:
            logger.warning(f"Prediction drift detected: p-value={p_value:.4f}")
        
        return drift_metrics
    
    def calculate_drift_score(
        self,
        reference_data: pd.DataFrame,
        current_data: pd.DataFrame
    ) -> float:
        """
        Calculate overall drift score.
        
        Args:
            reference_data: Reference dataset
            current_data: Current dataset
        
        Returns:
            Overall drift score (0-1)
        """
        drift_scores = self.detect_data_drift(reference_data, current_data)
        
        if not drift_scores:
            return 0.0
        
        # Average drift score across all columns
        total_drift = sum(
            1 for score in drift_scores.values()
            if score["drift_detected"]
        )
        
        return total_drift / len(drift_scores)
