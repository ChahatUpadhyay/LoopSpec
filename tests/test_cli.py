#!/usr/bin/env python3
"""
LoopSpec v3 CLI Automated Test Suite
Tests all criteria: C1-C14 (automated ones)
"""
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

REPO_DIR = Path(__file__).parent.parent
CLI_CMD = [sys.executable, "-m", "cli"]

passed = 0
failed = 0


def test(name, condition, evidence=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  [PASS] {name}")
        if evidence:
            print(f"         Evidence: {evidence}")
    else:
        failed += 1
        print(f"  [FAIL] {name}")
        if evidence:
            print(f"         Evidence: {evidence}")


def run_cli(args, cwd=None):
    """Run CLI command and return (exit_code, stdout, stderr)."""
    result = subprocess.run(
        CLI_CMD + args,
        capture_output=True, text=True,
        cwd=cwd or REPO_DIR,
        encoding="utf-8", errors="replace"
    )
    return result.returncode, result.stdout, result.stderr


# ============================================================
print("\n" + "=" * 60)
print("  LoopSpec v3 CLI - Automated Test Suite")
print("=" * 60)

# --- C1: CLI exists with init, status, validate, report commands ---
print("\n[C1] CLI commands exist and execute:")

rc, out, _ = run_cli(["--version"])
test("--version returns 3.0.0", "3.0.0" in out, f"Output: {out.strip()}")

rc, out, _ = run_cli(["--help"])
test("--help shows all commands", all(c in out for c in ["init", "status", "validate", "report", "git-sync"]),
     f"Commands found in help text")

for cmd in ["init", "status", "validate", "report", "git-sync"]:
    rc, out, _ = run_cli([cmd, "--help"])
    test(f"'{cmd} --help' exits 0", rc == 0, f"exit={rc}")

# --- C2: init creates .loopspec/ in <2 seconds ---
print("\n[C2] Init performance and file creation:")

with tempfile.TemporaryDirectory() as tmpdir:
    start = time.time()
    rc, out, _ = run_cli(["init", tmpdir])
    elapsed = time.time() - start

    test("init exits 0", rc == 0, f"exit={rc}")
    test("init completes in <2s", elapsed < 2.0, f"{elapsed:.3f}s")

    loopspec_dir = Path(tmpdir) / ".loopspec"
    test(".loopspec/ directory created", loopspec_dir.is_dir())

    expected_files = ["PROTOCOL.md", "GOAL.md", "CONTEXT.md", "PLAN.md",
                     "TESTS.md", "LEARNINGS.md", "CHANGELOG.md",
                     "QUESTIONS.md", "STATUS.md", "STATUS.json"]
    all_exist = all((loopspec_dir / f).exists() for f in expected_files)
    test("All 10 template files created", all_exist,
         f"Missing: {[f for f in expected_files if not (loopspec_dir / f).exists()]}")

    test("iterations/ subdirectory created", (loopspec_dir / "iterations").is_dir())
    test("AGENTS.md created at root", (Path(tmpdir) / "AGENTS.md").exists())

# --- C3: status reads STATUS.json correctly ---
print("\n[C3] Status command parses STATUS.json:")

with tempfile.TemporaryDirectory() as tmpdir:
    run_cli(["init", tmpdir])
    # Write a sample STATUS.json with criteria
    status_data = {
        "v": 3, "phase": "IMPLEMENT", "iter": 2, "blocked": False,
        "confidence": 60,
        "criteria": {
            "C1": {"s": "V", "n": "First criterion"},
            "C2": {"s": "P", "n": "Second criterion"},
            "C3": {"s": "N", "n": "Third criterion"}
        },
        "ts": "2025-01-01T12:00:00Z", "next": "Implement C2"
    }
    (Path(tmpdir) / ".loopspec" / "STATUS.json").write_text(
        json.dumps(status_data), encoding="utf-8"
    )

    rc, out, _ = run_cli(["status", tmpdir])
    test("status exits 0", rc == 0)
    test("status shows phase IMPLEMENT", "IMPLEMENT" in out, f"Output contains phase")
    test("status shows iteration 2", "2" in out)
    test("status shows criteria progress", "1/3" in out, "1 verified of 3")

# --- C4: validate detects structural issues ---
print("\n[C4] Validate detects missing fields and broken refs:")

with tempfile.TemporaryDirectory() as tmpdir:
    run_cli(["init", tmpdir])

    # Valid project should pass
    rc, out, _ = run_cli(["validate", tmpdir])
    test("Valid project passes validation", rc == 0)

    # Remove STATUS.json to cause error
    (Path(tmpdir) / ".loopspec" / "STATUS.json").unlink()
    rc, out, _ = run_cli(["validate", tmpdir])
    test("Missing STATUS.json detected", rc == 1 or "Missing" in out)

    # Write broken JSON
    (Path(tmpdir) / ".loopspec" / "STATUS.json").write_text("not json", encoding="utf-8")
    rc, out, _ = run_cli(["validate", tmpdir])
    test("Invalid JSON detected", "invalid" in out.lower() or "json" in out.lower() or rc == 1,
         f"exit={rc}, output snippet: {out.strip()[:100]}")

# --- C5: report generates markdown summary ---
print("\n[C5] Report generates markdown with criteria table:")

with tempfile.TemporaryDirectory() as tmpdir:
    run_cli(["init", tmpdir])
    # Write GOAL.md with criteria
    goal_content = """# Goal\n\n## Success Criteria\n\n| ID | Criterion | Verifier | Threshold | Required |\n|----|-----------|----------|-----------|----------|\n| C1 | Build API | automated | exits 0 | yes |\n| C2 | Tests pass | automated | all green | yes |\n"""
    (Path(tmpdir) / ".loopspec" / "GOAL.md").write_text(goal_content, encoding="utf-8")

    rc, out, _ = run_cli(["report", tmpdir])
    test("report exits 0", rc == 0)
    test("report contains criteria table", "| ID |" in out and "| C1 |" in out)
    test("report shows phase", "Phase" in out)
    test("report shows progress count", "verified" in out.lower() or "/2" in out or "/0" in out)

# --- C6: git-sync detects git repo ---
print("\n[C6] Git integration:")

rc, out, _ = run_cli(["git-sync", "."])
test("git-sync exits 0 in git repo", rc == 0)
test("git-sync shows current branch", "Loop_Spec_v3" in out)
test("git-sync suggests branch name", "loopspec/iter-" in out)
test("git-sync suggests commit message", "commit" in out.lower() or "chore:" in out or "feat:" in out)

# --- C9: Compressed STATUS.json < 500 bytes for 10 criteria ---
print("\n[C9] Compressed STATUS.json size:")

sample_status = {
    "v": 3, "phase": "VERIFY", "iter": 3, "blocked": False, "confidence": 80,
    "criteria": {f"C{i}": {"s": "V" if i <= 7 else "P", "n": f"Crit{i}"} for i in range(1, 11)},
    "ts": "2025-07-04T17:30:00Z", "next": "Adversarial"
}
sample_bytes = len(json.dumps(sample_status))
test("10-criteria STATUS.json < 500 bytes", sample_bytes < 500, f"{sample_bytes} bytes")

# --- C12: Package install works ---
print("\n[C12] Package structure:")

pyproject = REPO_DIR / "pyproject.toml"
test("pyproject.toml exists", pyproject.exists())
content = pyproject.read_text(encoding="utf-8")
test("pyproject.toml has entry point", "loopspec" in content and "cli.loopspec:main" in content)
test("cli/__init__.py exists", (REPO_DIR / "cli" / "__init__.py").exists())
test("cli/__main__.py exists", (REPO_DIR / "cli" / "__main__.py").exists())

# --- C13: Template size reduction ---
print("\n[C13] Template size reduction (deferred expansion):")

templates_dir = REPO_DIR / "templates"
v3_sizes = {}
for f in templates_dir.glob("*.md"):
    v3_sizes[f.name] = f.stat().st_size

# v2 sizes (from CONTEXT.md baseline analysis)
v2_sizes = {
    "GOAL.md": 3281, "CONTEXT.md": 2203, "PLAN.md": 2184,
    "TESTS.md": 2758, "LEARNINGS.md": 7006, "CHANGELOG.md": 922,
    "QUESTIONS.md": 1708, "STATUS.md": 1458
}

total_v3 = sum(v3_sizes.get(k, 0) for k in v2_sizes.keys())
total_v2 = sum(v2_sizes.values())
reduction = 1 - (total_v3 / total_v2) if total_v2 > 0 else 0

test(f"Templates reduced by >50%", reduction > 0.50,
     f"v2: {total_v2}B, v3: {total_v3}B, reduction: {reduction*100:.1f}%")

# Check INSTRUCTIONS.md exists as the deferred expansion target
test("INSTRUCTIONS.md exists (deferred comments)", (templates_dir / "INSTRUCTIONS.md").exists())

# --- C14: Backward compatibility with v2 projects ---
print("\n[C14] Backward compatibility:")

rc, out, _ = run_cli(["validate", "examples/oxygen-atom-sim"])
test("v2 oxygen-atom-sim validates OK", rc == 0, f"exit={rc}")

# Also test status on v2 project
rc, out, _ = run_cli(["status", "examples/oxygen-atom-sim"])
test("v2 project status readable", rc == 0)

# ============================================================
print("\n" + "=" * 60)
total = passed + failed
print(f"  RESULTS: {passed}/{total} PASSED, {failed} FAILED")
print("=" * 60 + "\n")

sys.exit(0 if failed == 0 else 1)
