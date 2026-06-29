<p align="center">
  <h1 align="center">🔁 LoopSpec</h1>
  <p align="center">
    <strong>A model-agnostic, self-correcting AI development protocol.</strong><br/>
    Stop hoping your AI gets it right. Start <em>engineering</em> it to.
  </p>
  <p align="center">
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
    <a href="https://github.com/loopspec/loopspec"><img src="https://img.shields.io/badge/protocol-v1.0-green.svg" alt="Protocol v1.0"></a>
    <a href="https://github.com/loopspec/loopspec/stargazers"><img src="https://img.shields.io/github/stars/loopspec/loopspec?style=social" alt="GitHub Stars"></a>
  </p>
</p>

---

## Why LoopSpec?

AI coding tools are powerful — but unreliable. They hallucinate APIs, skip edge cases, and silently break things. **LoopSpec fixes this** by giving every AI model a structured operating manual: analyze first, plan before coding, write tests before implementation, and self-correct when things fail.

It's not a framework. It's not a library. It's a **protocol** — a set of markdown files that any AI model can read and follow, regardless of which tool you use.

| Without LoopSpec | With LoopSpec |
|---|---|
| "Make this feature" → 🤞 hope it works | "Make this feature" → structured 6-phase execution |
| AI invents nonexistent APIs | AI analyzes the codebase first |
| One-shot attempt, no retry logic | Self-correcting retry loop (up to 10 iterations, configurable) |
| No memory across sessions | Persistent learnings file prevents repeat mistakes |
| Works with one specific tool | Works with Claude Code, Cursor, Windsurf, ChatGPT, Gemini, Aider… |

---

## Quick Start

### 1. Initialize

```bash
# Clone LoopSpec
git clone https://github.com/loopspec/loopspec.git
cd your-project

# Run the bootstrap script
# macOS / Linux
bash /path/to/loopspec/setup.sh .

# Windows (CMD)
\path\to\loopspec\setup.bat .

# Windows (PowerShell)
powershell -ExecutionPolicy Bypass -File \path\to\loopspec\setup.ps1 -TargetDir .
```

### 2. Define Your Goal

Open `.loopspec/GOAL.md` and fill in:
- **What** you want built (be specific)
- **Success criteria** (how you'll know it's done)
- **Permissions** (what the AI may and may not touch)

### 3. Start Your AI

Open the project in your AI coding tool and say:

> **"Read `.loopspec/PROTOCOL.md` and begin."**

That's it. The AI will follow the protocol from there.

---

## File Reference

LoopSpec creates a `.loopspec/` directory in your project with these files:

