# Goal

## Objective

Build and deploy a production-grade financial time-series forecasting system that ingests real market data from Yahoo Finance or Alpha Vantage, implements multiple forecasting models (ARIMA, XGBoost, LSTM, Transformer), includes a realistic backtesting engine, provides a production REST API, deploys via Docker and Kubernetes with CI/CD, and includes comprehensive observability for data drift, prediction drift, latency, and failure rates.

## Success Criteria

### Functional Benchmarks

| ID | Criterion | Verifier | Threshold | Required |
|----|-----------|----------|-----------|----------|
| C1 | Full pipeline runs from raw data → prediction → deployed API | automated | End-to-end pipeline executes without errors | yes |
| C2 | Data ingestion from Yahoo Finance or Alpha Vantage for 500 stocks | automated | Successfully retrieves OHLCV data for 500 stocks | yes |
| C3 | 10+ years of historical OHLCV data stored | automated | Data spans 10+ years with daily frequency | yes |
| C4 | Handle missing data, stock splits, dividends | automated | Data pipeline handles all edge cases without errors | yes |
| C5 | Technical indicators feature pipeline | automated | At least 10 technical indicators computed (SMA, EMA, RSI, MACD, Bollinger, etc.) | yes |
| C6 | Volatility clustering features | automated | GARCH or similar volatility features computed | yes |
| C7 | Macroeconomic data joins | automated | At least 3 macroeconomic indicators joined (interest rates, inflation, GDP) | yes |
| C8 | News sentiment features | automated | Sentiment scores integrated into feature set | yes |
| C9 | ARIMA model implementation | automated | ARIMA model trains and produces predictions | yes |
| C10 | XGBoost model implementation | automated | XGBoost model trains and produces predictions | yes |
| C11 | LSTM model implementation | automated | LSTM model trains and produces predictions | yes |
| C12 | Transformer-based forecasting model | automated | Transformer model trains and produces predictions | yes |
| C13 | Model selection framework | automated | Framework compares models and selects best performer | yes |
| C14 | Backtesting engine with slippage simulation | automated | Slippage is applied to trades in backtest | yes |
| C15 | Backtesting engine with commission simulation | automated | Commissions are deducted from trade P&L | yes |
| C16 | Backtesting engine with latency simulation | automated | Order execution delay is simulated | yes |
| C17 | Backtesting engine with position sizing | automated | Position sizing logic implemented (fixed fractional, Kelly, etc.) | yes |
| C18 | Backtesting engine with stop-loss logic | automated | Stop-loss orders trigger at specified thresholds | yes |
| C19 | REST API for inference | automated | API endpoints accept requests and return predictions | yes |
| C20 | Batch prediction pipeline | automated | Batch processing runs for multiple stocks/timeframes | yes |
| C21 | Model registry | automated | Trained models are stored with versioning | yes |
| C22 | Model versioning | automated | Multiple model versions can be deployed and rolled back | yes |
| C23 | Monitoring dashboard | automated | Real-time metrics displayed (latency, throughput, errors) | yes |
| C24 | Docker deployment | automated | Application runs in Docker container | yes |
| C25 | Kubernetes deployment | automated | Application deployed to Kubernetes cluster | yes |
| C26 | CI/CD pipeline | automated | Automated build, test, deploy pipeline configured | yes |
| C27 | Data drift detection | automated | Data drift alerts triggered when distribution changes | yes |
| C28 | Prediction drift detection | automated | Prediction drift alerts triggered when outputs shift | yes |
| C29 | Latency tracking | automated | API latency metrics collected and displayed | yes |
| C30 | Failure rate tracking | automated | Error rates monitored and alerted | yes |

### Model Benchmarks

| ID | Criterion | Verifier | Threshold | Required |
|----|-----------|----------|-----------|----------|
| C31 | Directional accuracy > 58% on unseen 1-year test data | metric | Directional accuracy >= 58% | yes |
| C32 | Sharpe ratio > 1.5 on backtest | metric | Sharpe ratio >= 1.5 | yes |
| C33 | Max drawdown < 15% on backtest | metric | Max drawdown <= 15% | yes |

