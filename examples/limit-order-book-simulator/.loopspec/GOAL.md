# Goal

<!--
  INSTRUCTIONS FOR HUMAN:
  Fill in the sections below to define what you want the AI model to achieve.
  Be as specific as possible — the model will use this as its north star.

  Each criterion MUST have a unique ID (C1, C2, ...) — the model uses these
  for traceability throughout the protocol.

  After filling this out, tell the model: "Read .loopspec/PROTOCOL.md and begin."
-->

## Objective

Build a realistic Limit Order Book Market Simulator - a simplified NASDAQ matching engine that simulates a live electronic market where multiple agents trade against each other.

The simulator must support:
- Event-driven order matching with price-time priority
- Multiple agent types (market makers, retail traders, arbitrage bots, momentum traders, institutional traders)
- Various order types (limit, market, cancel, modify)
- Realistic market dynamics (volatility regimes, liquidity droughts, flash crashes, news shocks)
- Latency simulation for each agent
- Comprehensive metrics tracking
- Real-time visualization

## Success Criteria

| ID | Criterion | Verifier | Threshold | Required |
|----|-----------|----------|-----------|----------|
| C1 | Matching engine implements price-time priority | automated | Orders matched by price first, then timestamp | yes |
| C2 | Matching engine supports partial fills | automated | Partial fills executed correctly when insufficient volume | yes |
| C3 | Matching engine maintains order queues | automated | Orders queued correctly at each price level | yes |
| C4 | Matching engine preserves bid/ask spread mechanics | automated | Spread calculated correctly from best bid/ask | yes |
| C5 | Market maker agent maintains spread | automated | Agent places orders on both sides maintaining target spread | yes |
| C6 | Market maker agent balances inventory | automated | Agent adjusts quotes based on inventory position | yes |
| C7 | Momentum trader buys upward moves | automated | Agent places buy orders when price trend is up | yes |
| C8 | Momentum trader sells downward moves | automated | Agent places sell orders when price trend is down | yes |
| C9 | Arbitrage bot exploits temporary inefficiencies | automated | Agent detects and trades on price discrepancies | yes |
| C10 | Institutional trader implements TWAP execution | automated | Agent executes orders evenly over time window | yes |
| C11 | Institutional trader implements VWAP execution | automated | Agent executes orders weighted by volume | yes |
| C12 | All agent behaviors are stochastic | automated | Agent decisions include randomness, not deterministic | yes |
| C13 | Simulator supports volatility regimes | automated | Volatility parameter affects order flow and price movement | yes |
| C14 | Simulator supports liquidity droughts | automated | Liquidity parameter affects order book depth | yes |
| C15 | Simulator supports flash crash scenarios | automated | Flash crash scenario produces rapid price decline | yes |
| C16 | Simulator supports news shocks | automated | News events cause sudden order flow changes | yes |
| C17 | Prices emerge from order flow, not hardcoded | automated | Final prices determined by order matching, not preset | yes |
| C18 | Each agent has network delay simulation | automated | Network delay applied to order submission | yes |
| C19 | Each agent has execution delay simulation | automated | Execution delay applied to order matching | yes |
| C20 | Each agent has cancellation delay simulation | automated | Cancellation delay applied to cancel orders | yes |
| C21 | Metrics engine tracks PnL by agent | automated | PnL calculated correctly for each agent | yes |
| C22 | Metrics engine tracks spread evolution | automated | Spread time series recorded correctly | yes |
| C23 | Metrics engine tracks inventory risk | automated | Inventory risk metrics calculated correctly | yes |
| C24 | Metrics engine tracks order book depth | automated | Book depth metrics recorded correctly | yes |
| C25 | Metrics engine tracks slippage | automated | Slippage calculated correctly for market orders | yes |
| C26 | Metrics engine tracks fill ratio | automated | Fill ratio calculated correctly for limit orders | yes |
| C27 | Visualization shows order book heatmap | manual | Heatmap displays bid/ask depth by price | yes |
| C28 | Visualization shows trade tape | manual | Trade tape displays executed trades in real-time | yes |
| C29 | Visualization shows price chart | manual | Price chart displays mid-price over time | yes |
| C30 | Visualization shows agent positions | manual | Agent positions displayed in real-time | yes |
| C31 | Simulator processes 1M+ orders | metric | Total orders processed >= 1,000,000 | yes |
| C32 | Deterministic replay works | automated | Same seed produces identical results | yes |
| C33 | No book inconsistency | automated | Order book state always valid (no negative quantities) | yes |
| C34 | Price conservation holds | automated | Total value conserved across all trades | yes |
| C35 | Latency model works | automated | Delays affect order timing as expected | yes |
| C36 | Flash crash scenario reproducible | automated | Flash crash produces consistent results across runs | yes |
| C37 | PnL accounting balances exactly | automated | Sum of all agent PnL equals zero (ignoring fees) | yes |

## Permissions

<!--
  Check what the model is ALLOWED to do.
  Unchecked items are FORBIDDEN — the model must ask before doing them.
-->

### Standard Permissions
- [x] Read all project files
- [x] Create new files
- [x] Modify existing files
- [x] Delete files
- [x] Execute shell commands
- [x] Run tests
- [x] Git operations (commit, branch, push)
- [x] Install dependencies (npm, pip, cargo, etc.)
- [x] Modify configuration files

### Safety-Gated Permissions (require explicit approval per action)
- [ ] Access network / external APIs
- [ ] Modify database schemas
- [ ] Deploy to production/staging
- [ ] Actions involving secrets/credentials
- [ ] Paid API calls or cloud resource creation
- [ ] Irreversible operations (publish, send, delete remote)

## Constraints

- Must use Python 3.10+ or Rust for performance-critical components
- Must process 1M+ orders within reasonable time (target: < 5 minutes)
- Must support deterministic replay for testing
- Must maintain exchange correctness exactly (no arbitrage from matching bugs)
- Visualization should be web-based (HTML/Canvas or similar)
- No external dependencies on paid APIs or cloud services

## Priority

Correctness > Performance > Features > Code Style

The matching engine must be mathematically correct above all else. Performance is critical for 1M+ order processing. Features should be added after core correctness is verified.

## Quality Threshold

- All automated tests pass
- Zero order book inconsistencies in any test
- Deterministic replay produces bit-identical results
- PnL accounting balances exactly (sum = 0)
- Code coverage >= 80% on matching engine

## Max Iterations

max_iterations: 10

## Additional Context

This is a high-performance systems programming task that requires careful attention to:
- Concurrency and thread safety
- Event-driven architecture
- State consistency under high load
- Deterministic behavior for testing

The simulator should be able to run flash crash scenarios reproducibly, which requires careful handling of random number generation and timing.
