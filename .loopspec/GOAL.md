# Goal

## Objective

Design and implement **LoopSpec v3** — a major protocol upgrade focused on:

1. **CLI Tool**: Easy-to-use command-line interface with basic commands (`loopspec init`, `loopspec status`, `loopspec validate`, `loopspec report`) that reduces manual setup friction and enables programmatic interaction.

2. **Git Integration**: Built-in git awareness — auto-branching per iteration, diff tracking, commit message generation tied to criterion IDs, and optional auto-commit on phase transitions.

3. **Context Overhead Reduction**: Reduce token/context consumption by 40%+ without losing protocol effectiveness. Techniques: compressed state format, selective file loading (only read what's needed per phase), summary-on-demand, deferred template expansion.

4. **Performance for Complex Tasks**: Improve success rate on complex multi-file tasks through parallel criterion tracking, dependency-aware execution ordering, incremental verification (verify as you go, not all at end), and smart retry strategies.

5. **User Convenience**: Reduce friction — fewer manual steps, better defaults, progress visualization, one-command setup, IDE integration hooks.

6. **Cost Reduction**: Minimize model context usage through efficient file formats, phase-specific minimal reads, compressed learnings, and avoiding redundant re-reads.

## Success Criteria

| ID | Criterion | Verifier | Threshold | Required |
|----|-----------|----------|-----------|----------|
| C1 | CLI tool exists with `init`, `status`, `validate`, `report` commands | automated | All 4 commands execute without error, produce expected output | yes |
| C2 | CLI `init` creates .loopspec/ with all templates in <2 seconds | automated | Timing test + file existence check | yes |
| C3 | CLI `status` reads STATUS.json and displays human-readable progress | automated | Correct parsing + formatted output for sample STATUS.json | yes |
| C4 | CLI `validate` checks all .loopspec/ files for structural correctness | automated | Detects missing fields, broken criterion refs, empty required sections | yes |
| C5 | CLI `report` generates a markdown summary of current state | automated | Output contains criteria table, phase history, pass/fail counts | yes |
| C6 | Git integration: protocol auto-detects git repo and tracks iterations via branches/tags | automated | Running in git repo shows branch info, iteration tag proposal | yes |
| C7 | Context reduction: PROTOCOL.md has a "compact mode" section <2000 tokens that contains all essential rules | metric | Token count of compact section < 2000 (measured by word count / 0.75) | yes |
| C8 | Context reduction: Phase-specific loading guide tells model which files to read per phase (not all) | manual | Each phase lists exactly which files to read, reducing from 10 to 2-4 per phase | yes |
| C9 | Compressed STATUS format: STATUS.json contains full state in <500 bytes for typical project | automated | Sample STATUS.json for 10 criteria project is < 500 bytes | yes |
| C10 | Incremental verification: PROTOCOL.md allows verify-as-you-go after each criterion implementation | manual | Protocol text explicitly supports partial verification with rules | yes |
| C11 | Smart retry: PROTOCOL.md defines retry strategies (bisect, isolate, simplify) beyond "materially different" | manual | At least 3 named retry strategies with when-to-use guidance | yes |
| C12 | User convenience: Single-command quickstart works cross-platform (npx/pip/cargo or curl pipe) | automated | Install command exists and produces working CLI | yes |
| C13 | Cost reduction: Templates use deferred expansion (comments/instructions only loaded when needed) | metric | Template files without comments are <50% size of v2 templates | yes |
| C14 | All changes are backward-compatible with v2 projects (v2 .loopspec/ dirs still work) | automated | CLI `validate` passes on existing v2 example project without modification | yes |
| C15 | README documents all v3 features with usage examples | manual | Each new feature has code example in README | yes |

## Permissions

### Standard Permissions
- [x] Read all project files
- [x] Create new files
- [x] Modify existing files
- [x] Delete files (cleanup only)
- [x] Execute shell commands
- [x] Run tests
- [x] Git operations (commit, branch, push)
- [x] Install dependencies (npm, pip, cargo, etc.)
- [x] Modify configuration files

### Safety-Gated Permissions (require explicit approval per action)
- [ ] Access network / external APIs
- [ ] Deploy to production/staging
- [x] Actions involving secrets/credentials (PAT for push)
- [ ] Paid API calls or cloud resource creation
- [x] Irreversible operations (push to remote — approved)

## Constraints

- Must remain model-agnostic (no OpenAI/Anthropic-specific features)
- CLI must work without runtime dependencies beyond Node.js 18+ OR Python 3.9+
- Protocol files remain Markdown (human-readable first, machine-parseable second)
- No breaking changes to v2 file format — only additions
- Keep total protocol size reasonable (PROTOCOL.md < 30KB)
- CLI should be zero-config for basic usage

## Priority

cost_reduction > user_convenience > performance > features > elegance

## Quality Threshold

- CLI passes all automated tests on Windows PowerShell
- Protocol changes don't break existing v2 examples
- Context reduction measurably demonstrated (before/after token counts)
- At least one complex example project uses v3 features

## Max Iterations

max_iterations: 5

## Additional Context

- v2 repo: https://github.com/ChahatUpadhyay/LoopSpec
- Current branch: Loop_Spec_v3 (branched from main after v2 merge)
- Key v2 pain points observed during testing:
  - Model must read ALL 10 files at start (expensive context)
  - Setup requires cloning repo + running script (friction)
  - No programmatic way to check protocol health
  - No git awareness (manual branching/committing)
  - Retry guidance is vague ("materially different" without concrete strategies)
  - Templates have verbose comments that inflate token usage
  - No incremental verification (must implement everything before testing)
