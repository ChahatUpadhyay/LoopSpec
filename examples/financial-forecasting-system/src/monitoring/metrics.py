import time
from prometheus_client import Counter, Histogram, Gauge, start_http_server
from typing import Optional
import logging

from ..utils.logging import get_logger
from ..utils.config import settings

logger = get_logger(__name__)


class MetricsCollector:
    """Collect and expose metrics for monitoring."""
    
    def __init__(self):
        """Initialize metrics collector."""
        # Request metrics
        self.request_count = Counter(
            "api_requests_total",
            "Total number of API requests",
            ["method", "endpoint", "status"]
        )
        
        self.request_latency = Histogram(
            "api_request_duration_seconds",
            "API request latency in seconds",
            ["method", "endpoint"]
        )
        
        # Prediction metrics
        self.prediction_count = Counter(
            "predictions_total",
            "Total number of predictions generated",
            ["model"]
        )
        
        self.prediction_latency = Histogram(
            "prediction_duration_seconds",
            "Prediction latency in seconds",
            ["model"]
        )
        
        # Error metrics
        self.error_count = Counter(
            "errors_total",
            "Total number of errors",
            ["type", "location"]
        )
        
        # System metrics
        self.active_connections = Gauge(
            "active_connections",
            "Number of active connections"
        )
        
        self.model_load_time = Histogram(
            "model_load_duration_seconds",
            "Model load time in seconds",
            ["model"]
        )
        
    def record_request(
        self,
        method: str,
        endpoint: str,
        status: str,
        duration: float
    ) -> None:
        """
        Record API request metrics.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            status: HTTP status code
            duration: Request duration in seconds
        """
        self.request_count.labels(method=method, endpoint=endpoint, status=status).inc()
        self.request_latency.labels(method=method, endpoint=endpoint).observe(duration)
    
    def record_prediction(
        self,
        model: str,
        duration: float
    ) -> None:
        """
        Record prediction metrics.
        
        Args:
            model: Model name
            duration: Prediction duration in seconds
        """
        self.prediction_count.labels(model=model).inc()
        self.prediction_latency.labels(model=model).observe(duration)
    
    def record_error(
        self,
        error_type: str,
        location: str
    ) -> None:
        """
        Record error metrics.
        
        Args:
            error_type: Type of error
            location: Location where error occurred
        """
        self.error_count.labels(type=error_type, location=location).inc()
    
    def update_connections(self, count: int) -> None:
        """
        Update active connections gauge.
        
        Args:
            count: Number of active connections
        """
        self.active_connections.set(count)
    
    def record_model_load(self, model: str, duration: float) -> None:
        """
        Record model load time.
        
        Args:
            model: Model name
            duration: Load duration in seconds
        """
        self.model_load_time.labels(model=model).observe(duration)


# Global metrics collector instance
metrics = MetricsCollector()


def track_latency(func):
    """Decorator to track function latency."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.debug(f"{func.__name__} completed in {duration:.3f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"{func.__name__} failed after {duration:.3f}s: {e}")
            metrics.record_error(type(e.__class__.__name__), func.__name__)
            raise
    return wrapper


def start_metrics_server(port: int = None):
    """
    Start Prometheus metrics server.
    
    Args:
        port: Port to run metrics server on
    """
    port = port or settings.prometheus_port
    start_http_server(port)
    logger.info(f"Prometheus metrics server started on port {port}")
