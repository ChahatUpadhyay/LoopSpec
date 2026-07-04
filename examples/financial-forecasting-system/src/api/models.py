from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class PredictionRequest(BaseModel):
    """Request model for single stock prediction."""
    
    symbol: str = Field(..., description="Stock ticker symbol")
    model: Optional[str] = Field(default="xgboost", description="Model to use for prediction")
    horizon: Optional[int] = Field(default=1, description="Prediction horizon in days")


class PredictionResponse(BaseModel):
    """Response model for prediction."""
    
    symbol: str
    model: str
    predictions: List[float]
    timestamps: List[datetime]
    confidence: Optional[float] = None
    generated_at: datetime


class BatchPredictionRequest(BaseModel):
    """Request model for batch predictions."""
    
    symbols: List[str] = Field(..., description="List of stock ticker symbols")
    model: Optional[str] = Field(default="xgboost", description="Model to use for prediction")
    horizon: Optional[int] = Field(default=1, description="Prediction horizon in days")


class BatchPredictionResponse(BaseModel):
    """Response model for batch predictions."""
    
    predictions: dict  # symbol -> PredictionResponse
    generated_at: datetime


class ModelInfo(BaseModel):
    """Model information."""
    
    name: str
    version: str
    type: str
    trained_at: Optional[datetime] = None
    performance_metrics: Optional[dict] = None


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str
    version: str
    timestamp: datetime
    models_loaded: List[str]
