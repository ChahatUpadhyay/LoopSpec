import pytest
import tempfile
import os
import shutil
from src.monitoring.registry import ModelRegistry


class TestModelRegistry:
    """Tests for model registry module."""
    
    @pytest.fixture
    def temp_registry(self):
        """Create temporary registry for testing."""
        temp_dir = tempfile.mkdtemp()
        registry = ModelRegistry(registry_path=temp_dir)
        yield registry
        shutil.rmtree(temp_dir)
    
    def test_save_model(self, temp_registry):
        """Test saving a model to registry."""
        mock_model = {"weights": [1, 2, 3]}
        
        path = temp_registry.save_model(
            model=mock_model,
            model_name="test_model",
            version="1.0.0"
        )
        
        assert os.path.exists(path)
        assert "test_model" in temp_registry.metadata
    
    def test_load_model(self, temp_registry):
        """Test loading a model from registry."""
        mock_model = {"weights": [1, 2, 3]}
        
        temp_registry.save_model(
            model=mock_model,
            model_name="test_model",
            version="1.0.0"
        )
        
        loaded_model = temp_registry.load_model("test_model", "1.0.0")
        
        assert loaded_model == mock_model
    
    def test_list_versions(self, temp_registry):
        """Test listing model versions."""
        mock_model = {"weights": [1, 2, 3]}
        
        temp_registry.save_model(mock_model, "test_model", "1.0.0")
        temp_registry.save_model(mock_model, "test_model", "2.0.0")
        
        versions = temp_registry.list_versions("test_model")
        
        assert len(versions) == 2
    
    def test_list_models(self, temp_registry):
        """Test listing all models."""
        mock_model = {"weights": [1, 2, 3]}
        
        temp_registry.save_model(mock_model, "model1", "1.0.0")
        temp_registry.save_model(mock_model, "model2", "1.0.0")
        
        models = temp_registry.list_models()
        
        assert len(models) == 2
        assert "model1" in models
        assert "model2" in models
