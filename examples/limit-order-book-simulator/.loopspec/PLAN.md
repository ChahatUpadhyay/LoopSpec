# Implementation Plan

## Iteration: 1
## Status: APPROVED

## Summary

Build a production-grade Limit Order Book Market Simulator in Python 3.10+ with event-driven architecture. The implementation will focus on correctness of the matching engine (price-time priority, partial fills, spread mechanics) as the highest priority, followed by performance optimization for 1M+ order processing. The system will include 5 agent types (market maker, momentum, arbitrage, institutional, retail) with stochastic behaviors, latency simulation, market dynamics scenarios, comprehensive metrics tracking, and real-time web-based visualization.

## Learnings Applied

First iteration — no prior learnings.

## Changes Required

### Matching Engine Core

#### File: `src/matching_engine/types.py` — CREATE
- **What**: Define dataclasses for Order, Trade, Agent, OrderBookState
- **Why**: Core data structures for the entire system (all criteria)
- **Criteria**: C1-C4, C17, C21, C33, C34, C37

#### File: `src/matching_engine/order_book.py` — CREATE
- **What**: Implement order book with bid/ask queues, price-time priority using heapq
- **Why**: Core matching engine functionality (C1, C3, C4)
- **Criteria**: C1, C3, C4, C33

#### File: `src/matching_engine/matching.py` — CREATE
- **What**: Implement order matching logic for limit/market/cancel/modify orders with partial fills
- **Why**: Execute trades correctly (C1, C2, C3, C4)
- **Criteria**: C1, C2, C3, C4, C33, C34, C37

### Agent Behaviors

#### File: `src/agents/base.py` — CREATE
- **What**: Abstract base class for all agents with order generation interface
- **Why**: Common interface for all agent types (C5-C12)
- **Criteria**: C5-C12, C12

#### File: `src/agents/market_maker.py` — CREATE
- **What**: Market maker agent with spread maintenance and inventory balancing
- **Why**: Two-sided quoting behavior (C5, C6)
- **Criteria**: C5, C6, C12

#### File: `src/agents/momentum.py` — CREATE
- **What**: Momentum trader agent that buys upward moves, sells downward moves
- **Why**: Trend-following behavior (C7, C8)
- **Criteria**: C7, C8, C12

#### File: `src/agents/arbitrage.py` — CREATE
- **What**: Arbitrage bot that exploits temporary price inefficiencies
- **Why**: Arbitrage behavior (C9)
- **Criteria**: C9, C12

#### File: `src/agents/institutional.py` — CREATE
- **What**: Institutional trader with TWAP and VWAP execution algorithms
- **Why**: Large order execution (C10, C11)
- **Criteria**: C10, C11, C12

#### File: `src/agents/retail.py` — CREATE
- **What**: Retail trader agent with random small orders
- **Why**: Background liquidity provider (C12)
- **Criteria**: C12

### Simulation Engine

#### File: `src/simulation/engine.py` — CREATE
- **What**: Main simulation loop with event scheduling, time management, agent coordination
- **Why**: Orchestrate all components (C12, C17, C31, C32)
- **Criteria**: C12, C17, C31, C32

#### File: `src/simulation/latency.py` — CREATE
- **What**: Latency simulation for network, execution, and cancellation delays
- **Why**: Realistic timing (C18, C19, C20, C35)
- **Criteria**: C18, C19, C20, C35

#### File: `src/simulation/scenarios.py` — CREATE
- **What**: Market scenarios (volatility regimes, liquidity droughts, flash crashes, news shocks)
- **Why**: Market dynamics (C13-C16, C36)
- **Criteria**: C13-C16, C36

### Metrics & Visualization

#### File: `src/metrics/tracker.py` — CREATE
- **What**: Metrics collection for spread, depth, slippage, fill ratio
- **Why**: Track market metrics (C22-C26)
- **Criteria**: C22-C26

#### File: `src/metrics/pnl.py` — CREATE
- **What**: PnL accounting with balance verification
- **Why**: Track agent performance (C21, C34, C37)
- **Criteria**: C21, C34, C37

