"""Flask server for real-time visualization data."""

from flask import Flask, jsonify, render_template
from typing import Dict, List, Optional
import json
from simulation.engine import SimulationEngine
from simulation.scenarios import ScenarioManager
from metrics.tracker import MetricsTracker
from metrics.pnl import PnLTracker


app = Flask(__name__, template_folder='templates')

# Global simulation state
simulation_engine: Optional[SimulationEngine] = None
metrics_tracker: Optional[MetricsTracker] = None
pnl_tracker: Optional[PnLTracker] = None
scenario_manager: Optional[ScenarioManager] = None


@app.route('/')
def index():
    """Serve the visualization UI."""
    return render_template('index.html')


@app.route('/api/orderbook')
def get_orderbook():
    """Get current order book state."""
    if simulation_engine is None:
        return jsonify({'error': 'Simulation not running'}), 404
    
    state = simulation_engine.get_order_book_state()
    return jsonify({
        'timestamp': state.timestamp,
        'best_bid': state.best_bid,
        'best_ask': state.best_ask,
        'bid_depth': state.bid_depth,
        'ask_depth': state.ask_depth,
        'total_bid_volume': state.total_bid_volume,
        'total_ask_volume': state.total_ask_volume
    })


@app.route('/api/trades')
def get_trades():
    """Get recent trades."""
    if simulation_engine is None:
        return jsonify({'error': 'Simulation not running'}), 404
    
    trades = simulation_engine.get_trades()
    # Return last 100 trades
    recent_trades = trades[-100:] if len(trades) > 100 else trades
    
    return jsonify([
        {
            'trade_id': t.trade_id,
            'price': t.price,
            'quantity': t.quantity,
            'timestamp': t.timestamp,
            'buy_agent_id': t.buy_agent_id,
            'sell_agent_id': t.sell_agent_id
        }
        for t in recent_trades
    ])


@app.route('/api/agents')
def get_agents():
    """Get agent positions."""
    if simulation_engine is None:
        return jsonify({'error': 'Simulation not running'}), 404
    
    agents = []
    for agent in simulation_engine.agents:
        agents.append({
            'agent_id': agent.agent_id,
            'agent_type': agent.agent_type,
            'inventory': agent.get_inventory(),
            'cash': agent.get_cash(),
            'pnl': agent.get_pnl()
        })
    
    return jsonify(agents)


@app.route('/api/metrics')
def get_metrics():
    """Get current metrics."""
    if metrics_tracker is None:
        return jsonify({'error': 'Metrics tracker not initialized'}), 404
    
    return jsonify({
        'average_spread': metrics_tracker.get_average_spread(),
        'average_slippage': metrics_tracker.get_average_slippage(),
        'average_fill_ratio': metrics_tracker.get_average_fill_ratio(),
        'order_count': simulation_engine.get_order_count() if simulation_engine else 0,
        'trade_count': simulation_engine.get_trade_count() if simulation_engine else 0
    })


@app.route('/api/spread_history')
def get_spread_history():
    """Get spread history."""
    if metrics_tracker is None:
        return jsonify({'error': 'Metrics tracker not initialized'}), 404
    
    history = metrics_tracker.get_spread_history()
    return jsonify([
        {
            'timestamp': h.timestamp,
            'spread': h.spread,
            'bid': h.bid,
            'ask': h.ask
        }
        for h in history
    ])


@app.route('/api/depth_history')
def get_depth_history():
    """Get depth history."""
    if metrics_tracker is None:
        return jsonify({'error': 'Metrics tracker not initialized'}), 404
    
    history = metrics_tracker.get_depth_history()
    return jsonify([
        {
            'timestamp': h.timestamp,
            'bid_depth': h.bid_depth,
            'ask_depth': h.ask_depth,
            'total_bid_volume': h.total_bid_volume,
            'total_ask_volume': h.total_ask_volume
        }
        for h in history
    ])


@app.route('/api/run_step', methods=['POST'])
def api_run_step():
    """Run one simulation step."""
    if simulation_engine is None:
        return jsonify({'error': 'Simulation not running'}), 404
    
    run_simulation_step()
    return jsonify({'success': True})


@app.route('/api/run_steps', methods=['POST'])
def api_run_steps():
    """Run multiple simulation steps."""
    if simulation_engine is None:
        return jsonify({'error': 'Simulation not running'}), 404
    
    from flask import request
    count = request.json.get('count', 1) if request.json else 1
    
    for _ in range(count):
        run_simulation_step()
    
    return jsonify({'success': True, 'steps_run': count})


def initialize_simulation(seed: Optional[int] = None):
    """Initialize simulation with default configuration.
    
    Args:
        seed: Random seed for deterministic behavior
    """
    global simulation_engine, metrics_tracker, pnl_tracker, scenario_manager
    
    scenario_manager = ScenarioManager(seed)
    simulation_engine = scenario_manager.create_normal_market_engine(seed=seed)
    metrics_tracker = MetricsTracker()
    pnl_tracker = PnLTracker()
    
    # Add agents to PnL tracker
    for agent in simulation_engine.agents:
        pnl_tracker.add_agent(agent.agent)


def run_simulation_step():
    """Run one simulation step and update metrics."""
    global simulation_engine, metrics_tracker, pnl_tracker
    
    if simulation_engine is None:
        return
    
    # Run one step
    trades = simulation_engine.step()
    
    # Record metrics
    order_book_state = simulation_engine.get_order_book_state()
    metrics_tracker.record_spread(order_book_state)
    metrics_tracker.record_depth(order_book_state)
    
    # Update agent inventory in metrics
    for agent in simulation_engine.agents:
        metrics_tracker.record_inventory(agent.agent_id, agent.get_inventory())
    
    # Record trades in PnL tracker
    current_price = order_book_state.mid_price or 100.0
    for trade in trades:
        pnl_tracker.record_trade(trade, current_price)
    
    # Record PnL for all agents
    for agent in simulation_engine.agents:
        pnl_tracker.record_pnl(agent.agent_id, current_price, simulation_engine.current_time)


if __name__ == '__main__':
    initialize_simulation(seed=42)
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.methods} {rule.rule}")
    app.run(host='0.0.0.0', port=5000, debug=False)
