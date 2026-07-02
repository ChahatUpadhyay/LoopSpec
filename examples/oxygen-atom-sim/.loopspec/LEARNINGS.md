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

## Learning L1 — Iteration 1 — Phase: ADVERSARIAL_CHECK

### What Went Wrong
Used Three.js r160 CDN URL with `examples/js/controls/OrbitControls.js` path. This file does NOT exist in r160 — Three.js removed the `examples/js/` (global script) directory starting at r150, keeping only `examples/jsm/` (ES modules).

### Root Cause
Knowledge of Three.js version history was outdated. The global-script version of OrbitControls only exists up to r149.

### Evidence
Three.js changelog r150: "Removed examples/js directory. Use ES modules from examples/jsm/ instead."
The URL `https://unpkg.com/three@0.160.0/examples/js/controls/OrbitControls.js` would 404.

### Fix Applied
Changed CDN to `https://cdn.jsdelivr.net/npm/three@0.149.0/build/three.min.js` and matching OrbitControls URL. r149 is the last version with global script support.

### Prevention Rule
When using Three.js with global `<script>` tags (not ES modules), use r149 or earlier. For r150+, you MUST use ES modules with `import` statements and importmap.

### Metadata
- **Scope**: Three.js / CDN / browser projects without bundlers
- **Confidence**: high
- **Date**: 2025-07-02
- **Supersedes**: none

---
