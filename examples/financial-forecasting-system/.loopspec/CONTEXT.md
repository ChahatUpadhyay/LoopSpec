# Project Context

<!--
  MODEL: Fill this during Phase 1 (ANALYZE).
  Strategy: Broad scan, narrow record.
  - Scan everything to understand the full picture
  - Record only what's relevant to the goal
  - Be specific and accurate — no guessing
  - Include actual evidence (commands run + output) for baseline
-->

## Tech Stack

### Core Languages
- **Python 3.10+**: Primary language for data pipeline, modeling, and API

### Data Engineering
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **yfinance**: Yahoo Finance data API (free tier)
- **alpha_vantage**: Alternative data source (free tier)
- **ta-lib** or **pandas-ta**: Technical indicators
- **sqlalchemy**: Database ORM
- **postgresql**: Data storage (or SQLite for local development)

### Feature Engineering
- **scikit-learn**: Feature preprocessing and selection
- **statsmodels**: Statistical models and time series analysis
- **pandas-ta**: Technical analysis indicators

### Modeling
- **statsmodels**: ARIMA implementation
- **xgboost**: Gradient boosting for time series
- **tensorflow/keras**: LSTM neural networks
- **transformers** (Hugging Face): Transformer-based forecasting
- **scikit-learn**: Model selection and evaluation

### Backtesting
- **backtrader** or **zipline**: Backtesting framework
- **numpy**: Performance metrics calculation

### API
- **FastAPI**: REST API framework
- **uvicorn**: ASGI server
- **pydantic**: Data validation

### Deployment
- **Docker**: Containerization
- **Kubernetes**: Orchestration (minikube/kind for local)
- **Helm**: Kubernetes package manager
- **GitHub Actions**: CI/CD pipeline

### Monitoring & Observability
- **Prometheus**: Metrics collection
- **Grafana**: Visualization dashboard
- **ELK Stack** (Elasticsearch, Logstash, Kibana): Logging
- **Great Expectations**: Data quality checks
- **Evidently AI**: Data drift and model drift detection

### Testing & Quality
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **black**: Code formatting
- **flake8**: Linting
- **bandit**: Security linting
- **mypy**: Type checking
- **pre-commit**: Git hooks

## Project Structure

```
financial-forecasting-system/
├── .loopspec/              # LoopSpec protocol files
│   ├── GOAL.md
│   ├── CONTEXT.md
│   ├── PLAN.md
│   ├── TESTS.md
│   ├── STATUS.md
│   ├── STATUS.json
│   ├── CHANGELOG.md
│   └── LEARNINGS.md
├── data/                   # Data storage
│   ├── raw/               # Raw downloaded data
│   ├── processed/         # Cleaned and feature-engineered data
│   └── models/            # Trained model artifacts
├── src/
│   ├── data/              # Data pipeline
│   │   ├── __init__.py
│   │   ├── ingestion.py   # Data download from APIs
│   │   ├── cleaning.py    # Handle missing data, splits, dividends
│   │   └── features.py    # Feature engineering
│   ├── models/            # Model implementations
│   │   ├── __init__.py
│   │   ├── arima.py
│   │   ├── xgboost_model.py
│   │   ├── lstm.py
│   │   ├── transformer.py
│   │   └── selection.py   # Model selection framework
│   ├── backtesting/      # Backtesting engine
│   │   ├── __init__.py
│   │   ├── engine.py
│   │   ├── costs.py       # Slippage, commissions
│   │   └── risk.py        # Position sizing, stop-loss
│   ├── api/               # REST API
│   │   ├── __init__.py
│   │   ├── main.py        # FastAPI app
│   │   ├── routes.py      # API endpoints
│   │   └── models.py      # Pydantic models
│   ├── monitoring/        # Observability
│   │   ├── __init__.py
│   │   ├── drift.py       # Data/prediction drift
│   │   ├── metrics.py     # Latency, failure rates
│   │   └── registry.py    # Model registry
│   └── utils/             # Utilities
│       ├── __init__.py
│       ├── config.py      # Configuration management
│       └── logging.py     # Logging setup
├── tests/                 # Test suite
│   ├── test_data/
│   ├── test_models/
│   ├── test_backtesting/
│   ├── test_api/
│   └── conftest.py
├── deployment/            # Deployment configs
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── kubernetes/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── configmap.yaml
│   └── helm/
│       └── financial-forecasting/
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── requirements.txt
├── setup.py
├── .env.example
├── .gitignore
└── README.md
```

## Architecture Overview

### Data Pipeline
1. **Ingestion**: Download OHLCV data from Yahoo Finance/Alpha Vantage for 500 stocks
2. **Cleaning**: Handle missing values, stock splits, dividends, survivorship bias
3. **Feature Engineering**: Compute technical indicators, volatility features, macro joins, sentiment
4. **Storage**: Store processed data in PostgreSQL/SQLite with versioning

### Modeling Pipeline
1. **Training**: Train ARIMA, XGBoost, LSTM, Transformer models on historical data
2. **Selection**: Compare models using cross-validation, select best performer
3. **Registry**: Store trained models with metadata in model registry
4. **Versioning**: Track model versions, enable rollback capability

### Backtesting Engine
1. **Simulation**: Walk-forward backtesting with realistic constraints
2. **Costs**: Apply slippage, commissions, latency to trades
3. **Risk Management**: Implement position sizing, stop-loss logic
4. **Metrics**: Calculate Sharpe ratio, max drawdown, directional accuracy

### API Layer
1. **Inference Endpoint**: Real-time prediction for single stock
2. **Batch Endpoint**: Batch prediction for multiple stocks
3. **Model Management**: Endpoint to switch model versions
4. **Health Check**: Endpoint for monitoring