| File | Purpose | Who Writes It |
|---|---|---|
| `PROTOCOL.md` | Complete AI operating manual — read-only instructions | LoopSpec (you don't edit this) |
| `GOAL.md` | Objective, success criteria, permissions, constraints | **Human** |
| `CONTEXT.md` | Project analysis — tech stack, architecture, patterns | AI (Phase 1) |
| `PLAN.md` | Step-by-step implementation plan | AI (Phase 2) → **Human approves** |
| `TESTS.md` | Test cases derived from success criteria | AI (Phase 3) |
| `CHANGELOG.md` | Log of all changes made and reasoning | AI (ongoing) |
| `LEARNINGS.md` | Self-corrective memory — mistakes and fixes | AI (ongoing) |
| `QUESTIONS.md` | Clarification requests from AI to human | AI asks → **Human answers** |
| `STATUS.md` | Current phase, iteration count, blockers | AI (ongoing) |
| `iterations/` | Per-iteration snapshots for audit trail | AI (each cycle) |

Additionally, an `AGENTS.md` file is generated at your **project root** for compatibility with tools that support `AGENTS.md` auto-discovery (e.g., Gemini CLI, Claude Code).

---

## The Six Phases

LoopSpec follows a strict phase sequence. The AI may not skip phases.

```
┌──────────┐     ┌──────┐     ┌────────────┐     ┌───────────┐     ┌────────┐     ┌──────────┐
│ ANALYZE  │────▸│ PLAN │────▸│ TEST DESIGN│────▸│ IMPLEMENT │────▸│ VERIFY │────▸│ EVALUATE │
│ Phase 1  │     │ Ph 2 │     │  Phase 3   │     │  Phase 4  │     │ Ph 5   │     │ Phase 6  │
└──────────┘     └──┬───┘     └────────────┘     └───────────┘     └────────┘     └─────┬────┘
                    │                                                                    │
                    │                          ◂── retry loop (max 3) ──────────────────┘
                    ▾
             Human Approval
              (required)
```

### Phase 1 — ANALYZE

The AI reads the codebase, identifies the tech stack, understands the architecture, maps dependencies, and writes its findings to `CONTEXT.md`. No code changes happen here.

### Phase 2 — PLAN

Based on the analysis, the AI writes a detailed implementation plan in `PLAN.md`. **The human must approve this plan** before the AI proceeds. This is the critical checkpoint.

### Phase 3 — TEST DESIGN

The AI writes test cases in `TESTS.md` derived directly from the success criteria in `GOAL.md`. Tests are designed *before* implementation (test-driven development).

### Phase 4 — IMPLEMENT

The AI executes the approved plan, writing code and logging every change in `CHANGELOG.md`. If it encounters surprises, it records them in `LEARNINGS.md`.

### Phase 5 — VERIFY

The AI runs all tests from `TESTS.md`. If tests fail, it documents the root cause in `LEARNINGS.md`, fixes the issue, and retries. It also performs a self-check: "Are my tests sufficient?" — adding more if needed.

### Phase 6 — EVALUATE

The AI checks each success criterion against the implementation. If all pass → done. If any fail, the AI records *why* in `LEARNINGS.md` and loops back to Phase 2 with new knowledge. Default maximum of 10 iterations (configurable in `GOAL.md`) prevents infinite loops.

---

## Model-Specific Tips

LoopSpec works with any AI model. Here's how to get the best results with each tool:

### Claude Code

```
claude "Read .loopspec/PROTOCOL.md and begin."
```

- Claude Code has native `AGENTS.md` support — it will auto-discover the protocol
- Excels at following multi-step instructions faithfully
- Set `CLAUDE.md` to point to LoopSpec if you already have one:
  ```
  Read and follow .loopspec/PROTOCOL.md for all development tasks.
  ```

### ChatGPT / Codex (CLI)

```
codex "Read .loopspec/PROTOCOL.md and follow the LoopSpec protocol."
```

- Upload `.loopspec/PROTOCOL.md` and `.loopspec/GOAL.md` at the start of a session
- GPT-4o and o3 both follow the phase structure well
- For Codex CLI, the `AGENTS.md` file at the root will be auto-discovered

### Cursor

- Open the project in Cursor, then in Composer:
  ```
  @.loopspec/PROTOCOL.md Read this protocol and begin.
  ```
- Add a `.cursorrules` file pointing to LoopSpec:
  ```
  Read and follow .loopspec/PROTOCOL.md for all development tasks.
  ```
- Use **Agent Mode** (not Ask) for best results — the AI needs tool access

### Windsurf

- In Cascade:
  ```
  Read .loopspec/PROTOCOL.md and follow the LoopSpec protocol to achieve the goal in GOAL.md
  ```
- Add `.windsurfrules` pointing to the protocol for persistence across sessions
- Windsurf's file-editing flow works naturally with LoopSpec's phase structure

### Gemini (CLI / AI Studio)

```
gemini "Read .loopspec/PROTOCOL.md and begin."
```

- Gemini CLI auto-discovers `AGENTS.md` at the project root
- For AI Studio, paste `PROTOCOL.md` and `GOAL.md` into the system prompt
- Works well with large codebases thanks to the long context window

### Aider

```bash
aider --message "Read .loopspec/PROTOCOL.md and follow the LoopSpec protocol."
```

- Add the protocol to Aider's conventions:
  ```yaml
  # .aider.conf.yml
  conventions:
    - .loopspec/PROTOCOL.md
  ```
- Aider's git-based workflow complements LoopSpec's changelog tracking
- Use `--auto-commits` to get per-phase git history

---

## FAQ

### Is this just prompt engineering?

No. LoopSpec is a *protocol* — a structured system of files that persist across sessions, accumulate learnings, and enforce a development workflow. Prompt engineering is one-shot; LoopSpec is a feedback loop.

### Does this work with local/open-source models?

Yes. Any model that can read markdown files and follow instructions can use LoopSpec. The protocol is intentionally simple — no special APIs, no dependencies, just markdown.

### What if the AI ignores the protocol?

This happens less than you'd think — modern models are quite good at following structured instructions. But if it does, just restart the session and explicitly say: *"You MUST follow each phase in PROTOCOL.md. Do not skip any phase."*

### Can I customize the protocol?

Absolutely. `PROTOCOL.md` is just a markdown file. Fork LoopSpec and adapt the phases, add your own conventions, change the retry limit — it's your protocol.

### How is this different from AGENTS.md / CLAUDE.md / .cursorrules?

Those are single-file instruction sets. LoopSpec is a **multi-file system** with separation of concerns: goals, plans, tests, learnings, and status are all separate files that the AI reads and writes. The auto-generated `AGENTS.md` simply points to the LoopSpec protocol.

### Does this add overhead to small tasks?

For a one-liner fix, you probably don't need LoopSpec. It shines on tasks that are medium-to-large: features, refactors, migrations, new modules — anything where "just do it" leads to broken code and multiple rounds of back-and-forth.

### What's in the `iterations/` directory?

Each retry cycle (when verification fails and the AI loops back) creates a snapshot in `iterations/` so you have a full audit trail of what was tried and why it failed.

---

## Proof: LoopSpec in Action

We dogfooded LoopSpec to build a **premium sorting algorithm visualizer** — a complex single-page web app with 12 stringent success criteria. Here are the real results:

### The Challenge

Build a fully interactive sorting visualizer with:
- 4 algorithms (Bubble, Quick, Merge, Insertion) with real-time animation
- Step-by-step mode, algorithm comparison mode (side-by-side)
- Statistics dashboard (comparisons, swaps, time, Big-O)
- Dark glassmorphism UI, responsive design (1920px → 375px)
- Automated correctness tests for all algorithms

### The Results

| Metric | Result |
|--------|--------|
| **Total phases completed** | 6 of 6 ✅ |
| **Iterations needed** | 1 (goal achieved first try) |
| **Self-corrections made** | 1 (auto-detected Node.js missing, switched to cscript.exe) |
| **Tests designed** | 15 (covering all 12 criteria) |
| **Tests passed** | 15/15 ✅ |
| **Success criteria met** | 12/12 ✅ |
| **Learnings documented** | 1 (with root cause + prevention rule) |
| **Code produced** | ~1,728 lines across 7 files |
| **Files documented** | 9 `.loopspec/` files updated throughout |

### Self-Correction in Action

During Phase 5 (VERIFY), the model attempted `node test-node.js` — but Node.js wasn't installed. Instead of failing, it:

1. **Documented** the error in `LEARNINGS.md` with root cause analysis
2. **Created** a fallback test script using Windows' built-in `cscript.exe`
3. **Ran** the fallback — all 36 sorting tests passed
4. **Wrote a prevention rule**: _"Always check for available runtimes before assuming Node.js"_

This is the LoopSpec difference. Without the protocol, the AI would have reported "tests can't run" and stopped. With LoopSpec, it self-corrected and continued.

### Why LoopSpec Beats Unstructured AI Coding

| Approach | Self-Correcting | Test-First | Persistent Memory | Audit Trail | Works Across Tools |
|----------|:-:|:-:|:-:|:-:|:-:|
| Just prompting | ❌ | ❌ | ❌ | ❌ | ❌ |
| `.cursorrules` / `CLAUDE.md` | ❌ | ❌ | ❌ | ❌ | ❌ |
| `AGENTS.md` | ❌ | ❌ | ❌ | ❌ | ✅ |
| OpenSpec | ❌ | ❌ | ❌ | Partial | ✅ |
| BMAD Method | ❌ | ❌ | ❌ | ✅ | Partial |
| **LoopSpec** | **✅** | **✅** | **✅** | **✅** | **✅** |

> **Key insight**: The `LEARNINGS.md` file is what makes LoopSpec fundamentally different. It gives AI models _persistent memory across iterations_ — they never repeat the same mistake twice.

See the full dogfood test results in the [`examples/sorting-visualizer/`](examples/sorting-visualizer/) directory.

---

## Contributing

We welcome contributions! See the repo for guidelines:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

Use LoopSpec to build LoopSpec. 🔁

---

## License

[MIT](LICENSE) — © 2024-present LoopSpec Contributors

