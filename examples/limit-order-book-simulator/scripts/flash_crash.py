"""Flash crash scenario script."""

import sys
import os
import argparse
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from simulation.engine import SimulationEngine
from simulation.scenarios import ScenarioManager
from metrics.tracker import MetricsTracker
from metrics.pnl import PnLTracker


def main():
    parser = argparse.ArgumentParser(description='Run flash crash scenario')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    parser.add_argument('--steps', type=int, default=500, help='Number of simulation steps')
    parser.add_argument('--repeat', type=int, default=1, help='Number of times to repeat')
    
    args = parser.parse_args()
    
    print(f"Running flash crash scenario with seed={args.seed}, steps={args.steps}")
    
    all_price_series = []
    
    for run in range(args.repeat):
        print(f"\nRun {run + 1}/{args.repeat}")
        
        # Initialize scenario manager
        scenario_manager = ScenarioManager(seed=args.seed)
        
        # Create flash crash engine
        engine = scenario_manager.create_flash_crash_engine(seed=args.seed)
        
        # Initialize metrics
        metrics_tracker = MetricsTracker()
        pnl_tracker = PnLTracker()
        
        # Add agents to PnL tracker
        for agent in engine.agents:
            pnl_tracker.add_agent(agent.agent_id)
        
        # Track price series
        price_series = []
        
        # Run simulation
        for step in range(args.steps):
            # Run one step
            trades = engine.step()
            
            # Record metrics
            order_book_state = engine.get_order_book_state()
            metrics_tracker.record_spread(order_book_state)
            metrics_tracker.record_depth(order_book_state)
            
            # Track mid price
            mid_price = (order_book_state.best_bid + order_book_state.best_ask) / 2
            if mid_price > 0:
                price_series.append(mid_price)
            
            # Record trades in PnL tracker
            current_price = order_book_state.best_bid or 100.0
            for trade in trades:
                pnl_tracker.record_trade(trade, current_price)
            
            # Record PnL for all agents
            for agent in engine.agents:
                pnl_tracker.record_pnl(agent.agent_id, current_price, engine.current_time)
        
        all_price_series.append(price_series)
        
        # Print summary for this run
        print(f"Orders: {engine.get_order_count()}, Trades: {engine.get_trade_count()}")
        if price_series:
            initial_price = price_series[0]
            min_price = min(price_series)
            max_decline = (initial_price - min_price) / initial_price * 100
            print(f"Initial price: {initial_price:.2f}")
            print(f"Min price: {min_price:.2f}")
            print(f"Max decline: {max_decline:.2f}%")
    
    # Check reproducibility if multiple runs
    if args.repeat > 1:
        print("\n" + "="*50)
        print("REPRODUCIBILITY CHECK")
        print("="*50)
        
        if len(all_price_series) >= 2:
            # Compare first two runs
            series1 = all_price_series[0]
            series2 = all_price_series[1]
            
            if len(series1) == len(series2):
                # Calculate correlation
                import statistics
                mean1 = statistics.mean(series1)
                mean2 = statistics.mean(series2)
                
                covariance = sum((x - mean1) * (y - mean2) for x, y in zip(series1, series2))
                variance1 = sum((x - mean1) ** 2 for x in series1)
                variance2 = sum((y - mean2) ** 2 for y in series2)
                
                if variance1 > 0 and variance2 > 0:
                    correlation = covariance / (variance1 ** 0.5 * variance2 ** 0.5)
                    print(f"Price series correlation: {correlation:.4f}")
                    print(f"Reproducible: {correlation > 0.99}")
                else:
                    print("Cannot calculate correlation (zero variance)")
            else:
                print(f"Series lengths differ: {len(series1)} vs {len(series2)}")


if __name__ == '__main__':
    main()
