# Project Context

<!--
  MODEL: Fill this during Phase 1 (ANALYZE).
  Strategy: Broad scan, narrow record.
  - Scan everything to understand the full picture
  - Record only what's relevant to the goal
  - Be specific and accurate — no guessing
  - Include actual evidence (commands run + output) for baseline
-->

## Tech Stack

**Primary Language**: Python 3.10+ (for core logic and agent behaviors)
**Alternative**: Rust (optional for performance-critical matching engine if needed)

**Core Libraries**:
- `asyncio` - Event-driven architecture and concurrency
- `dataclasses` - Order and agent data structures
- `typing` - Type hints for correctness
- `random` - Stochastic agent behaviors (with seed for determinism)
- `time` - Latency simulation
- `collections` - Order queues (deque, defaultdict)
- `heapq` - Priority queues for price-time ordering
- `threading` or `multiprocessing` - Concurrent agent execution

**Visualization**:
- HTML5 Canvas or SVG for real-time visualization
- JavaScript for client-side rendering
- WebSocket or polling for real-time updates

**Testing**:
- `pytest` - Test framework
- `unittest.mock` - Mocking for agent testing

**Performance**:
- `numpy` - Efficient numerical operations (optional)
- `pandas` - Metrics analysis (optional)

## Project Structure

```
limit-order-book-simulator/
├── .loopspec/
│   ├── GOAL.md
│   ├── CONTEXT.md
│   ├── PLAN.md
│   ├── TESTS.md
│   ├── STATUS.md
│   ├── STATUS.json
│   └── CHANGELOG.md
├── src/
│   ├── matching_engine/
│   │   ├── __init__.py
│   │   ├── order_book.py      # Order book state management
│   │   ├── matching.py        # Order matching logic
│   │   └── types.py           # Order, Trade, Agent dataclasses
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base.py            # Base agent class
│   │   ├── market_maker.py    # Market maker agent
│   │   ├── momentum.py        # Momentum trader agent
│   │   ├── arbitrage.py       # Arbitrage bot agent
│   │   ├── institutional.py   # Institutional trader agent
│   │   └── retail.py          # Retail trader agent
│   ├── simulation/
│   │   ├── __init__.py
│   │   ├── engine.py          # Main simulation loop
│   │   ├── latency.py         # Latency simulation
│   │   └── scenarios.py       # Market scenarios (flash crash, etc.)
│   ├── metrics/
│   │   ├── __init__.py
│   │   ├── tracker.py         # Metrics collection
│   │   └── pnl.py             # PnL accounting
│   └── visualization/
│       ├── __init__.py
│       ├── server.py          # Web server for visualization
│       └── templates/
│           └── index.html     # Visualization UI
├── tests/
│   ├── test_matching/
│   │   ├── test_order_book.py
│   │   └── test_matching.py
│   ├── test_agents/
│   │   ├── test_market_maker.py
│   │   ├── test_momentum.py
│   │   └── test_arbitrage.py
│   ├── test_simulation/
│   │   ├── test_engine.py
│   │   └── test_latency.py
│   └── test_metrics/
│       └── test_pnl.py
├── scripts/
│   ├── run_simulation.py      # Main simulation script
│   ├── flash_crash.py         # Flash crash scenario
│   └── benchmark.py           # Performance benchmark
├── requirements.txt
├── setup.py
├── README.md
└── .gitignore
```

## Architecture Overview

**Event-Driven Simulation**:
- Discrete time steps with agent order generation
- Matching engine processes orders sequentially
- Latency simulation delays order execution
- Metrics collected in real-time

**Data Flow**:
1. Agents generate orders (limit, market, cancel, modify)
2. Orders pass through latency simulation
3. Matching engine processes orders against order book
4. Trades generated and recorded
5. Metrics engine tracks PnL, spread, depth, etc.
6. Visualization updates via WebSocket/polling

**Design Patterns**:
- Observer pattern for order book updates
- Strategy pattern for agent behaviors
- Factory pattern for order creation
- State pattern for order lifecycle

## Key Files & Their Roles

| File | Role | Relevant to Criteria |
|------|------|---------------------|
| `src/matching_engine/order_book.py` | Order book state management | C1, C3, C4 |
| `src/matching_engine/matching.py` | Order matching logic | C1, C2, C3, C4 |
| `src/matching_engine/types.py` | Order, Trade, Agent dataclasses | All criteria |
| `src/agents/market_maker.py` | Market maker agent | C5, C6 |
| `src/agents/momentum.py` | Momentum trader agent | C7, C8 |
| `src/agents/arbitrage.py` | Arbitrage bot agent | C9 |
| `src/agents/institutional.py` | Institutional trader agent | C10, C11 |
| `src/simulation/engine.py` | Main simulation loop | C12, C17, C31, C32 |
| `src/simulation/latency.py` | Latency simulation | C18, C19, C20, C35 |
| `src/simulation/scenarios.py` | Market scenarios | C13, C14, C15, C16, C36 |
| `src/metrics/tracker.py` | Metrics collection | C21-C26 |
| `src/metrics/pnl.py` | PnL accounting | C21, C34, C37 |
| `src/visualization/server.py` | Web server for visualization | C27-C30 |
| `src/visualization/templates/index.html` | Visualization UI | C27-C30 |

## Dependencies

**Core**:
- Python 3.10+ (standard library only for core logic)
- pytest (testing)
- flask or fastapi (visualization server)

**Optional**:
- numpy (performance)
- pandas (metrics analysis)
- matplotlib (static charts)

## Existing Tests

**Current State**: No existing tests (greenfield project)

**Test Infrastructure to be Created**:
- pytest for unit and integration tests
- Test runner command: `pytest tests/`
- Coverage target: >= 80% on matching engine

## Baseline State

**Current State**: Empty project directory (greenfield)

**Working**: None (no code exists yet)
**Broken**: None (no code exists yet)

**Evidence**:
```
$ dir
 Directory: C:\Users\chaha\Documents\Codex\2026-06-28\e\LoopSpec\examples\limit-order-book-simulator

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        03-07-2026     01:14                .loopspec
```

## Available Runtimes

- Python 3.11 (Windows)
- Web browser (Chrome, Firefox, Edge) for visualization
- Git available
- No external cloud services or APIs

## Patterns & Conventions

**Architecture**:
- Event-driven simulation with discrete time steps
- Price-time priority using priority queues
- Immutable order objects (modifications create new orders)
- Deterministic random number generation (seeded)

**Code Style**:
- Type hints on all functions
- Dataclasses for data structures
- Async/await for concurrent agent execution
- Clear separation of concerns (matching, agents, simulation, metrics)

**Testing**:
- Unit tests for matching engine correctness
- Integration tests for agent behaviors
- Property-based tests for invariants (PnL conservation, book consistency)
