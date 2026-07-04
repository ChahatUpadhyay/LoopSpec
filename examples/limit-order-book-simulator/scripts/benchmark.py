"""Performance benchmark script for 1M+ orders."""

import sys
import os
import argparse
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from simulation.engine import SimulationEngine
from simulation.scenarios import ScenarioManager


def main():
    parser = argparse.ArgumentParser(description='Performance benchmark')
    parser.add_argument('--orders', type=int, default=1000000, help='Target number of orders')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    
    args = parser.parse_args()
    
    print(f"Performance benchmark: target {args.orders} orders")
    print(f"Seed: {args.seed}")
    
    # Initialize scenario manager
    scenario_manager = ScenarioManager(seed=args.seed)
    
    # Create simulation engine with more agents for higher order volume
    engine = scenario_manager.create_normal_market_engine(
        num_market_makers=10,
        num_momentum=5,
        num_arbitrage=3,
        num_institutional=5,
        num_retail=50,
        seed=args.seed
    )
    
    # Run benchmark
    print("Running benchmark...")
    start_time = time.time()
    
    target_orders = args.orders
    step = 0
    
    while engine.get_order_count() < target_orders:
        engine.step()
        step += 1
        
        # Progress update
        if step % 1000 == 0:
            elapsed = time.time() - start_time
            orders_per_sec = engine.get_order_count() / elapsed
            print(f"Step {step}: {engine.get_order_count()} orders ({orders_per_sec:.0f} orders/sec)")
    
    elapsed_time = time.time() - start_time
    
    # Print results
    print("\n" + "="*50)
    print("BENCHMARK RESULTS")
    print("="*50)
    print(f"Target orders: {args.orders}")
    print(f"Actual orders: {engine.get_order_count()}")
    print(f"Steps: {step}")
    print(f"Elapsed time: {elapsed_time:.2f}s")
    print(f"Orders per second: {engine.get_order_count() / elapsed_time:.2f}")
    print(f"Trades executed: {engine.get_trade_count()}")
    
    # Check if target met
    if engine.get_order_count() >= args.orders:
        print(f"\n[TARGET MET] {engine.get_order_count()} >= {args.orders} orders")
    else:
        print(f"\n[TARGET NOT MET] {engine.get_order_count()} < {args.orders} orders")


if __name__ == '__main__':
    main()