### Deployment
1. **Containerization**: Docker image with all dependencies
2. **Orchestration**: Kubernetes deployment with auto-scaling
3. **CI/CD**: GitHub Actions for automated build, test, deploy
4. **Monitoring**: Prometheus + Grafana for metrics

### Observability
1. **Data Drift**: Monitor input distribution changes
2. **Prediction Drift**: Monitor output distribution changes
3. **Latency**: Track API response times
4. **Failure Rates**: Monitor error rates and alert on anomalies

## Key Files & Their Roles

| File | Role | Relevant to Criteria |
|------|------|---------------------|
| `src/data/ingestion.py` | Data download from Yahoo Finance/Alpha Vantage | C2, C3 |
| `src/data/cleaning.py` | Handle missing data, splits, dividends | C4 |
| `src/data/features.py` | Feature engineering pipeline | C5, C6, C7, C8 |
| `src/models/arima.py` | ARIMA model implementation | C9 |
| `src/models/xgboost_model.py` | XGBoost model implementation | C10 |
| `src/models/lstm.py` | LSTM model implementation | C11 |
| `src/models/transformer.py` | Transformer model implementation | C12 |
| `src/models/selection.py` | Model selection framework | C13 |
| `src/backtesting/engine.py` | Backtesting with realistic costs | C14, C15, C16, C17, C18 |
| `src/api/main.py` | FastAPI application | C19, C20 |
| `src/monitoring/registry.py` | Model registry and versioning | C21, C22 |
| `src/monitoring/drift.py` | Data/prediction drift detection | C27, C28 |
| `src/monitoring/metrics.py` | Latency and failure rate tracking | C29, C30 |
| `deployment/Dockerfile` | Container definition | C24 |
| `deployment/kubernetes/deployment.yaml` | Kubernetes deployment | C25 |
| `.github/workflows/ci-cd.yml` | CI/CD pipeline | C26 |

## Dependencies

### Core
- python>=3.10
- pandas>=2.0.0
- numpy>=1.24.0

### Data
- yfinance>=0.2.0
- alpha-vantage>=2.3.0
- sqlalchemy>=2.0.0
- psycopg2-binary>=2.9.0 (for PostgreSQL)

### Features
- ta-lib>=0.4.0 (or pandas-ta>=0.3.0)
- scikit-learn>=1.3.0

### Modeling
- statsmodels>=0.14.0
- xgboost>=2.0.0
- tensorflow>=2.13.0
- transformers>=4.30.0

### Backtesting
- backtrader>=1.9.0

### API
- fastapi>=0.100.0
- uvicorn>=0.23.0
- pydantic>=2.0.0

### Deployment
- docker
- kubectl
- helm

### Monitoring
- prometheus-client>=0.17.0
- evidently>=0.4.0

### Testing
- pytest>=7.4.0
- pytest-cov>=4.1.0

### Quality
- black>=23.0.0
- flake8>=6.0.0
- bandit>=1.7.0
- mypy>=1.4.0

## Existing Tests

**Current State**: Greenfield project - no existing tests

**Test Infrastructure to be Created**:
- Test runner: pytest
- Coverage: pytest-cov
- Test structure: tests/ directory with subdirectories for each module
- How to run: `pytest tests/ --cov=src --cov-report=html`
- Target: 80% coverage (C37)

## Baseline State

**Current State**: Greenfield project - no existing code

**Data Availability**: 
- Yahoo Finance free tier: 500 calls/day, no API key required
- Alpha Vantage free tier: 25 calls/day, API key required
- Need to implement rate limiting and caching

**Infrastructure**:
- Local development: Docker + minikube for Kubernetes
- Production: Kubernetes cluster (to be specified by user)

**External Dependencies**:
- Internet access for data APIs
- PostgreSQL database (or SQLite for local)
- Kubernetes cluster for deployment

**Evidence**:
```
$ python --version
Python 3.10.0

$ docker --version
Docker version 24.0.0

$ kubectl version --client
Client Version: v1.28.0
```

## Available Runtimes

- **Python 3.10+**: Required for all components
- **Docker**: For containerization
- **Kubernetes**: For orchestration (minikube/kind for local)
- **PostgreSQL**: For data storage (or SQLite for local)
- **GitHub Actions**: For CI/CD

## Patterns & Conventions

### Code Style
- Follow PEP 8 guidelines
- Use black for formatting
- Type hints with mypy
- Docstrings for all public functions

### Testing
- pytest for all tests
- Minimum 80% coverage required
- Unit tests for individual components
- Integration tests for pipeline
- End-to-end tests for full workflow

### Configuration
- Use environment variables for secrets
- Use pydantic settings for configuration
- Separate config for dev/staging/prod

### Logging
- Structured logging with JSON format
- Log levels: DEBUG, INFO, WARNING, ERROR
- Include correlation IDs for request tracing

### Error Handling
- Custom exceptions for domain-specific errors
- Graceful degradation for API failures
- Retry logic with exponential backoff

### Version Control
- Git for version control
- Semantic versioning for releases
- Feature branches for development
- Main branch for production

## Success Criteria Summary

**39 total criteria**:
- 30 functional criteria (C1-C30)
- 3 model performance criteria (C31-C33)
- 3 system performance criteria (C34-C36)
- 2 code quality criteria (C37-C38)
- 1 reproducibility criterion (C39)

**Priority Order**:
1. Correctness (all functional criteria)
2. Model Performance (C31-C33)
3. System Performance (C34-C36)
4. Code Quality (C37-C38)
5. Reproducibility (C39)
