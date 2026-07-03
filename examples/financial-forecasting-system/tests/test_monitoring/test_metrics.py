import pytest
import time
from src.monitoring.metrics import MetricsCollector, track_latency


class TestMetricsCollector:
    """Tests for metrics collection module."""
    
    def test_request_recording(self):
        """Test request metric recording."""
        collector = MetricsCollector()
        
        collector.record_request(
            method="GET",
            endpoint="/health",
            status="200",
            duration=0.1
        )
        
        # Should not raise any errors
        assert True
    
    def test_prediction_recording(self):
        """Test prediction metric recording."""
        collector = MetricsCollector()
        
        collector.record_prediction(
            model="xgboost",
            duration=0.05
        )
        
        # Should not raise any errors
        assert True
    
    def test_error_recording(self):
        """Test error metric recording."""
        collector = MetricsCollector()
        
        collector.record_error(
            error_type="ValueError",
            location="model_training"
        )
        
        # Should not raise any errors
        assert True
    
    def test_latency_decorator(self):
        """Test latency tracking decorator."""
        @track_latency
        def sample_function():
            time.sleep(0.01)
            return "result"
        
        result = sample_function()
        assert result == "result"
