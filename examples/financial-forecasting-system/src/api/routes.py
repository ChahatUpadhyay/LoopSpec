from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime, timedelta
import logging

from .models import (
    PredictionRequest,
    PredictionResponse,
    BatchPredictionRequest,
    BatchPredictionResponse,
    ModelInfo,
    HealthResponse
)
from ..utils.logging import get_logger
from ..utils.config import settings

logger = get_logger(__name__)

router = APIRouter()


# Mock model registry (in production, this would load from database)
MODEL_REGISTRY = {
    "arima": ModelInfo(name="arima", version="1.0.0", type="statistical"),
    "xgboost": ModelInfo(name="xgboost", version="1.0.0", type="gradient_boosting"),
    "lstm": ModelInfo(name="lstm", version="1.0.0", type="neural_network"),
    "transformer": ModelInfo(name="transformer", version="1.0.0", type="transformer")
}


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        timestamp=datetime.utcnow(),
        models_loaded=list(MODEL_REGISTRY.keys())
    )


@router.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Generate prediction for a single stock.
    
    Args:
        request: Prediction request
    
    Returns:
        Prediction response
    """
    logger.info(f"Prediction request for {request.symbol} using {request.model}")
    
    # Validate model
    if request.model not in MODEL_REGISTRY:
        raise HTTPException(status_code=400, detail=f"Model {request.model} not available")
    
    # Mock prediction (in production, this would load model and generate real prediction)
    # For now, return mock data
    base_price = 100.0  # Mock base price
    predictions = [base_price + i * 0.5 for i in range(request.horizon)]
    timestamps = [datetime.utcnow() + timedelta(days=i) for i in range(request.horizon)]
    
    response = PredictionResponse(
        symbol=request.symbol,
        model=request.model,
        predictions=predictions,
        timestamps=timestamps,
        confidence=0.75,
        generated_at=datetime.utcnow()
    )
    
    logger.info(f"Generated {len(predictions)} predictions for {request.symbol}")
    return response


@router.post("/batch_predict", response_model=BatchPredictionResponse)
async def batch_predict(request: BatchPredictionRequest):
    """
    Generate predictions for multiple stocks.
    
    Args:
        request: Batch prediction request
    
    Returns:
        Batch prediction response
    """
    logger.info(f"Batch prediction request for {len(request.symbols)} stocks")
    
    # Validate model
    if request.model not in MODEL_REGISTRY:
        raise HTTPException(status_code=400, detail=f"Model {request.model} not available")
    
    # Generate predictions for each symbol
    predictions = {}
    for symbol in request.symbols:
        try:
            # Mock prediction
            base_price = 100.0 + hash(symbol) % 50  # Varying base prices
            preds = [base_price + i * 0.5 for i in range(request.horizon)]
            timestamps = [datetime.utcnow() + timedelta(days=i) for i in range(request.horizon)]
            
            predictions[symbol] = PredictionResponse(
                symbol=symbol,
                model=request.model,
                predictions=preds,
                timestamps=timestamps,
                confidence=0.75,
                generated_at=datetime.utcnow()
            )
        except Exception as e:
            logger.error(f"Error predicting {symbol}: {e}")
            continue
    
    response = BatchPredictionResponse(
        predictions=predictions,
        generated_at=datetime.utcnow()
    )
    
    logger.info(f"Generated predictions for {len(predictions)} stocks")
    return response


@router.get("/models", response_model=List[ModelInfo])
async def list_models():
    """List available models."""
    return list(MODEL_REGISTRY.values())


@router.get("/models/{model_name}", response_model=ModelInfo)
async def get_model_info(model_name: str):
    """Get information about a specific model."""
    if model_name not in MODEL_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Model {model_name} not found")
    return MODEL_REGISTRY[model_name]
