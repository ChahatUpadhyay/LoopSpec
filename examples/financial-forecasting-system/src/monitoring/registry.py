import os
import json
import pickle
from datetime import datetime
from typing import Dict, Optional, List
import logging

from ..utils.logging import get_logger
from ..utils.config import settings

logger = get_logger(__name__)


class ModelRegistry:
    """Model registry for storing and versioning trained models."""
    
    def __init__(self, registry_path: str = None):
        """
        Initialize model registry.
        
        Args:
            registry_path: Path to model registry directory
        """
        self.registry_path = registry_path or settings.model_path
        os.makedirs(self.registry_path, exist_ok=True)
        
        # Metadata file
        self.metadata_file = os.path.join(self.registry_path, "metadata.json")
        self.metadata = self._load_metadata()
        
    def _load_metadata(self) -> Dict:
        """Load metadata from file."""
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, "r") as f:
                return json.load(f)
        return {}
    
    def _save_metadata(self) -> None:
        """Save metadata to file."""
        with open(self.metadata_file, "w") as f:
            json.dump(self.metadata, f, indent=2)
    
    def save_model(
        self,
        model,
        model_name: str,
        version: str,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Save a trained model to the registry.
        
        Args:
            model: Trained model object
            model_name: Name of the model
            version: Model version
            metadata: Additional metadata
        
        Returns:
            Path to saved model
        """
        timestamp = datetime.utcnow().isoformat()
        model_id = f"{model_name}_v{version}"
        model_path = os.path.join(self.registry_path, f"{model_id}.pkl")
        
        # Save model
        with open(model_path, "wb") as f:
            pickle.dump(model, f)
        
        # Update metadata
        if model_name not in self.metadata:
            self.metadata[model_name] = {
                "versions": [],
                "latest_version": version
            }
        
        version_info = {
            "version": version,
            "path": model_path,
            "timestamp": timestamp,
            "metadata": metadata or {}
        }
        
        self.metadata[model_name]["versions"].append(version_info)
        self.metadata[model_name]["latest_version"] = version
        
        self._save_metadata()
        
        logger.info(f"Saved model {model_id} to {model_path}")
        return model_path
    
    def load_model(
        self,
        model_name: str,
        version: Optional[str] = None
    ):
        """
        Load a model from the registry.
        
        Args:
            model_name: Name of the model
            version: Model version (uses latest if None)
        
        Returns:
            Loaded model object
        """
        if model_name not in self.metadata:
            raise ValueError(f"Model {model_name} not found in registry")
        
        if version is None:
            version = self.metadata[model_name]["latest_version"]
        
        # Find version info
        version_info = None
        for v in self.metadata[model_name]["versions"]:
            if v["version"] == version:
                version_info = v
                break
        
        if version_info is None:
            raise ValueError(f"Version {version} not found for model {model_name}")
        
        # Load model
        with open(version_info["path"], "rb") as f:
            model = pickle.load(f)
        
        logger.info(f"Loaded model {model_name} v{version}")
        return model
    
    def list_versions(self, model_name: str) -> List[Dict]:
        """
        List all versions of a model.
        
        Args:
            model_name: Name of the model
        
        Returns:
            List of version information
        """
        if model_name not in self.metadata:
            return []
        
        return self.metadata[model_name]["versions"]
    
    def list_models(self) -> List[str]:
        """
        List all registered models.
        
        Returns:
            List of model names
        """
        return list(self.metadata.keys())
    
    def delete_model(
        self,
        model_name: str,
        version: Optional[str] = None
    ) -> None:
        """
        Delete a model from the registry.
        
        Args:
            model_name: Name of the model
            version: Model version (deletes all if None)
        """
        if model_name not in self.metadata:
            raise ValueError(f"Model {model_name} not found in registry")
        
        if version is None:
            # Delete all versions
            for version_info in self.metadata[model_name]["versions"]:
                if os.path.exists(version_info["path"]):
                    os.remove(version_info["path"])
            
            del self.metadata[model_name]
        else:
            # Delete specific version
            version_info = None
            for v in self.metadata[model_name]["versions"]:
                if v["version"] == version:
                    version_info = v
                    break
            
            if version_info and os.path.exists(version_info["path"]):
                os.remove(version_info["path"])
            
            # Remove from metadata
            self.metadata[model_name]["versions"] = [
                v for v in self.metadata[model_name]["versions"]
                if v["version"] != version
            ]
        
        self._save_metadata()
        logger.info(f"Deleted model {model_name} v{version if version else 'all'}")
