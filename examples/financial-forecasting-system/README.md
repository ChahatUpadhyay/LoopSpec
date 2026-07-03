# Financial Forecasting System

A production-grade financial time-series forecasting system with end-to-end pipeline from data ingestion to deployed API.

## Features

- **Data Engineering**: Ingest OHLCV data for 500+ stocks from Yahoo Finance
- **Feature Engineering**: Technical indicators, volatility features, macroeconomic joins, sentiment analysis
- **Modeling**: ARIMA, XGBoost, LSTM, and Transformer-based forecasting models
- **Model Selection**: Automated framework to select best performing model
- **Backtesting**: Realistic simulation with slippage, commissions, latency, position sizing, and stop-loss
- **Production API**: REST API for inference and batch predictions
- **Model Registry**: Versioned model storage and management
- **Monitoring**: Data drift detection, prediction drift tracking, latency and failure rate metrics
- **Deployment**: Docker and Kubernetes ready with CI/CD pipeline

## Installation

### Prerequisites

- Python 3.10+
- Docker (optional, for containerized deployment)
- Kubernetes (optional, for production deployment)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd financial-forecasting-system
```

2. Install dependencies:
```bash
pip install -e .
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Usage

### Running the Pipeline

Run the complete end-to-end pipeline:
```bash
python scripts/run_pipeline.py --test
```

### Starting the API Server

Start the FastAPI server:
```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

### API Endpoints

- `GET /api/v1/health` - Health check
- `POST /api/v1/predict` - Single stock prediction
- `POST /api/v1/batch_predict` - Batch predictions
- `GET /api/v1/models` - List available models
- `GET /api/v1/models/{model_name}` - Get model information

### Example API Request

```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "model": "xgboost",
    "horizon": 5
  }'
```

## Testing

Run the test suite:
```bash
pytest tests/ --cov=src --cov-report=html
```

Run specific test modules:
```bash
pytest tests/test_data/
pytest tests/test_models/
pytest tests/test_backtesting/
pytest tests/test_api/
pytest tests/test_monitoring/
```

## Code Quality

Run linting and type checking:
```bash
black --check src/
flake8 src/
bandit -r src/
mypy src/
```

## Deployment

### Docker

Build and run with Docker:
```bash
docker build -t financial-forecasting .
docker run -p 8000:8000 financial-forecasting
```

### Docker Compose

Run with monitoring stack:
```bash
docker-compose up
```

### Kubernetes

Deploy to Kubernetes:
```bash
kubectl apply -f deployment/kubernetes/
```

## Project Structure

```
financial-forecasting-system/
├── src/
│   ├── data/              # Data pipeline
│   ├── models/            # Model implementations
│   ├── backtesting/      # Backtesting engine
│   ├── api/               # REST API
│   ├── monitoring/        # Observability
│   └── utils/             # Utilities
├── tests/                 # Test suite
├── deployment/            # Deployment configs
├── scripts/               # Utility scripts
├── data/                  # Data storage
└── .loopspec/            # LoopSpec protocol files
```

## Model Performance Benchmarks

Target performance metrics:
- Directional accuracy: >= 58%
- Sharpe ratio: >= 1.5
- Max drawdown: <= 15%
- API p95 latency: < 150ms
- Test coverage: >= 80%

## License

See LICENSE file for details.

## Disclaimer

This system is for research and educational purposes only. It does not provide financial advice. Past performance does not guarantee future results.
