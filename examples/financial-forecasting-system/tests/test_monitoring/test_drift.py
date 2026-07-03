import pytest
import pandas as pd
import numpy as np
from src.monitoring.drift import DriftDetector


class TestDriftDetector:
    """Tests for drift detection module."""
    
    def test_data_drift_detection(self):
        """Test data drift detection."""
        detector = DriftDetector(threshold=0.05)
        
        reference_data = pd.DataFrame({
            "feature1": np.random.normal(0, 1, 100),
            "feature2": np.random.normal(0, 1, 100)
        })
        
        current_data = pd.DataFrame({
            "feature1": np.random.normal(0.5, 1, 100),  # Shifted distribution
            "feature2": np.random.normal(0, 1, 100)
        })
        
        drift_scores = detector.detect_data_drift(reference_data, current_data)
        
        assert "feature1" in drift_scores
        assert "feature2" in drift_scores
        assert "p_value" in drift_scores["feature1"]
        assert "drift_detected" in drift_scores["feature1"]
    
    def test_prediction_drift_detection(self):
        """Test prediction drift detection."""
        detector = DriftDetector(threshold=0.05)
        
        reference_predictions = np.random.normal(0, 1, 100)
        current_predictions = np.random.normal(0.5, 1, 100)  # Shifted
        
        drift_metrics = detector.detect_prediction_drift(
            reference_predictions,
            current_predictions
        )
        
        assert "p_value" in drift_metrics
        assert "mean_shift" in drift_metrics
        assert "drift_detected" in drift_metrics
    
    def test_drift_score_calculation(self):
        """Test overall drift score calculation."""
        detector = DriftDetector()
        
        reference_data = pd.DataFrame({
            "feature1": np.random.normal(0, 1, 100),
            "feature2": np.random.normal(0, 1, 100)
        })
        
        current_data = pd.DataFrame({
            "feature1": np.random.normal(0, 1, 100),
            "feature2": np.random.normal(0, 1, 100)
        })
        
        drift_score = detector.calculate_drift_score(reference_data, current_data)
        
        assert 0 <= drift_score <= 1
