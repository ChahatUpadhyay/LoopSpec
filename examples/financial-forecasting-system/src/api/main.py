from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
import logging

from .routes import router
from ..utils.logging import setup_logging, get_logger
from ..utils.config import settings

# Setup logging
setup_logging(settings.log_level, settings.log_format)
logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Financial Forecasting API",
    description="Production-grade financial time-series forecasting API",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api/v1")

# Add Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("Starting Financial Forecasting API")
    logger.info(f"API running on {settings.api_host}:{settings.api_port}")
    logger.info(f"Default model: {settings.default_model}")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("Shutting down Financial Forecasting API")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Financial Forecasting API",
        "version": "0.1.0",
        "status": "running"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        workers=settings.api_workers,
        log_level=settings.log_level.lower()
    )
