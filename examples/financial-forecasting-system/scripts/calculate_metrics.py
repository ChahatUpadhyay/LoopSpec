#!/usr/bin/env python
"""
Calculate performance metrics from backtest results.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import pandas as pd
import numpy as np

from src.utils.logging import setup_logging, get_logger
from src.utils.config import settings

logger = get_logger(__name__)


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


def calculate_metrics(metric: str = "sharpe") -> float:
    """
    Calculate specified metric.
    
    Args:
        metric: Metric to calculate (sharpe, max_drawdown)
    
    Returns:
        Metric value
    """
    logger.info(f"Calculating {metric} metric")
    
    # Load backtest results (placeholder)
    # For now, return mock values
    if metric == "sharpe":
        return 1.8
    elif metric == "max_drawdown":
        return -0.12
    else:
        raise ValueError(f"Unknown metric: {metric}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--metric", required=True, help="Metric to calculate")
    args = parser.parse_args()
    
    setup_logging(settings.log_level, settings.log_format)
    value = calculate_metrics(args.metric)
    
    print(f"{args.metric.capitalize()}: {value:.4f}")
