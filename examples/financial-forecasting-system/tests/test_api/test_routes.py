import pytest
from fastapi.testclient import TestClient
from src.api.main import app


class TestAPIRoutes:
    """Tests for API routes."""
    
    def test_health_check(self):
        """Test health check endpoint."""
        client = TestClient(app)
        response = client.get("/api/v1/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "models_loaded" in data
    
    def test_inference_endpoint(self):
        """Test single stock prediction endpoint."""
        client = TestClient(app)
        
        response = client.post(
            "/api/v1/predict",
            json={
                "symbol": "AAPL",
                "model": "xgboost",
                "horizon": 5
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "AAPL"
        assert data["model"] == "xgboost"
        assert len(data["predictions"]) == 5
    
    def test_batch_prediction(self):
        """Test batch prediction endpoint."""
        client = TestClient(app)
        
        response = client.post(
            "/api/v1/batch_predict",
            json={
                "symbols": ["AAPL", "MSFT", "GOOGL"],
                "model": "xgboost",
                "horizon": 3
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "predictions" in data
        assert len(data["predictions"]) == 3
    
    def test_list_models(self):
        """Test list models endpoint."""
        client = TestClient(app)
        
        response = client.get("/api/v1/models")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
