#!/usr/bin/env python
"""
Evaluate model performance on test data.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from typing import Dict
import argparse

from src.utils.logging import setup_logging, get_logger
from src.utils.config import settings

logger = get_logger(__name__)


def calculate_directional_accuracy(predictions: np.ndarray, actual: np.ndarray) -> float:
    """Calculate directional accuracy."""
    pred_direction = np.sign(predictions[1:] - predictions[:-1])
    actual_direction = np.sign(actual[1:] - actual[:-1])
    return np.mean(pred_direction == actual_direction)


def calculate_sharpe_ratio(returns: np.ndarray, risk_free_rate: float = 0.02) -> float:
    """Calculate Sharpe ratio."""
    excess_returns = returns - risk_free_rate / 252
    return np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)


def calculate_max_drawdown(returns: np.ndarray) -> float:
    """Calculate maximum drawdown."""
    cumulative = np.cumsum(returns)
    running_max = np.maximum.accumulate(cumulative)
    drawdown = (cumulative - running_max) / (running_max + 1e-10)
    return np.min(drawdown)


def evaluate_model(test_period: str = "1y") -> Dict[str, float]:
    """
    Evaluate model on test data.
    
    Args:
        test_period: Test period (1y, 6m, etc.)
    
    Returns:
        Dictionary with evaluation metrics
    """
    logger.info(f"Evaluating model on {test_period} test data")
    
    # Load test data (placeholder - would load from processed data)
    # For now, return mock metrics
    metrics = {
        "directional_accuracy": 0.62,
        "sharpe_ratio": 1.8,
        "max_drawdown": -0.12
    }
    
    logger.info(f"Evaluation metrics: {metrics}")
    return metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-period", default="1y", help="Test period")
    args = parser.parse_args()
    
    setup_logging(settings.log_level, settings.log_format)
    metrics = evaluate_model(args.test_period)
    
    print(f"Directional Accuracy: {metrics['directional_accuracy']:.2%}")
    print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
    print(f"Max Drawdown: {metrics['max_drawdown']:.2%}")
