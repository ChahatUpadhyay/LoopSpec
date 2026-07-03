#!/usr/bin/env python
"""
End-to-end pipeline script for financial forecasting system.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.ingestion import download_all_stocks
from src.data.cleaning import clean_stock_data
from src.data.features import engineer_features
from src.models.selection import train_and_select
from src.backtesting.engine import run_backtest
from src.utils.logging import setup_logging, get_logger
from src.utils.config import settings

# Setup logging
setup_logging(settings.log_level, settings.log_format)
logger = get_logger(__name__)


def run_pipeline(test_mode: bool = False):
    """
    Run the complete pipeline.
    
    Args:
        test_mode: If True, use smaller dataset for testing
    """
    logger.info("Starting end-to-end pipeline")
    
    # Step 1: Download data
    logger.info("Step 1: Downloading stock data")
    num_stocks = 10 if test_mode else settings.num_stocks
    data_dict = download_all_stocks(num_stocks=num_stocks)
    
    if not data_dict:
        logger.error("No data downloaded, exiting")
        return False
    
    # Step 2: Process first stock as example
    logger.info("Step 2: Processing data")
    symbol = list(data_dict.keys())[0]
    data = data_dict[symbol]
    
    # Clean data
    clean_data = clean_stock_data(data)
    
    # Engineer features
    features = engineer_features(clean_data)
    
    # Step 3: Train models
    logger.info("Step 3: Training models")
    # Split data
    train_size = int(len(features) * 0.8)
    X = features.drop(columns=["close", "date"] if "date" in features.columns else ["close"])
    y = features["close"]
    
    X_train = X.iloc[:train_size]
    y_train = y.iloc[:train_size]
    X_test = X.iloc[train_size:]
    y_test = y.iloc[train_size:]
    
    # Train and select best model
    best_model, model_name, metrics = train_and_select(X_train, y_train, X_test, y_test)
    
    logger.info(f"Best model: {model_name}")
    logger.info(f"Metrics: {metrics}")
    
    # Step 4: Backtest
    logger.info("Step 4: Running backtest")
    predictions = best_model.predict(X_test)
    trades_df, backtest_metrics = run_backtest(
        data.iloc[train_size:],
        predictions,
        initial_capital=100000
    )
    
    logger.info(f"Backtest metrics: {backtest_metrics}")
    
    logger.info("Pipeline completed successfully")
    return True


if __name__ == "__main__":
    test_mode = "--test" in sys.argv
    success = run_pipeline(test_mode=test_mode)
    sys.exit(0 if success else 1)
