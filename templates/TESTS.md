# Test Cases

<!--
  MODEL: Design these BEFORE implementation (Phase 3).

  CRITICAL RULES:
  1. Each test MUST reference a criterion ID from GOAL.md
  2. Tests MUST execute production code — never test duplicate implementations
  3. Tests MUST be falsifiable — if a test cannot fail, it proves nothing
  4. You MUST NOT weaken tests to make them pass without human approval
  5. Each test must be marked as "required" or "optional"

  Status legend:
    NOT_RUN  — designed but not executed
    PASSED   — ran and produced expected output (with evidence)
    FAILED   — ran and did NOT produce expected output
    SKIPPED  — skipped (reason documented)
-->

## Iteration: 1

<!--
## Test T[N]: [Descriptive Name]
- **Criterion**: [C1/C2/... — which criterion ID from GOAL.md]
- **Required**: [yes | no]
- **Type**: [unit | integration | e2e | manual]
- **Verifier**: [automated | manual]
- **Description**: [What this test verifies]
- **Setup**: [Any prerequisites, environment, or data needed]
- **Input**: [What to provide or trigger]
- **Expected Output**: [Exact expected result — be specific and measurable]
- **Threshold**: [What counts as pass — exact value or condition]
- **Command**: `[shell command to run this test]`
- **Status**: NOT_RUN

### Evidence (filled after running)
- **Command Executed**: `[exact command]`
- **Exit Code**: [0/1/etc]
- **Actual Output**: [raw output — key parts, truncated if very long]
- **Evidence Location**: [file path or log location]
- **Environment**: [OS, runtime version]
- **Timestamp**: [when this was run]
- **Notes**: [any observations]
-->

## Test Summary

| # | Name | Criterion | Type | Required | Verifier | Status | Evidence |
|---|------|-----------|------|----------|----------|--------|----------|

## Test Sufficiency Check

<!--
  MODEL: After all tests pass, honestly answer:
  - [ ] Does every REQUIRED criterion have at least one required test?
  - [ ] Are edge cases covered?
  - [ ] Are integration points tested?
  - [ ] Could the code pass these tests but still be wrong?
  - [ ] Am I testing production code directly (not copies/duplicates)?
  - [ ] Is every assertion specific enough to catch real defects?
  - [ ] Would an adversarial reviewer find gaps in this coverage?

  If any answer is "no" or "possibly", add more tests before proceeding.
-->

## Adversarial Checks

<!--
  MODEL: Fill this during Phase 6 (ADVERSARIAL CHECK).
  For each criterion, try to break it. Document what you tried and what happened.

| Criterion | Adversarial Scenario | Result | Evidence |
|-----------|---------------------|--------|----------|
| C1 | [what you tried] | [held / broke] | [proof] |
-->
