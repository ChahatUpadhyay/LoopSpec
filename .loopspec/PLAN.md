# Implementation Plan

## Iteration: 1
## Status: APPROVED

## Summary

Build a Python-based CLI tool (`loopspec`) that replaces the platform-specific setup scripts, adds `init/status/validate/report` commands with git integration, and rewrite the protocol templates to be context-efficient (compact mode, phase-specific loading, deferred expansion). The CLI is zero-dependency (stdlib only) for maximum portability.

## Learnings Applied

First iteration — no prior learnings in LEARNINGS.md.

External learning from v2 testing: Three.js CDN version mismatch taught us to always verify external dependency URLs exist before committing. Applied here: CLI will validate template file existence during init.

## Changes Required

### 1. CLI Tool (`cli/`)

#### File: `cli/loopspec.py` — CREATE
- **What**: Single-file Python CLI with argparse. Commands: init, status, validate, report, git-sync
- **Why**: Replaces 3 platform-specific scripts with 1 cross-platform tool
- **Criteria**: C1, C2, C12

#### File: `cli/__init__.py` — CREATE
- **What**: Package init
- **Criteria**: C1, C12

#### File: `cli/__main__.py` — CREATE
- **What**: Entry point for `python -m loopspec`
- **Criteria**: C1, C12

#### File: `pyproject.toml` — CREATE
- **What**: Python package config with `[project.scripts]` entry point
- **Why**: Enables `pip install .` and `pipx run loopspec`
- **Criteria**: C12

### 2. CLI Commands Implementation

#### `init` command (in loopspec.py)
- **What**: Create .loopspec/ dir, copy v3 templates, detect git, create AGENTS.md
- **Criteria**: C1, C2, C6

#### `status` command (in loopspec.py)
- **What**: Parse STATUS.json, display phase, iteration, criteria progress with colors
- **Criteria**: C3, C9

#### `validate` command (in loopspec.py)
- **What**: Check all .loopspec/ files exist, have required sections, criterion IDs are consistent across files
- **Criteria**: C4, C14

#### `report` command (in loopspec.py)
- **What**: Generate markdown summary from STATUS.json + TESTS.md + GOAL.md
- **Criteria**: C5

#### `git-sync` command (in loopspec.py)
- **What**: Auto-detect git, propose branch names, generate commit messages with criterion IDs
- **Criteria**: C6

### 3. Protocol v3 Templates

#### File: `templates/PROTOCOL.md` — MODIFY
- **What**: Add "Compact Mode" section (<2000 tokens), phase-specific loading guide, incremental verification rules, smart retry strategies
- **Criteria**: C7, C8, C10, C11

#### File: `templates/STATUS.json` — MODIFY
- **What**: Compressed format (<500 bytes for 10 criteria) using short keys
- **Criteria**: C9

#### File: `templates/*.md` (all) — MODIFY
- **What**: Create "slim" versions with deferred expansion (comments in separate INSTRUCTIONS.md)
- **Criteria**: C13

### 4. Documentation

#### File: `README.md` — MODIFY
- **What**: Update for v3 — CLI usage, new features, migration guide
- **Criteria**: C15

## Traceability Matrix

| Criterion | Planned Changes | Test Strategy |
|-----------|----------------|---------------|
| C1 | cli/loopspec.py (4 commands) | Run each command, check exit 0 + output |
| C2 | init command | Time execution + verify file creation |
| C3 | status command | Feed sample STATUS.json, check output format |
| C4 | validate command | Run on valid + invalid projects, check detection |
| C5 | report command | Check output contains required sections |
| C6 | git-sync command + git detection | Run in git repo, check branch/tag output |
| C7 | PROTOCOL.md compact section | Word count / 0.75 < 2000 |
| C8 | PROTOCOL.md phase loading guide | Manual check: each phase has file list |
| C9 | STATUS.json compressed format | Measure bytes of sample with 10 criteria |
| C10 | PROTOCOL.md incremental verify section | Manual: text supports partial verification |
| C11 | PROTOCOL.md retry strategies | Manual: 3+ named strategies exist |
| C12 | pyproject.toml + __main__.py | pip install + run `loopspec --help` |
| C13 | Slim templates | Byte size comparison vs v2 |
| C14 | validate on v2 example | Run validate on oxygen-atom-sim/.loopspec |
| C15 | README.md | Manual: each feature has example |

## Order of Operations

1. Create CLI package structure (pyproject.toml, __main__.py, __init__.py)
2. Implement `loopspec init` command with v3 templates
3. Create v3 templates (slim versions) — PROTOCOL.md with compact mode + phase loading
4. Implement `loopspec status` and `loopspec validate` commands
5. Implement `loopspec report` and `loopspec git-sync` commands
6. Add compressed STATUS.json format
7. Update README.md for v3
8. Run automated tests on all commands
9. Verify backward compatibility with v2 examples

## Risks & Mitigations

- **Risk**: Python not installed on some systems
  **Mitigation**: Provide `pipx` install path + keep old setup scripts as fallback

- **Risk**: Template changes break v2 backward compatibility
  **Mitigation**: validate command explicitly checks v2 format; new fields are optional additions

- **Risk**: Compact mode loses essential protocol rules
  **Mitigation**: Compact mode is a summary, full protocol still exists for reference

- **Risk**: CLI too complex for single-file
  **Mitigation**: Keep stdlib-only, single main file with clear function boundaries

## Scope Boundary

- **IN**: cli/, templates/, README.md, pyproject.toml
- **OUT**: examples/ (except for backward compat testing), images/, SPEECH.md, LICENSE

---

> **HUMAN APPROVAL**: [x] APPROVED
>
> _Simulated approval — user authorized full end-to-end execution._
