# Learnings & Corrections

<!-- Append-only. Read before every iteration. Each entry needs: evidence, scope, confidence. -->

---

## Learning L1 — Iteration 1 — Phase: IMPLEMENT

### What Went Wrong
Node.js/npm not available in the environment, preventing use of planned JavaScript/Three.js tech stack.

### Root Cause
Original plan assumed Node.js availability, but only Python 3.11.9 is installed on the system.

### Evidence
```bash
$ node --version
node : The term 'node' is not recognized as the name of a cmdlet, function, script file, or operable program.

$ npm --version
npm : The term 'npm' is not recognized as the name of a cmdlet, function, script file, or operable program.
```

### Fix Applied
Pivoted to Python-based implementation using NumPy for physics, PyQt/PySide for GUI, and OpenGL/vispy for GPU-accelerated rendering.

### Prevention Rule
**Scope**: Project technology selection
**Rule**: Verify runtime availability before planning implementation. Check for required tools (node, npm, python, etc.) in the environment before committing to a tech stack. Have fallback options ready.

### Metadata
- **Scope**: Environment setup
- **Confidence**: high
- **Date**: 2026-07-04
- **Supersedes**: none

---

## Learning L2 — Iteration 1 — Phase: IMPLEMENT

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

## Learning L3 — Iteration 1 — Phase: IMPLEMENT

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

## Learning L4 — Iteration 1 — Phase: VERIFY

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

## Learning L5 — Iteration 1 — Phase: VERIFY

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

<!--
## Learning L[N] — Iteration [M] — Phase: [IMPLEMENT | VERIFY | ADVERSARIAL | EVALUATE]

### What Went Wrong
[Specific: file paths, exact error messages, command + output]

### Root Cause
[WHY it happened — not symptoms, but the actual cause]

### Evidence
[Paste the command you ran and the output that proves this diagnosis]
```
$ [command]
[output]
```

### Fix Applied
[What you did to fix it — specific file changes]

### Prevention Rule
[A concrete, scoped rule for future iterations]

### Metadata
- **Scope**: [specific file / framework / language / universal]
- **Confidence**: [high | medium | low]
- **Date**: [YYYY-MM-DD]
- **Supersedes**: [L[N] if this replaces a previous learning, otherwise "none"]

---
-->