#### File: `src/visualization/server.py` — CREATE
- **What**: Flask/FastAPI server for real-time visualization data
- **Why**: Serve visualization data (C27-C30)
- **Criteria**: C27-C30

#### File: `src/visualization/templates/index.html` — CREATE
- **What**: HTML/Canvas visualization with order book heatmap, trade tape, price chart, agent positions
- **Why**: Real-time visualization (C27-C30)
- **Criteria**: C27-C30

### Configuration & Scripts

#### File: `requirements.txt` — CREATE
- **What**: Python dependencies (pytest, flask/fastapi, optional numpy/pandas)
- **Why**: Dependency management (all criteria)
- **Criteria**: All

#### File: `setup.py` — CREATE
- **What**: Package setup configuration
- **Why**: Installation (all criteria)
- **Criteria**: All

#### File: `scripts/run_simulation.py` — CREATE
- **What**: Main simulation script with configuration options
- **Why**: Run the simulator (C31, C32)
- **Criteria**: C31, C32

#### File: `scripts/flash_crash.py` — CREATE
- **What**: Flash crash scenario script
- **Why**: Reproduce flash crash (C15, C36)
- **Criteria**: C15, C36

#### File: `scripts/benchmark.py` — CREATE
- **What**: Performance benchmark script for 1M+ orders
- **Why**: Verify performance (C31)
- **Criteria**: C31

### Tests

#### File: `tests/test_matching/test_order_book.py` — CREATE
- **What**: Unit tests for order book state management
- **Why**: Verify book correctness (C1, C3, C4, C33)
- **Criteria**: C1, C3, C4, C33

#### File: `tests/test_matching/test_matching.py` — CREATE
- **What**: Unit tests for order matching logic
- **Why**: Verify matching correctness (C1, C2, C3, C4, C34, C37)
- **Criteria**: C1, C2, C3, C4, C34, C37

#### File: `tests/test_agents/test_market_maker.py` — CREATE
- **What**: Unit tests for market maker behavior
- **Why**: Verify spread maintenance (C5, C6)
- **Criteria**: C5, C6

#### File: `tests/test_agents/test_momentum.py` — CREATE
- **What**: Unit tests for momentum trader behavior
- **Why**: Verify trend following (C7, C8)
- **Criteria**: C7, C8

#### File: `tests/test_agents/test_arbitrage.py` — CREATE
- **What**: Unit tests for arbitrage bot behavior
- **Why**: Verify arbitrage detection (C9)
- **Criteria**: C9

#### File: `tests/test_simulation/test_engine.py` — CREATE
- **What**: Integration tests for simulation engine
- **Why**: Verify end-to-end simulation (C12, C17, C31, C32)
- **Criteria**: C12, C17, C31, C32

#### File: `tests/test_simulation/test_latency.py` — CREATE
- **What**: Unit tests for latency simulation
- **Why**: Verify delay application (C18, C19, C20, C35)
- **Criteria**: C18, C19, C20, C35

#### File: `tests/test_metrics/test_pnl.py` — CREATE
- **What**: Unit tests for PnL accounting
- **Why**: Verify balance conservation (C21, C34, C37)
- **Criteria**: C21, C34, C37

## Traceability Matrix

