from setuptools import setup, find_packages

setup(
    name="financial-forecasting-system",
    version="0.1.0",
    description="Production-grade financial time-series forecasting system",
    author="Financial Forecasting Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "yfinance>=0.2.0",
        "scikit-learn>=1.3.0",
        "statsmodels>=0.14.0",
        "xgboost>=2.0.0",
        "tensorflow>=2.13.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.23.0",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        "prometheus-client>=0.17.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "bandit>=1.7.0",
            "mypy>=1.4.0",
        ],
    },
    python_requires=">=3.10",
)
