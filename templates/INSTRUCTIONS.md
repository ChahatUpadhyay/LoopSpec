# Template Instructions (Reference Only)

> This file is NOT loaded during normal protocol execution.
> It exists for first-time users who need help filling templates.
> The AI model should NOT read this file — it adds context cost with no benefit.

## GOAL.md Instructions

Each criterion MUST have:
- A unique ID (C1, C2, ...)
- A clear, objectively verifiable description
- A verifier type: automated test, manual check, or metric
- A threshold: what "pass" means
- Required flag: yes/no

Permissions checklist: check what the model is ALLOWED to do.
Unchecked items are FORBIDDEN — model must ask before doing them.

## CONTEXT.md Instructions

Fill during Phase 1 (ANALYZE). Include:
- Tech Stack (languages, frameworks, versions)
- Project Structure (directory layout)
- Architecture Overview (how components connect)
- Key Files (most important for this goal)
- Dependencies (external packages/services)
- Existing Tests (how to run, coverage)
- Baseline State (what works/fails BEFORE changes — include command output)
- Available Runtimes (tools in environment)

## PLAN.md Instructions

Fill during Phase 2 (PLAN):
- Every change must reference criterion IDs
- If iteration > 1, approach MUST differ from last attempt
- Include traceability matrix, order of operations, risks
- REQUIRES human approval before implementation

## TESTS.md Instructions

Fill during Phase 3 (TEST DESIGN):
- Each test references a criterion ID
- Tests MUST exercise production code (not duplicates)
- Mark required vs optional
- Define verifier type and threshold
- After running: fill Evidence section with command + output + exit code

## LEARNINGS.md Instructions

Append-only during any phase:
- Evidence: exact command + output
- Scope: where this applies
- Confidence: high/medium/low
- Supersedes: which previous learning this replaces (if any)

## STATUS.json Field Reference

```json
{
  "v": 3,                    // Protocol version
  "phase": "IDLE",           // Current phase
  "iter": 0,                 // Iteration number
  "blocked": false,          // Is work blocked?
  "confidence": 0,           // 0-100 confidence level
  "criteria": {              // Criterion status map
    "C1": {"s":"V","n":"description"},  // s: V=verified, F=failed, P=progress, N=not started
    "C2": {"s":"N","n":"description"}
  },
  "ts": "",                  // Last updated timestamp
  "next": ""                 // Next action description
}
```
