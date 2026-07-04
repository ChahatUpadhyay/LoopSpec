from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """Application configuration using environment variables."""
    
    # Database
    database_url: str = Field(default="sqlite:///./data/financial_forecasting.db", alias="DATABASE_URL")
    
    # API Keys
    alpha_vantage_api_key: Optional[str] = Field(default=None, alias="ALPHA_VANTAGE_API_KEY")
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")
    api_workers: int = Field(default=4, alias="API_WORKERS")
    
    # Model Configuration
    model_path: str = Field(default="data/models", alias="MODEL_PATH")
    default_model: str = Field(default="xgboost", alias="DEFAULT_MODEL")
    
    # Data Configuration
    data_path: str = Field(default="data/raw", alias="DATA_PATH")
    processed_data_path: str = Field(default="data/processed", alias="PROCESSED_DATA_PATH")
    num_stocks: int = Field(default=500, alias="NUM_STOCKS")
    years_of_data: int = Field(default=10, alias="YEARS_OF_DATA")
    
    # Backtesting Configuration
    initial_capital: float = Field(default=100000.0, alias="INITIAL_CAPITAL")
    commission_per_trade: float = Field(default=0.001, alias="COMMISSION_PER_TRADE")
    slippage_percentage: float = Field(default=0.0001, alias="SLIPPAGE_PERCENTAGE")
    
    # Monitoring
    prometheus_port: int = Field(default=9090, alias="PROMETHEUS_PORT")
    grafana_port: int = Field(default=3000, alias="GRAFANA_PORT")
    
    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_format: str = Field(default="json", alias="LOG_FORMAT")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
