"""Main simulation script with configuration options."""

import sys
import os
import argparse
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from simulation.engine import SimulationEngine
from simulation.scenarios import ScenarioManager, MarketScenario
from simulation.latency import LatencyProfile
from metrics.tracker import MetricsTracker
from metrics.pnl import PnLTracker


def main():
    parser = argparse.ArgumentParser(description='Run limit order book simulation')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    parser.add_argument('--steps', type=int, default=1000, help='Number of simulation steps')
    parser.add_argument('--scenario', type=str, default='normal', 
                        choices=['normal', 'flash_crash'], help='Market scenario')
    parser.add_argument('--visualize', action='store_true', help='Start visualization server')
    
    args = parser.parse_args()
    
    print(f"Starting simulation with seed={args.seed}, steps={args.steps}, scenario={args.scenario}")
    
    # Initialize scenario manager
    scenario_manager = ScenarioManager(seed=args.seed)
    
    # Create simulation engine based on scenario
    if args.scenario == 'flash_crash':
        print("Using flash crash scenario")
        engine = scenario_manager.create_flash_crash_engine(seed=args.seed)
    else:
        print("Using normal market scenario")
        engine = scenario_manager.create_normal_market_engine(seed=args.seed)
    
    # Initialize metrics
    metrics_tracker = MetricsTracker()
    pnl_tracker = PnLTracker()
    
    # Add agents to PnL tracker
    for agent in engine.agents:
        pnl_tracker.add_agent(agent)
    
    # Run simulation
    print(f"Running {args.steps} steps...")
    start_time = time.time()
    
    for step in range(args.steps):
        # Run one step
        trades = engine.step()
        
        # Record metrics
        order_book_state = engine.get_order_book_state()
        metrics_tracker.record_spread(order_book_state)
        metrics_tracker.record_depth(order_book_state)
        
        # Update agent inventory in metrics
        for agent in engine.agents:
            metrics_tracker.record_inventory(agent.agent_id, agent.get_inventory())
        
        # Record trades in PnL tracker
        current_price = order_book_state.best_bid or 100.0
        for trade in trades:
            pnl_tracker.record_trade(trade, current_price)
        
        # Record PnL for all agents
        for agent in engine.agents:
            pnl_tracker.record_pnl(agent.agent_id, current_price, engine.current_time)
        
        # Progress update
        if (step + 1) % 100 == 0:
            print(f"Step {step + 1}/{args.steps}: {engine.get_order_count()} orders, {engine.get_trade_count()} trades")
    
    elapsed_time = time.time() - start_time
    
    # Print summary
    print("\n" + "="*50)
    print("SIMULATION SUMMARY")
    print("="*50)
    print(f"Steps: {args.steps}")
    print(f"Orders processed: {engine.get_order_count()}")
    print(f"Trades executed: {engine.get_trade_count()}")
    print(f"Elapsed time: {elapsed_time:.2f}s")
    print(f"Orders per second: {engine.get_order_count() / elapsed_time:.2f}")
    avg_spread = metrics_tracker.get_average_spread()
    avg_fill_ratio = metrics_tracker.get_average_fill_ratio()
    spread_str = f"{avg_spread:.4f}" if avg_spread is not None else "N/A"
    fill_ratio_str = f"{avg_fill_ratio:.4f}" if avg_fill_ratio is not None else "N/A"
    print(f"Average spread: {spread_str}")
    print(f"Average fill ratio: {fill_ratio_str}")
    
    # Print PnL summary
    print("\n" + "="*50)
    print("PNL SUMMARY")
    print("="*50)
    all_pnl = pnl_tracker.get_all_pnl()
    for agent_id, pnl in sorted(all_pnl.items()):
        print(f"{agent_id}: {pnl:.2f}")
    
    # Verify balance conservation
    total_pnl = sum(all_pnl.values())
    print(f"\nTotal PnL (should be ~0): {total_pnl:.4f}")
    print(f"Balance conserved: {pnl_tracker.verify_balance_conservation()}")
    
    # Start visualization server if requested
    if args.visualize:
        print("\nStarting visualization server...")
        print("Open http://localhost:5000 in your browser")
        
        from visualization.server import app, initialize_simulation, run_simulation_step
        
        # Initialize server with current simulation state
        initialize_simulation(seed=args.seed)
        
        # Run simulation loop in background
        def simulation_loop():
            while True:
                run_simulation_step()
                time.sleep(0.01)
        
        import threading
        sim_thread = threading.Thread(target=simulation_loop, daemon=True)
        sim_thread.start()
        
        app.run(host='0.0.0.0', port=5000, debug=False)


if __name__ == '__main__':
    main()