### System Benchmarks

| ID | Criterion | Verifier | Threshold | Required |
|----|-----------|----------|-----------|----------|
| C34 | API p95 latency < 150ms | metric | p95 latency <= 150ms | yes |
| C35 | 99.5% uptime over 7 days | metric | Uptime >= 99.5% over 7-day period | yes |
| C36 | Retraining pipeline completes < 30 min | metric | Retraining time <= 30 minutes | yes |

### Code Quality Benchmarks

| ID | Criterion | Verifier | Threshold | Required |
|----|-----------|----------|-----------|----------|
| C37 | 80% unit test coverage | metric | Test coverage >= 80% | yes |
| C38 | Zero critical lint/security issues | automated | No critical lint or security issues reported | yes |

### Reproducibility Benchmarks

| ID | Criterion | Verifier | Threshold | Required |
|----|-----------|----------|-----------|----------|
| C39 | Fresh clone + one command reproduces everything | manual | Single command setup and execution works | yes |

## Permissions

### Standard Permissions
- [x] Read all project files
- [x] Create new files
- [x] Modify existing files
- [x] Delete files
- [x] Execute shell commands
- [x] Run tests
- [x] Git operations (commit, branch, push)
- [x] Install dependencies (npm, pip, cargo, etc.)
- [x] Modify configuration files

### Safety-Gated Permissions (require explicit approval per action)
- [x] Access network / external APIs (Yahoo Finance, Alpha Vantage)
- [ ] Modify database schemas
- [x] Deploy to production/staging (local Docker/Kubernetes only)
- [ ] Actions involving secrets/credentials (use environment variables)
- [ ] Paid API calls or cloud resource creation
- [ ] Irreversible operations (publish, send, delete remote)

## Constraints

- Must use Python for data pipeline and modeling
- Must use Yahoo Finance or Alpha Vantage for data (free tier)
- Must use Docker for containerization
- Must use Kubernetes for orchestration (local minikube/kind acceptable)
- Must use FastAPI or Flask for REST API
- Must use scikit-learn, statsmodels, XGBoost, TensorFlow/PyTorch for modeling
- Must use pytest for testing
- Must use GitHub Actions or similar for CI/CD
- Must not use paid cloud services without explicit approval
- Must handle API rate limits gracefully
- Must implement proper error handling and logging
- Must follow PEP 8 style guidelines
- Must use environment variables for configuration

## Priority

1. Correctness > Speed
2. Model Performance > Feature Completeness
3. Code Quality > Rapid Development
4. Reproducibility > Optimization
5. Test Coverage > Documentation

## Quality Threshold

- All automated tests must pass on first run
- >= 80% test coverage on new code
- Zero critical security vulnerabilities
- API response time < 150ms (p95)
- Model directional accuracy >= 58%
- Backtest Sharpe ratio >= 1.5
- Max drawdown <= 15%

## Max Iterations

max_iterations: 20

## Additional Context

This is a production-grade financial forecasting system. Key considerations:

- Data Quality: Financial data has missing values, survivorship bias, and structural breaks
- Model Selection: Different models work better in different market regimes
- Backtesting Realism: Must account for transaction costs, slippage, and market impact
- Production Readiness: API must be reliable, monitored, and scalable
- Reproducibility: All experiments must be reproducible with proper versioning
- Regulatory: Must not provide financial advice, this is for research/educational purposes

Tech Stack Recommendations:
- Data: pandas, numpy, yfinance, alpha_vantage
- Features: ta-lib, pandas-ta
- Modeling: statsmodels (ARIMA), xgboost, tensorflow/keras (LSTM), transformers
- Backtesting: backtrader or zipline
- API: FastAPI
- Deployment: Docker, Kubernetes (Helm charts)
- CI/CD: GitHub Actions
- Monitoring: Prometheus, Grafana
- Testing: pytest, pytest-cov
- Quality: black, flake8, bandit, mypy