| Criterion | Planned Changes | Test Strategy |
|-----------|----------------|---------------|
| C1 | matching.py, order_book.py | Unit tests for price-time priority |
| C2 | matching.py | Unit tests for partial fills |
| C3 | order_book.py | Unit tests for order queues |
| C4 | order_book.py, matching.py | Unit tests for spread calculation |
| C5 | market_maker.py | Unit tests for spread maintenance |
| C6 | market_maker.py | Unit tests for inventory balancing |
| C7 | momentum.py | Unit tests for upward move buying |
| C8 | momentum.py | Unit tests for downward move selling |
| C9 | arbitrage.py | Unit tests for inefficiency detection |
| C10 | institutional.py | Unit tests for TWAP execution |
| C11 | institutional.py | Unit tests for VWAP execution |
| C12 | All agents + engine.py | Integration tests for stochastic behavior |
| C13 | scenarios.py | Integration tests for volatility regimes |
| C14 | scenarios.py | Integration tests for liquidity droughts |
| C15 | scenarios.py + flash_crash.py | Integration tests for flash crash |
| C16 | scenarios.py | Integration tests for news shocks |
| C17 | engine.py | Integration tests for price emergence |
| C18 | latency.py | Unit tests for network delay |
| C19 | latency.py | Unit tests for execution delay |
| C20 | latency.py | Unit tests for cancellation delay |
| C21 | pnl.py | Unit tests for PnL tracking |
| C22 | tracker.py | Unit tests for spread tracking |
| C23 | tracker.py | Unit tests for inventory risk |
| C24 | tracker.py | Unit tests for book depth |
| C25 | tracker.py | Unit tests for slippage |
| C26 | tracker.py | Unit tests for fill ratio |
| C27 | server.py + index.html | Manual verification of heatmap |
| C28 | server.py + index.html | Manual verification of trade tape |
| C29 | server.py + index.html | Manual verification of price chart |
| C30 | server.py + index.html | Manual verification of agent positions |
| C31 | engine.py + benchmark.py | Metric: orders processed >= 1M |
| C32 | engine.py | Automated test with same seed |
| C33 | order_book.py + matching.py | Property tests for book consistency |
| C34 | matching.py + pnl.py | Property tests for value conservation |
| C35 | latency.py + engine.py | Integration tests for delay effects |
| C36 | scenarios.py + flash_crash.py | Automated test for reproducibility |
| C37 | pnl.py | Property test for zero-sum PnL |

## Order of Operations

1. Create project structure and configuration files (requirements.txt, setup.py, .gitignore)
2. Implement core data structures (types.py)
3. Implement order book (order_book.py)
4. Implement matching logic (matching.py)
5. Write unit tests for matching engine
6. Implement base agent class (base.py)
7. Implement all agent types (market_maker.py, momentum.py, arbitrage.py, institutional.py, retail.py)
8. Write unit tests for agents
9. Implement latency simulation (latency.py)
10. Implement simulation engine (engine.py)
11. Implement market scenarios (scenarios.py)
12. Write integration tests for simulation
13. Implement metrics tracking (tracker.py, pnl.py)
14. Write unit tests for metrics
15. Implement visualization server (server.py)
16. Implement visualization UI (index.html)
17. Create simulation scripts (run_simulation.py, flash_crash.py, benchmark.py)
18. Run full test suite
19. Performance benchmark for 1M+ orders
20. Manual verification of visualization

## Risks & Mitigations

- **Risk**: Performance bottleneck in matching engine for 1M+ orders
  **Mitigation**: Use efficient data structures (heapq, deque), profile and optimize hot paths, consider Rust for critical sections if needed

- **Risk**: Non-deterministic behavior breaking replay
  **Mitigation**: Seed all random number generators, use deterministic time steps, record all random decisions

- **Risk**: Order book inconsistency under concurrent access
  **Mitigation**: Use single-threaded event loop initially, add thread safety if needed, extensive property-based testing

- **Risk**: PnL accounting errors due to floating-point precision
  **Mitigation**: Use decimal.Decimal for financial calculations, verify balance conservation with tolerance

- **Risk**: Visualization performance degradation with high order volume
  **Mitigation**: Sample data for visualization, use efficient canvas rendering, implement throttling

## Scope Boundary

**IN**:
- All files in src/ directory
- All files in tests/ directory
- All files in scripts/ directory
- Configuration files (requirements.txt, setup.py, .gitignore, README.md)
- LoopSpec protocol files (.loopspec/)

**OUT**:
- External APIs or cloud services
- Paid services or dependencies
- Database persistence (in-memory only)
- Real trading integration (simulation only)
- Advanced features not in criteria (e.g., options, futures, multi-asset)

---

> **HUMAN APPROVAL**: [x] APPROVED
>
> _Model will not proceed to Phase 3 until this checkbox is marked `[x]`._
>
> **Human Notes** _(optional)_:
>
