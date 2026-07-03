# LoopSpec v2

**A model-agnostic, self-correcting, evidence-driven AI development protocol.**

Stop hoping your AI gets it right. Start *engineering* it to — with verifiable evidence at every step.

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Protocol v2.0](https://img.shields.io/badge/protocol-v2.0-green.svg)](https://github.com/ChahatUpadhyay/LoopSpec)
[![Made for AI](https://img.shields.io/badge/made%20for-AI%20coding%20tools-purple.svg)](#model-specific-integration)
[![Examples](https://img.shields.io/badge/examples-5%20projects-orange.svg)](#examples)

---

## What is LoopSpec?

LoopSpec is a **protocol** — a set of markdown files that give any AI model a structured operating manual for development tasks. It's not a framework, not a library, not a SaaS product. It's a portable workflow contract that works across any IDE and any AI model.

**The core idea**: Goal → Plan → Test → Implement → Verify → Learn → Repeat until done.

**What makes v2 different from v1**: Evidence-gated verification, adversarial checking, anti-cheating rules, memory hygiene, safety gates, and honest acknowledgment of what a Markdown protocol can and cannot do.

> **TL;DR for developers**: You write `GOAL.md` (what you want + success criteria). The AI does the rest — plans, implements, tests, learns from mistakes, and retries until every criterion has verifiable evidence.

### What LoopSpec IS:
- A structured set of files that persist across AI sessions
- A workflow contract any capable model can follow
- A portable standard (works with Claude, GPT, Gemini, Cursor, Windsurf, Aider, etc.)
- A self-correcting feedback loop with persistent memory

### What LoopSpec is NOT:
- An execution engine (it cannot run commands or keep processes alive)
- A guarantee that your AI will follow it (it relies on model compliance)
- A replacement for good engineering judgment
- Necessary for simple one-liner fixes

---

## Quick Start (< 2 minutes)

### Option 1: Clone and Initialize

```bash
# Clone LoopSpec
git clone https://github.com/ChahatUpadhyay/LoopSpec.git

# Navigate to YOUR project
cd your-project

# Initialize LoopSpec in your project
# macOS / Linux
bash /path/to/LoopSpec/setup.sh .

# Windows (PowerShell)
powershell -ExecutionPolicy Bypass -File \path\to\LoopSpec\setup.ps1 -TargetDir .

# Windows (CMD)
\path\to\LoopSpec\setup.bat .
```

### Option 2: Manual Setup (Zero Dependencies)

```bash
# Create the directory
mkdir -p .loopspec/iterations

# Copy the template files from this repo's templates/ folder into .loopspec/
# That's it. No install, no npm, no pip, no binary.
```

### Then:

1. **Edit** `.loopspec/GOAL.md` — define what you want, with criterion IDs (C1, C2, ...)
2. **Open** your project in any AI coding tool
3. **Tell the AI**: `"Read .loopspec/PROTOCOL.md and begin."`

Done. The AI handles the rest.

---

## How It Works

### The Seven Phases

```
ANALYZE → PLAN → TEST DESIGN → IMPLEMENT → VERIFY → ADVERSARIAL CHECK → EVALUATE
                   ↑                                                         |
                   └──────────── retry (materially different) ───────────────┘
```

| Phase | What Happens | Key Rule |
|-------|-------------|----------|
| **1. ANALYZE** | AI scans codebase, establishes baseline | Must document current state with evidence |
| **2. PLAN** | AI writes implementation plan | **Human must approve** before proceeding |
| **3. TEST DESIGN** | AI designs tests linked to criteria | Tests must exercise production code, not copies |
| **4. IMPLEMENT** | AI executes the approved plan | Safety gates for destructive/costly actions |
| **5. VERIFY** | AI runs tests, records evidence | Every result needs command + output + exit code |
| **6. ADVERSARIAL** | AI tries to disprove its own success | Must attempt to break each criterion |
| **7. EVALUATE** | Final evidence-gated pass/fail | Criterion is VERIFIED only with current evidence |

### What's New in v2

| Feature | v1 | v2 |
|---------|----|----|
| Criterion IDs | No | C1, C2, ... with verifier + threshold |
| Evidence requirement | "Tests pass" | Command + output + exit code + location |
| Adversarial checking | No | Mandatory attempt to disprove success |
| Anti-cheating rules | No | Cannot weaken tests, replace verifiers, or test copies |
| Memory hygiene | Append anything | Evidence, scope, confidence, supersession |
| Safety gates | Basic permissions | Destructive/irreversible/costly/secret-bearing gates |
| State model | Free-form | Strict state machine with WAITING_HUMAN, BLOCKED |
| Installer | Overwrites AGENTS.md | Non-destructive append, --repair mode |
| Honest limitations | Claims autonomy | Explicitly states what Markdown cannot do |
| Machine-readable state | STATUS.md only | STATUS.json for tooling integration |

---

## File Reference

LoopSpec creates a `.loopspec/` directory in your project:

| File | Purpose | Who Writes It |
|------|---------|---------------|
| `PROTOCOL.md` | Complete operating manual (read-only) | LoopSpec |
| `GOAL.md` | Objective, criteria (with IDs), permissions | **Human** |
| `CONTEXT.md` | Project analysis + baseline state | AI (Phase 1) |
| `PLAN.md` | Implementation plan with traceability | AI (Phase 2) → **Human approves** |
| `TESTS.md` | Tests with criterion IDs + evidence fields | AI (Phase 3+) |
| `CHANGELOG.md` | Append-only change log with rationale | AI (ongoing) |
| `LEARNINGS.md` | Evidence-backed memory with scope/confidence | AI (ongoing) |
| `QUESTIONS.md` | Human-in-the-loop questions + decisions log | AI asks → **Human answers** |
| `STATUS.md` | Human-readable execution state | AI (ongoing) |
| `STATUS.json` | Machine-readable state for tooling | AI (ongoing) |
| `iterations/` | Per-iteration archive snapshots | AI (each cycle) |

Plus `AGENTS.md` at project root for tools that auto-discover it (Claude Code, Gemini CLI, Codex).

---

## Model-Specific Integration

LoopSpec works with **any model that can read files and follow instructions**.

### Claude Code / Claude CLI
```bash
claude "Read .loopspec/PROTOCOL.md and begin."
```
- Auto-discovers `AGENTS.md` at project root
- Add to `CLAUDE.md`: `Read and follow .loopspec/PROTOCOL.md for all tasks.`

### OpenAI Codex CLI
```bash
codex "Read .loopspec/PROTOCOL.md and follow the LoopSpec protocol."
```
- `AGENTS.md` auto-discovery supported
- Works with o3, o4-mini, GPT-4o

### Cursor
```
@.loopspec/PROTOCOL.md Read this protocol and begin.
```
- Add `.cursorrules`: `Read and follow .loopspec/PROTOCOL.md for all development tasks.`
- Use **Agent Mode** (not Ask) — the AI needs tool access

### Windsurf (Cascade)
```
Read .loopspec/PROTOCOL.md and follow the LoopSpec protocol to achieve the goal in GOAL.md
```
- Add `.windsurfrules` pointing to the protocol

### Gemini CLI / AI Studio
```bash
gemini "Read .loopspec/PROTOCOL.md and begin."
```
- Auto-discovers `AGENTS.md`
- Long context window handles full protocol well

### Aider
```bash
aider --message "Read .loopspec/PROTOCOL.md and follow the LoopSpec protocol."
```
- Add to `.aider.conf.yml`: `read: [.loopspec/PROTOCOL.md]`
- Use `--auto-commits` for per-phase git history

### Any Other Model
Just paste the contents of `PROTOCOL.md` and `GOAL.md` into the system prompt or first message. LoopSpec is plain Markdown — it works anywhere.

---

## Key Design Principles

### 1. Evidence Over Claims
No criterion is "met" without executable, reproducible evidence. "Tests pass" means showing the command, exit code, and output — not just saying it.

### 2. Anti-Cheating
The AI cannot weaken tests, lower thresholds, replace automated verifiers with "manual review", or test duplicate implementations instead of production code. These are the most common ways AI models inadvertently game their own success criteria.

### 3. Memory Hygiene
Learnings are powerful but can poison future work. Every learning requires evidence, scope, confidence level, and supersession tracking. Broad cargo-cult rules without evidence are rejected.

### 4. Materially Different Retries
When something fails and the AI retries, it must use a *materially different* approach. Repeating the same failing code/logic is explicitly forbidden.

### 5. Adversarial Self-Check
After tests pass, the AI must actively try to disprove its own success. This catches false positives, weak assertions, and tests that pass for the wrong reasons.

### 6. Safety Gates
Destructive, irreversible, costly, external, and secret-bearing operations require explicit permission. The protocol stops and asks rather than assuming.

### 7. Human Checkpoint
The plan requires human approval. This is non-negotiable. It prevents AI overbuilding, wrong assumptions, and architecture drift.

---

## Upgrading from v1

```bash
# If you already have .loopspec/ from v1:
bash /path/to/LoopSpec/setup.sh . --repair

# Or PowerShell:
.\setup.ps1 -TargetDir . -Repair
```

This updates `PROTOCOL.md` and adds `STATUS.json` without overwriting your existing GOAL, LEARNINGS, or other data files.

### Key differences to be aware of:
- **GOAL.md** now expects criterion IDs (C1, C2, ...) with verifier and threshold columns
- **TESTS.md** now requires evidence fields and criterion references
- **LEARNINGS.md** now requires scope, confidence, and evidence per entry
- **New phase**: Adversarial Check (Phase 6) between Verify and Evaluate
- **New file**: `STATUS.json` for machine-readable state

---

## FAQ

### Is this just prompt engineering?
No. Prompt engineering is one-shot. LoopSpec is a persistent multi-file system that accumulates state, memory, and evidence across sessions. It's a *workflow contract*, not a prompt.

### Does this work with local/open-source models?
Yes. Any model that can read markdown and follow instructions. No APIs, no dependencies, just files.

### What if the AI ignores the protocol?
Modern models rarely do when given clear structured instructions. If it happens: restart and say "You MUST follow each phase in PROTOCOL.md. Do not skip any phase." The protocol also self-reinforces through cross-references between files.

### Can I customize the protocol?
Absolutely. Fork and adapt. Change phases, add conventions, adjust retry limits. It's your protocol.

### Does this add overhead to small tasks?
Yes. Don't use LoopSpec for one-liner fixes. Use it for medium-to-large tasks where "just do it" leads to broken code and 5 rounds of "that's still not right."

### How is this different from AGENTS.md / CLAUDE.md?
Those are single instruction files. LoopSpec is a multi-file system with separation of concerns: goal, plan, tests, memory, status, and questions are all separate, persistent, and cross-referenced.

### Can the protocol actually enforce anything?
No. A Markdown file cannot force a model to comply. But it provides clear enough structure that compliant models follow it reliably, and humans can audit compliance by reading the `.loopspec/` files. Think of it like a legal contract — it works because parties agree to follow it, not because it physically prevents violations.

---

## Examples

The `examples/` directory contains **5 complete projects** built using LoopSpec v2 — each with full `.loopspec/` directories showing the protocol in action.

| Example | Description | Tech Stack | Criteria | Key Learnings |
|---------|------------|------------|----------|---------------|
| **[Oxygen Atom Sim](examples/oxygen-atom-sim/)** | 3D quantum orbital visualization of oxygen atom | Three.js, WebGL | 10 criteria | Orbital physics accuracy, shader rendering |
| **[Black Hole Sim](examples/black-hole-sim/)** | Cinematic black hole with gravitational lensing & accretion disk | Three.js, GLSL shaders | 20+ criteria | CDN version management, shader effects |
| **[Solar System Sim](examples/solar-system-sim/)** | Interactive 3D solar system with Kepler orbital mechanics | Three.js, WebGL | 25+ criteria | Kepler's laws, planet scale ratios |
| **[Financial Forecasting](examples/financial-forecasting-system/)** | Production ML pipeline with ARIMA, XGBoost, LSTM, Transformer | Python, PyTorch, FastAPI, Docker | 35+ criteria | Model registry, data pipeline, CI/CD |
| **[Limit Order Book](examples/limit-order-book-simulator/)** | NASDAQ-style matching engine with multi-agent trading simulation | Python, Flask | 37 criteria | Import structure, agent API design, PnL tracking |

### What to look at in each example:

- **`GOAL.md`** — The human-written objective with success criteria table
- **`PLAN.md`** — AI-generated implementation plan (linked to criteria)
- **`TESTS.md`** — Test cases with evidence (command + output + exit code)
- **`LEARNINGS.md`** — Mistakes the AI made and how it avoided repeating them
- **`EVALUATION_REPORT.md`** — Final pass/fail assessment with evidence

> Browse any example's `.loopspec/LEARNINGS.md` to see how the protocol's memory system prevents repeated mistakes across iterations.

---

## The `.loopspec/` File Structure — Quick Reference

Every LoopSpec project gets a `.loopspec/` directory with these files:

| File | Who Writes | Purpose |
|------|-----------|---------|
| **`PROTOCOL.md`** | LoopSpec (read-only) | The complete operating manual. The AI reads this first and follows the seven phases. Never edit this manually. |
| **`GOAL.md`** | **You (Human)** | Your objective + success criteria table (C1, C2...) with verifier types and thresholds. This is the ONLY file you need to write. |
| **`CONTEXT.md`** | AI (Phase 1) | AI scans your codebase and documents the current state, tech stack, dependencies, and baseline before changing anything. |
| **`PLAN.md`** | AI (Phase 2) → **You approve** | AI writes a detailed implementation plan linked to your criteria. You must approve before it starts coding. |
| **`TESTS.md`** | AI (Phase 3+) | Test cases designed before implementation, with evidence fields filled after execution (command, exit code, output). |
| **`LEARNINGS.md`** | AI (ongoing) | The AI's long-term memory. Every mistake gets documented with root cause, evidence, and a prevention rule for future iterations. |
| **`CHANGELOG.md`** | AI (ongoing) | Append-only log of every change made, with rationale and linked criteria. |
| **`QUESTIONS.md`** | AI asks → **You answer** | When the AI is uncertain, it asks here instead of guessing. Your answers become permanent decisions. |
| **`STATUS.md`** | AI (ongoing) | Human-readable current phase, iteration, confidence level, and next action. |
| **`STATUS.json`** | AI (ongoing) | Machine-readable version of status for tooling integration. |
| **`ADVERSARIAL_CHECK.md`** | AI (Phase 6) | AI actively tries to break its own implementation. Documents what it tried and what survived. |
| **`EVALUATION_REPORT.md`** | AI (Phase 7) | Final evidence-gated report. Each criterion marked VERIFIED only with reproducible evidence. |

---

## Project Structure

```
LoopSpec/
├── templates/               # Template files copied to .loopspec/
│   ├── PROTOCOL.md          # The operating manual (v2)
│   ├── GOAL.md              # Goal template with criterion IDs
│   ├── CONTEXT.md           # Context template with baseline
│   ├── PLAN.md              # Plan template with traceability
│   ├── TESTS.md             # Tests template with evidence fields
│   ├── LEARNINGS.md         # Memory template with hygiene rules
│   ├── QUESTIONS.md         # Questions template with decisions log
│   ├── CHANGELOG.md         # Changelog template
│   ├── STATUS.md            # Human-readable status
│   └── STATUS.json          # Machine-readable status
├── examples/                # 5 complete protocol-driven projects
│   ├── oxygen-atom-sim/     # 3D quantum orbital visualization
│   ├── black-hole-sim/      # Cinematic black hole simulation
│   ├── solar-system-sim/    # Interactive solar system
│   ├── financial-forecasting-system/  # ML pipeline
│   └── limit-order-book-simulator/    # Trading engine
├── setup.sh                 # Unix/macOS bootstrap
├── setup.ps1                # PowerShell bootstrap (PS 5.1+)
├── setup.bat                # Windows CMD bootstrap
├── LICENSE                  # MIT
└── README.md                # This file
```

---

## Contributing

We welcome contributions! Here's how:

1. **Fork** the repository
2. **Create** a feature branch
3. **Submit** a pull request

### Ways to contribute:
- **Add examples** — Build something with LoopSpec and submit it with full `.loopspec/` directory
- **Improve the protocol** — Fix edge cases, add rigor, improve cross-model compatibility
- **Fix installer issues** — Edge cases on different OS/shell combinations
- **Documentation** — Better guides, tutorials, video walkthroughs
- **Tooling** — Build integrations that read `STATUS.json` for dashboards/CI

---

## License

[MIT](LICENSE) - 2024-present LoopSpec Contributors

