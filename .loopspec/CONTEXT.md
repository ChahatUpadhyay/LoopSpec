# Project Context

## Tech Stack

- **Protocol format**: Markdown (.md) + JSON (STATUS.json)
- **Setup scripts**: PowerShell (.ps1), Bash (.sh), Windows CMD (.bat)
- **CLI target for v3**: Node.js 18+ (cross-platform, npm distribution, enables `npx`)
- **Runtime available**: Python 3.11.9, PowerShell 5.1, Git 2.x
- **Package distribution plan**: npm (enables `npx loopspec init`)
- **OS**: Windows 11 (primary dev), must support macOS/Linux

## Project Structure

```
LoopSpec/
├── .loopspec/          # Protocol meta (for v3 dev itself)
├── templates/          # 10 template .md files + STATUS.json (v2)
├── examples/           # 5 example projects using v2
│   ├── oxygen-atom-sim/
│   ├── solar-system-sim/
│   ├── black-hole-sim/
│   ├── financial-forecasting-system/
│   └── limit-order-book-simulator/
├── images/             # README proof images
├── setup.ps1           # v2 PowerShell setup (184 lines)
├── setup.sh            # v2 Bash setup
├── setup.bat           # v2 CMD setup
├── README.md           # 386 lines, documents v2
├── SPEECH.md           # LinkedIn post content
├── LICENSE             # MIT
└── .gitignore
```

## Architecture Overview

v2 is a **file-based protocol** with no runtime component:
1. User clones LoopSpec repo → runs setup script → copies templates into project
2. User edits GOAL.md → tells AI "read PROTOCOL.md and begin"
3. AI reads all .loopspec/ files → executes phases → writes results back
4. State persists across sessions via filesystem

**No CLI, no daemon, no server.** Pure filesystem convention.

## Key Files & Their Roles

| File | Size | Role | Relevant to |
|------|------|------|-------------|
| templates/PROTOCOL.md | 23,960B (544 lines) | Core operating manual | C7, C8, C10, C11 |
| templates/GOAL.md | 3,281B | User criteria definition | C13 |
| templates/STATUS.json | 362B | Machine-readable state | C3, C9 |
| templates/LEARNINGS.md | 7,006B | Persistent memory | C13 |
| setup.ps1 | 7,371B | Windows init script | C1, C2, C12 |
| setup.sh | 5,852B | Unix init script | C1, C2, C12 |
| README.md | 18,398B | Documentation | C15 |

**Total template size: ~45,844 bytes (~12,000 tokens if model reads all)**

## Dependencies

- Zero runtime dependencies in v2
- Setup scripts are self-contained
- Templates are plain text

## Existing Tests

- `examples/oxygen-atom-sim/verify-static.ps1`: 35-test PowerShell verification
- No automated test suite for the protocol/CLI itself
- No CI/CD pipeline

## Baseline State

```
$ git log --oneline -3 (on Loop_Spec_v3 branch)
9f61c5e docs: Add example proof images to README
98000ea feat: Add 4 example projects, enhanced README, LinkedIn speech
3329fbd Update Three.js to v0.162.0 and fix OrbitControls import
```

v2 protocol token cost (approximate):
- PROTOCOL.md alone: ~8,000 tokens
- All templates if read at init: ~12,000 tokens
- Per-phase with all reads: ~3,000-8,000 tokens
- Full 7-phase execution: **~50,000-80,000 tokens overhead**

Setup friction: 6+ manual steps before AI starts working.

## Available Runtimes

- Python 3.11.9 ✓
- PowerShell 5.1 ✓
- Git 2.x ✓
- Node.js — to verify/install

## Patterns & Conventions

- Template comments use HTML `<!-- ... -->` (verbose)
- File naming: UPPERCASE.md for protocol files
- Duplicate state: STATUS.json + STATUS.md
- No version field in templates
- Setup scripts duplicated for 3 platforms

## v2 Gap Analysis

### Critical Gaps (High Impact):
1. **No CLI** — Manual clone + script + navigate. No `npx loopspec init`.
2. **Context bloat** — 12K tokens of templates at start, 60% is comments.
3. **No selective loading** — Protocol says "read all" regardless of phase.
4. **No git awareness** — No auto-branching, no iteration tracking.
5. **Retry guidance vague** — "materially different" without strategies.
6. **No incremental verification** — Must implement all before testing.

### Medium Gaps:
7. **Duplicate state** — STATUS.md + STATUS.json = same data twice.
8. **Template verbosity** — Instructions inflate token usage.
9. **No validation tool** — No way to check structural correctness.
10. **No progress view** — No quick status command.

### Low Gaps (Nice-to-Have):
11. **No IDE hooks** — No .cursorrules/.windsurfrules generation.
12. **No cost tracking** — No token usage measurement.
13. **No iteration archiving tool** — Convention exists but no automation.
