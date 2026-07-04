# Goal

<!--
  INSTRUCTIONS FOR HUMAN:
  Fill in the sections below to define what you want the AI model to achieve.
  Be as specific as possible — the model will use this as its north star.

  Each criterion MUST have a unique ID (C1, C2, ...) — the model uses these
  for traceability throughout the protocol.

  After filling this out, tell the model: "Read .loopspec/PROTOCOL.md and begin."
-->

## Objective

<!-- Describe what you want to achieve. Be specific and clear. -->
<!-- Example: "Add user authentication to the Express.js API using JWT tokens" -->

[Describe your goal here]

## Success Criteria

<!--
  Each criterion must have:
  - A unique ID (C1, C2, ...)
  - A clear, objectively verifiable description
  - A verifier type: how it will be checked (automated test, manual check, metric)
  - A threshold: what "pass" means (exact value, range, or condition)
  - Required flag: is this mandatory or nice-to-have?

  The model will not stop until ALL required criteria are VERIFIED with evidence.
-->

| ID | Criterion | Verifier | Threshold | Required |
|----|-----------|----------|-----------|----------|
| C1 | [description] | [automated/manual/metric] | [what counts as pass] | yes/no |
| C2 | [description] | [automated/manual/metric] | [what counts as pass] | yes/no |
| C3 | [description] | [automated/manual/metric] | [what counts as pass] | yes/no |

## Permissions

<!--
  Check what the model is ALLOWED to do.
  Unchecked items are FORBIDDEN — the model must ask before doing them.
-->

### Standard Permissions
- [x] Read all project files
- [x] Create new files
- [x] Modify existing files
- [ ] Delete files
- [ ] Execute shell commands
- [ ] Run tests
- [ ] Git operations (commit, branch, push)
- [ ] Install dependencies (npm, pip, cargo, etc.)
- [ ] Modify configuration files

### Safety-Gated Permissions (require explicit approval per action)
- [ ] Access network / external APIs
- [ ] Modify database schemas
- [ ] Deploy to production/staging
- [ ] Actions involving secrets/credentials
- [ ] Paid API calls or cloud resource creation
- [ ] Irreversible operations (publish, send, delete remote)

## Constraints

<!--
  Boundaries the model must respect. Examples:
  - "Don't change the public API"
  - "Must support Node 18+"
  - "Keep bundle size under 500KB"
  - "Follow existing code style"
  - "No new dependencies without approval"
-->

## Priority

<!--
  What matters most? This helps the model make trade-off decisions.
  Examples: correctness > speed, readability > cleverness, test coverage > features
-->

## Quality Threshold

<!--
  Optional: define what "good enough" means for this task.
  Examples:
  - "All automated tests pass on first run"
  - ">80% test coverage on new code"
  - "Zero console errors in browser"
  - "Response time < 200ms for all endpoints"
-->

## Max Iterations

<!--
  How many full plan->implement->verify->evaluate cycles before stopping?
  Default is 10. Set lower for simple tasks, higher for complex ones.
-->
max_iterations: 10

## Additional Context

<!--
  Optional: anything else the model should know.
  Links to docs, design decisions, related PRs, user stories, etc.
-->
