# LoopSpec v2 — LinkedIn Video Speech

*A developer's guide to making AI coding tools actually deliver what you ask for.*

---

## Opening (Hook — 30 seconds)

Hey developers, let me ask you something.

How many times have you asked an AI coding tool to build something — and it gets it 80% right, then you spend the next hour fixing the other 20%? Or worse — it says "done!" but the tests don't pass, the imports are wrong, and the edge cases are completely ignored?

I built something to fix that. It's called **LoopSpec** — and it's an open-source protocol that turns any AI model into a self-correcting development partner.

No framework. No library. No SaaS. Just **Markdown files**.

---

## The Problem (1 minute)

Here's what typically happens when you use AI coding tools today:

1. You describe what you want
2. The AI generates code
3. Something breaks
4. You paste the error back
5. The AI "fixes" it — sometimes creating new bugs
6. Repeat 5-10 times
7. You eventually fix it yourself

The AI has **no memory** of what it tried before. No structured plan. No tests designed upfront. No way to verify its own work. And no way to learn from its mistakes.

You're basically managing an intern who forgets everything between messages.

**LoopSpec changes that.**

---

## What is LoopSpec? (1.5 minutes)

LoopSpec is a **protocol** — a set of Markdown files that live inside your project in a `.loopspec/` directory. These files give any AI model a structured operating manual:

**Goal → Plan → Test Design → Implement → Verify → Adversarial Check → Evaluate**

And if something fails? It loops back — but with **memory**. It documents what went wrong, why, and how to avoid it next time.

### The File Structure

Here's what each file does — in plain English:

- **`PROTOCOL.md`** — The operating manual. The AI reads this first and follows it phase by phase. You never edit this.

- **`GOAL.md`** — This is the **only file you write**. You define what you want and your success criteria in a simple table. That's it.

- **`CONTEXT.md`** — The AI scans your codebase and documents what already exists before touching anything.

- **`PLAN.md`** — The AI writes a detailed plan linked to your criteria. **You approve it** before any code gets written.

- **`TESTS.md`** — Tests are designed **before** implementation. After running, evidence is recorded — actual commands, exit codes, output.

- **`LEARNINGS.md`** — This is the AI's **long-term memory**. Every mistake gets documented with root cause and a prevention rule. This is the magic — the AI reads this before every new iteration and avoids repeating the same mistakes.

- **`QUESTIONS.md`** — When the AI is uncertain, it asks here instead of guessing. Your answers become permanent decisions.

- **`STATUS.md`** / **`STATUS.json`** — Current phase, iteration count, confidence level. Human-readable and machine-readable.

- **`ADVERSARIAL_CHECK.md`** — After tests pass, the AI actively tries to **break** its own code. This catches false positives.

- **`EVALUATION_REPORT.md`** — Final report. Every criterion is marked VERIFIED only with reproducible evidence.

---

## How Easy is Onboarding? (1 minute)

Three steps. Under two minutes.

**Step 1**: Clone LoopSpec and run the setup script in your project:

```bash
git clone https://github.com/ChahatUpadhyay/LoopSpec.git
cd your-project
bash /path/to/LoopSpec/setup.sh .
```

**Step 2**: Open `GOAL.md` and fill in your objective and success criteria. Here's a real example from one of our projects:

```markdown
## Objective
Build a Limit Order Book Market Simulator with multi-agent trading.

## Success Criteria
| ID  | Criterion                              | Verifier  | Threshold              | Required |
|-----|----------------------------------------|-----------|------------------------|----------|
| C1  | Matching engine has price-time priority | automated | Orders matched correctly | yes      |
| C2  | Market maker maintains spread           | automated | Orders on both sides    | yes      |
| C3  | Performance handles 1M+ orders          | metric    | >10,000 orders/sec      | yes      |
```

That's it. You define **what** success looks like. The AI figures out **how**.

**Step 3**: Tell your AI model:

> "Read `.loopspec/PROTOCOL.md` and begin."

Works with Claude, GPT, Gemini, Cursor, Windsurf, Aider — any model that can read files.

---

## The Learning System in Action (1.5 minutes)

Let me show you the most powerful part — `LEARNINGS.md`.

In our Limit Order Book Simulator project, the AI hit this error during implementation:

```
ImportError: attempted relative import beyond top-level package
```

It fixed it by switching to absolute imports. But here's what matters — it **documented the learning**:

```markdown
## Learning L1 — Iteration 1 — Phase: IMPLEMENT

### What Went Wrong
Relative imports failed when running scripts from the scripts/ directory.

### Root Cause
The project uses src/ as a package, but scripts run outside the package context.

### Prevention Rule
Use absolute imports when scripts run outside the package context.
```

Later in the same project, when building the visualization server, the AI needed to add new modules. Because it had already documented L1, it used absolute imports from the start — **zero retry, zero wasted time**.

Without LoopSpec? The AI would have made the same mistake again. And again. Because it has no memory between sessions.

With LoopSpec? Every mistake becomes a **permanent lesson**.

---

## Real Results (30 seconds)

We've built **5 complete projects** with LoopSpec v2:

1. **Oxygen Atom Simulation** — 3D quantum orbital visualization (10 criteria)
2. **Black Hole Simulation** — Cinematic gravitational lensing (20+ criteria)
3. **Solar System Simulator** — Kepler orbital mechanics (25+ criteria)
4. **Financial Forecasting System** — ML pipeline with 4 models (35+ criteria)
5. **Limit Order Book Simulator** — NASDAQ-style trading engine (37 criteria)

Each one has a full `.loopspec/` directory you can browse on GitHub to see exactly how the AI planned, implemented, tested, and learned.

---

## Call to Action (30 seconds)

LoopSpec is **open source**, **MIT licensed**, and works with **any AI model**.

Here's what I'm asking:

- **Try it** on your next medium-to-large AI coding task
- **Star the repo** if it saves you time
- **Contribute** — add examples, improve the protocol, fix edge cases
- **Share your results** — I'd love to see what you build with it

The repo is at: **github.com/ChahatUpadhyay/LoopSpec** — branch `Loop_Spec_v2`.

---

## Benefits Summary

- **Zero dependencies** — Just Markdown files. No install, no npm, no pip, no binary.
- **Model-agnostic** — Works with Claude, GPT, Gemini, Cursor, Windsurf, Aider, or any model that reads files.
- **Self-correcting** — AI learns from mistakes and avoids repeating them via `LEARNINGS.md`.
- **Evidence-driven** — No criterion is "met" without executable, reproducible evidence (command + exit code + output).
- **Anti-cheating** — AI cannot weaken tests, lower thresholds, or test duplicate code instead of production code.
- **Human-in-the-loop** — Plan requires your approval. Safety gates for destructive operations. Questions asked, not assumed.
- **Adversarial self-check** — After tests pass, AI actively tries to break its own implementation.
- **Persistent memory** — Learnings survive across sessions. The AI reads them before every new iteration.
- **Portable** — `.loopspec/` directory lives in your project repo. Version-controlled. Shareable. Auditable.
- **Open source** — MIT licensed. Fork it, adapt it, make it yours.
- **2-minute onboarding** — Clone, run setup, write GOAL.md, tell the AI to begin.

---

*LoopSpec v2 — Stop managing AI. Start engineering with it.*
