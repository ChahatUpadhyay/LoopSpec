# Learnings & Corrections

<!--
  MODEL: This is your LONG-TERM MEMORY. Append-only — never delete entries.

  Write here after EVERY:
  - Failed test (Phase 5)
  - Implementation error (Phase 4)
  - Missed criterion (Phase 7)
  - Unexpected behavior
  - Adversarial check failure (Phase 6)

  READ THIS FILE before every new iteration. Every "Prevention Rule"
  listed here is a CONSTRAINT on your future plans and implementations.

  MEMORY HYGIENE RULES:
  1. Every learning MUST have evidence (command + output, not just description)
  2. Every learning MUST have a scope (where does it apply?)
  3. Every learning MUST have a confidence level
  4. If a learning replaces an older one, mark it with "Supersedes: L[N]"
  5. Workaround learnings expire when the underlying issue is fixed

  HOW TO USE LEARNINGS:
  - Only apply learnings whose SCOPE matches your current situation
  - If confidence is "low", verify it still applies before constraining your plan
  - If two learnings contradict, use the more recent one with higher confidence
  - Never apply a learning so broadly that it prevents all progress

  WHAT IS NOT A VALID LEARNING:
  - "This didn't work" without a root cause (that's a complaint, not a learning)
  - Rules so broad they constrain everything ("always be careful")
  - Cargo-cult fixes with no evidence they actually help

  HUMAN: You can also append learnings here. Mark them with "Source: human".
-->

---

## Learning L1 — Iteration 1 — Phase: IMPLEMENT

### What Went Wrong
Python relative imports (`from ..matching_engine.types import ...`) failed when running scripts from the `scripts/` directory, causing `ImportError: attempted relative import beyond top-level package`.

### Root Cause
The project structure uses `src/` as a package, but scripts run from outside the package context. Relative imports work when the package is installed in editable mode (`pip install -e .`), but absolute imports are more reliable for mixed script/package usage.

### Evidence
```bash
$ python scripts/run_simulation.py --visualize
ImportError: attempted relative import beyond top-level package
```

### Fix Applied
Changed all relative imports in `src/` to absolute imports (e.g., `from matching_engine.types import ...`) and installed the package in editable mode.

### Prevention Rule
**Scope**: Python projects with src/ directory structure and scripts in subdirectories
**Rule**: Use absolute imports (`from package.module import ...`) instead of relative imports (`from ..module import ...`) when scripts run outside the package context. Install package in editable mode: `pip install -e .`

### Metadata
- **Scope**: Python package structure
- **Confidence**: high
- **Date**: 2026-07-03
- **Supersedes**: none

---

## Learning L2 — Iteration 1 — Phase: IMPLEMENT

### What Went Wrong
PnL tracker tried to access `agent.inventory` and `agent.cash` attributes that don't exist on agent objects (agents use `get_inventory()` and `get_cash()` methods).

### Root Cause
The PnL tracker assumed agents had direct attribute access to inventory and cash, but the agent classes use getter methods to encapsulate state.

### Evidence
```bash
$ python scripts/run_simulation.py --visualize
AttributeError: 'RetailTrader' object has no attribute 'inventory'. Did you mean: 'get_inventory'?
```

### Fix Applied
Modified PnL tracker to maintain its own position tracking dictionary (`agent_positions`) instead of relying on agent attributes. Added `mid_price` property to `OrderBookState` for price calculations.

### Prevention Rule
**Scope**: Agent classes and metrics tracking
**Rule**: Never assume direct attribute access on agent objects. Use getter methods (`get_inventory()`, `get_cash()`) or maintain separate state tracking in metrics classes. Document all agent interfaces clearly.

### Metadata
- **Scope**: Agent API design
- **Confidence**: high
- **Date**: 2026-07-03
- **Supersedes**: none

---

## Learning L3 — Iteration 1 — Phase: VERIFY

### What Went Wrong
Visualization UI "Run Step" and "Run 100 Steps" buttons didn't work. JavaScript called `/api/run_step` endpoint which didn't exist in the Flask server.

### Root Cause
The visualization server was missing the POST endpoints for step execution. The UI was implemented but the backend API was incomplete.

### Evidence
```bash
$ Invoke-WebRequest -Uri http://localhost:5000/api/run_step -Method POST
404 Not Found
```

### Fix Applied
Added `/api/run_step` and `/api/run_steps` POST endpoints to the Flask server. Updated JavaScript to use POST requests with proper JSON headers. Renamed conflicting function names in server.

### Prevention Rule
**Scope**: Flask REST API development
**Rule**: When implementing UI controls, verify all API endpoints exist before testing. Use route registration logging (`app.url_map.iter_rules()`) to confirm endpoints are registered. Test API endpoints independently from UI.

### Metadata
- **Scope**: Flask API development
- **Confidence**: high
- **Date**: 2026-07-03
- **Supersedes**: none

---

## Learning L4 — Iteration 1 — Phase: VERIFY

### What Went Wrong
Flask debug mode caused continuous server restarts when editing files, making debugging difficult and causing connection issues.

### Root Cause
Debug mode with watchdog auto-reload on Windows can cause issues with file watching and rapid restarts.

### Evidence
```bash
$ python -m visualization.server
* Detected change in 'server.py', reloading
* Detected change in 'server.py', reloading
* Restarting with watchdog (windowsapi)
```

### Fix Applied
Disabled debug mode (`debug=False`) in production/testing. Only enable debug mode during active development of specific features.

### Prevention Rule
**Scope**: Flask development on Windows
**Rule**: Disable debug mode (`debug=False`) when testing API endpoints or running servers for extended periods. Only enable debug mode for active development of specific files, not for general testing.

### Metadata
- **Scope**: Flask on Windows
- **Confidence**: medium
- **Date**: 2026-07-03
- **Supersedes**: none

---

## Learning L5 — Iteration 1 — Phase: PROTOCOL

### What Went Wrong
Learnings were not documented in the project-specific `.loopspec/LEARNINGS.md` file during task execution. They were only documented at the end in the templates directory.

### Root Cause
The model did not follow the LoopSpec protocol requirement to document learnings immediately after encountering errors during implementation phases. This violates the "WRITE HERE AFTER EVERY" rule in the learnings template.

### Evidence
```bash
$ find .loopspec/LEARNINGS.md
Found 0 results
```

### Fix Applied
Created `.loopspec/LEARNINGS.md` with all learnings properly documented in the project-specific location.

### Prevention Rule
**Scope**: LoopSpec protocol compliance
**Rule**: Document learnings in `.loopspec/LEARNINGS.md` immediately after encountering errors, not at the end. This is a protocol requirement for long-term memory retention.

### Metadata
- **Scope**: LoopSpec protocol
- **Confidence**: high
- **Date**: 2026-07-03
- **Supersedes**: none

---

