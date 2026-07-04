#!/usr/bin/env python3
"""
LoopSpec CLI v3.0 - Self-correcting AI development protocol tooling.

Commands:
    init        Initialize .loopspec/ in a project directory
    status      Display current protocol state from STATUS.json
    validate    Check .loopspec/ files for structural correctness
    report      Generate markdown summary of current state
    git-sync    Git integration - branch proposals, commit messages

Zero dependencies beyond Python 3.9+ stdlib.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

__version__ = "3.0.0"

# --- Constants ---
LOOPSPEC_DIR = ".loopspec"
REQUIRED_FILES = [
    "PROTOCOL.md", "GOAL.md", "CONTEXT.md", "PLAN.md",
    "TESTS.md", "LEARNINGS.md", "CHANGELOG.md",
    "QUESTIONS.md", "STATUS.md", "STATUS.json"
]
PHASES = [
    "IDLE", "ANALYZE", "PLAN", "WAITING_HUMAN", "TEST_DESIGN",
    "IMPLEMENT", "VERIFY", "ADVERSARIAL_CHECK", "EVALUATE", "DONE", "BLOCKED"
]

# ANSI colors (disabled on Windows without VT100 support)
def _supports_color():
    if os.environ.get("NO_COLOR"):
        return False
    if sys.platform == "win32":
        return os.environ.get("WT_SESSION") or os.environ.get("TERM_PROGRAM")
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

USE_COLOR = _supports_color()

def c(text, code):
    """Colorize text if terminal supports it."""
    if not USE_COLOR:
        return text
    return f"\033[{code}m{text}\033[0m"

def green(t): return c(t, "32")
def red(t): return c(t, "31")
def yellow(t): return c(t, "33")
def cyan(t): return c(t, "36")
def bold(t): return c(t, "1")
def dim(t): return c(t, "2")


# ============================================================
# COMMAND: init
# ============================================================
def cmd_init(args):
    """Initialize .loopspec/ in target directory."""
    target = Path(args.target).resolve()
    if not target.is_dir():
        print(red(f"Error: '{target}' is not a directory"))
        return 1

    loopspec_dir = target / LOOPSPEC_DIR
    iterations_dir = loopspec_dir / "iterations"
    agents_file = target / "AGENTS.md"

    # Find templates (relative to this script or installed package)
    templates_dir = _find_templates_dir()
    if not templates_dir:
        print(red("Error: Cannot find templates/ directory."))
        print("  Ensure you're running from the LoopSpec repo or have installed the package.")
        return 1

    start_time = time.time()

    # Create directories
    loopspec_dir.mkdir(exist_ok=True)
    iterations_dir.mkdir(exist_ok=True)

    # Copy templates
    copied = 0
    skipped = 0
    for fname in REQUIRED_FILES:
        src = templates_dir / fname
        dst = loopspec_dir / fname
        if not src.exists():
            print(yellow(f"  [WARN] Template missing: {fname}"))
            continue
        if dst.exists() and not args.repair:
            skipped += 1
            continue
        if dst.exists() and args.repair:
            # In repair mode, only overwrite PROTOCOL.md (operating manual updates)
            if fname != "PROTOCOL.md":
                skipped += 1
                continue
        shutil.copy2(src, dst)
        copied += 1

    # Create AGENTS.md if not exists
    if not agents_file.exists():
        agents_file.write_text(
            "# AI Agent Entry Point\n\n"
            "Read `.loopspec/PROTOCOL.md` to understand your operating protocol.\n\n"
            "Then read `.loopspec/STATUS.json` to know where to resume.\n",
            encoding="utf-8"
        )

    # Git detection
    git_info = ""
    if _is_git_repo(target):
        branch = _git_branch(target)
        git_info = f"\n  Git detected: branch '{branch}'"

    elapsed = time.time() - start_time

    print(f"\n{bold('LoopSpec v3 initialized')} in {elapsed:.2f}s")
    print(f"  Directory: {loopspec_dir}")
    print(f"  Files: {copied} copied, {skipped} preserved")
    if git_info:
        print(git_info)
    print(f"\n  Next: Edit {cyan('.loopspec/GOAL.md')} then tell your AI:")
    hint = '"Read .loopspec/PROTOCOL.md and begin."'
    print(f"  {dim(hint)}\n")
    return 0


# ============================================================
# COMMAND: status
# ============================================================
def cmd_status(args):
    """Display current protocol state."""
    target = Path(args.target).resolve()
    status_file = target / LOOPSPEC_DIR / "STATUS.json"

    if not status_file.exists():
        print(red("Error: No .loopspec/STATUS.json found."))
        print(f"  Run: loopspec init {target}")
        return 1

    try:
        data = json.loads(status_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(red(f"Error: Invalid STATUS.json - {e}"))
        return 1

    phase = data.get("phase", "UNKNOWN")
    iteration = data.get("iter", data.get("iteration", 0))
    blocked = data.get("blocked", False)
    confidence = data.get("confidence", 0)
    criteria = data.get("criteria", {})

    # Phase coloring
    phase_color = green if phase == "DONE" else (red if phase == "BLOCKED" else yellow)

    print(f"\n{bold('LoopSpec Status')}")
    print(f"  Phase:      {phase_color(phase)}")
    print(f"  Iteration:  {iteration}")
    print(f"  Blocked:    {'YES' if blocked else 'no'}")
    print(f"  Confidence: {confidence}%")

    if criteria:
        verified = sum(1 for v in criteria.values() if v.get("s") == "V" or v.get("status") == "VERIFIED")
        total = len(criteria)
        bar = _progress_bar(verified, total)
        print(f"\n  Criteria: {bar} {verified}/{total}")
        for cid, info in criteria.items():
            status = info.get("s", info.get("status", "?"))
            symbol = green("+") if status in ("V", "VERIFIED") else (red("X") if status in ("F", "FAILED") else dim("o"))
            print(f"    {symbol} {cid}: {info.get('n', info.get('name', ''))}")

    # Git info
    if _is_git_repo(target):
        branch = _git_branch(target)
        print(f"\n  Git: {cyan(branch)}")

    print()
    return 0


# ============================================================
# COMMAND: validate
# ============================================================
def cmd_validate(args):
    """Validate .loopspec/ structure and content."""
    target = Path(args.target).resolve()
    loopspec_dir = target / LOOPSPEC_DIR

    if not loopspec_dir.is_dir():
        print(red(f"Error: No .loopspec/ directory in {target}"))
        return 1

    issues = []
    warnings = []

    # Check required files exist
    for fname in REQUIRED_FILES:
        fpath = loopspec_dir / fname
        if not fpath.exists():
            issues.append(f"Missing required file: {fname}")

    # Validate STATUS.json
    status_file = loopspec_dir / "STATUS.json"
    if status_file.exists():
        try:
            data = json.loads(status_file.read_text(encoding="utf-8"))
            if "phase" not in data:
                issues.append("STATUS.json missing 'phase' field")
            elif data["phase"] not in PHASES:
                warnings.append(f"STATUS.json phase '{data['phase']}' not in known phases")
            if "iteration" not in data and "iter" not in data:
                issues.append("STATUS.json missing 'iteration' (or 'iter') field")
        except json.JSONDecodeError as e:
            issues.append(f"STATUS.json invalid JSON: {e}")

    # Validate GOAL.md has criteria
    goal_file = loopspec_dir / "GOAL.md"
    if goal_file.exists():
        goal_content = goal_file.read_text(encoding="utf-8")
        criterion_ids = re.findall(r'\|\s*(C\d+)\s*\|', goal_content)
        if not criterion_ids:
            warnings.append("GOAL.md: No criterion IDs (C1, C2...) found in table format")
        else:
            # Check TESTS.md references valid criterion IDs
            tests_file = loopspec_dir / "TESTS.md"
            if tests_file.exists():
                tests_content = tests_file.read_text(encoding="utf-8")
                test_refs = set(re.findall(r'C\d+', tests_content))
                goal_ids = set(criterion_ids)
                orphan_refs = test_refs - goal_ids
                if orphan_refs:
                    warnings.append(f"TESTS.md references unknown criteria: {orphan_refs}")

    # Validate PROTOCOL.md exists and has version
    proto_file = loopspec_dir / "PROTOCOL.md"
    if proto_file.exists():
        proto_content = proto_file.read_text(encoding="utf-8")
        if "v2" not in proto_content.lower() and "v3" not in proto_content.lower():
            warnings.append("PROTOCOL.md: No version identifier found")

    # Check LEARNINGS.md is not corrupted (append-only check)
    learnings_file = loopspec_dir / "LEARNINGS.md"
    if learnings_file.exists():
        content = learnings_file.read_text(encoding="utf-8")
        if content.strip() and "# " not in content:
            warnings.append("LEARNINGS.md: Missing heading structure")

    # Report results
    print(f"\n{bold('LoopSpec Validation')}: {loopspec_dir}\n")

    if not issues and not warnings:
        print(f"  {green('[OK] All checks passed')} - project is valid\n")
        return 0

    if issues:
        print(f"  {red('Errors')} ({len(issues)}):")
        for issue in issues:
            print(f"    {red('X')} {issue}")

    if warnings:
        print(f"  {yellow('Warnings')} ({len(warnings)}):")
        for warn in warnings:
            print(f"    {yellow('!')} {warn}")

    print()
    return 1 if issues else 0


# ============================================================
# COMMAND: report
# ============================================================
def cmd_report(args):
    """Generate markdown summary report."""
    target = Path(args.target).resolve()
    loopspec_dir = target / LOOPSPEC_DIR

    if not loopspec_dir.is_dir():
        print(red(f"Error: No .loopspec/ directory in {target}"))
        return 1

    # Read STATUS.json
    status_data = {}
    status_file = loopspec_dir / "STATUS.json"
    if status_file.exists():
        try:
            status_data = json.loads(status_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass

    # Read GOAL.md for criteria
    criteria_list = []
    goal_file = loopspec_dir / "GOAL.md"
    if goal_file.exists():
        goal_content = goal_file.read_text(encoding="utf-8")
        # Parse table rows
        for match in re.finditer(r'\|\s*(C\d+)\s*\|\s*([^|]+)\|', goal_content):
            criteria_list.append((match.group(1), match.group(2).strip()))

    # Build report
    phase = status_data.get("phase", "UNKNOWN")
    iteration = status_data.get("iteration", 0)
    criteria_status = status_data.get("criteria", {})

    verified = sum(1 for v in criteria_status.values() if v.get("s") == "V" or v.get("status") == "VERIFIED")
    failed = sum(1 for v in criteria_status.values() if v.get("s") == "F" or v.get("status") == "FAILED")
    total = len(criteria_list) or len(criteria_status)

    report = []
    report.append("# LoopSpec Progress Report\n")
    report.append(f"**Phase**: {phase}  ")
    report.append(f"**Iteration**: {iteration}  ")
    report.append(f"**Progress**: {verified}/{total} criteria verified  ")
    if failed:
        report.append(f"**Failed**: {failed}  ")
    report.append("")

    # Criteria table
    if criteria_list:
        report.append("## Criteria Status\n")
        report.append("| ID | Criterion | Status |")
        report.append("|----|-----------|--------|")
        for cid, desc in criteria_list:
            info = criteria_status.get(cid, {})
            status = info.get("s", info.get("status", "NOT_STARTED"))
            status_display = {"V": "VERIFIED", "F": "FAILED", "P": "IN_PROGRESS"}.get(status, status)
            report.append(f"| {cid} | {desc} | {status_display} |")
        report.append("")

    # Phase history from status
    history = status_data.get("history", [])
    if history:
        report.append("## Phase History\n")
        report.append("| Phase | Result | Timestamp |")
        report.append("|-------|--------|-----------|")
        for entry in history:
            report.append(f"| {entry.get('phase', '?')} | {entry.get('result', '?')} | {entry.get('ts', '?')} |")
        report.append("")

    output = "\n".join(report)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Report written to: {args.output}")
    else:
        print(output)

    return 0


# ============================================================
# COMMAND: git-sync
# ============================================================
def cmd_git_sync(args):
    """Git integration - branch proposals and commit messages."""
    target = Path(args.target).resolve()

    if not _is_git_repo(target):
        print(red("Error: Not a git repository"))
        print(f"  Run: git init {target}")
        return 1

    loopspec_dir = target / LOOPSPEC_DIR
    status_file = loopspec_dir / "STATUS.json"

    # Read current state
    status_data = {}
    if status_file.exists():
        try:
            status_data = json.loads(status_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass

    phase = status_data.get("phase", "IDLE")
    iteration = status_data.get("iteration", 1)
    branch = _git_branch(target)

    print(f"\n{bold('LoopSpec Git Sync')}")
    print(f"  Current branch: {cyan(branch)}")
    print(f"  Phase: {phase}")
    print(f"  Iteration: {iteration}")

    # Suggest branch name
    suggested_branch = f"loopspec/iter-{iteration}"
    print(f"\n  Suggested branch: {green(suggested_branch)}")

    # Generate commit message based on phase
    criteria_status = status_data.get("criteria", {})
    if isinstance(criteria_status, list):
        criteria_status = {}  # v2 format uses list, convert to empty dict gracefully
    verified_ids = [k for k, v in criteria_status.items() if v.get("s") == "V" or v.get("status") == "VERIFIED"]

    if phase == "DONE":
        msg = f"feat: Complete all criteria ({', '.join(verified_ids) or 'all'})"
    elif phase in ("IMPLEMENT", "VERIFY"):
        msg = f"wip: Phase {phase.lower()}, iteration {iteration}"
        if verified_ids:
            msg += f" [{', '.join(verified_ids)} verified]"
    else:
        msg = f"chore: LoopSpec phase {phase.lower()}, iteration {iteration}"

    print(f"  Suggested commit: {dim(msg)}")

    # Show diff stats
    try:
        result = subprocess.run(
            ["git", "diff", "--stat", "--cached"],
            capture_output=True, text=True, cwd=target
        )
        if result.stdout.strip():
            print(f"\n  Staged changes:\n{dim(result.stdout)}")
        else:
            result2 = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True, text=True, cwd=target
            )
            changed = len(result2.stdout.strip().splitlines())
            print(f"\n  Unstaged changes: {changed} files")
    except (FileNotFoundError, subprocess.SubprocessError):
        pass

    # Tag suggestion
    if phase == "DONE":
        tag = f"loopspec-done-iter{iteration}"
        print(f"  Suggested tag: {green(tag)}")

    print()
    return 0


# ============================================================
# Utility Functions
# ============================================================
def _find_templates_dir() -> Optional[Path]:
    """Find the templates/ directory relative to this script or package."""
    # Check relative to script location (dev mode)
    script_dir = Path(__file__).parent.parent
    templates = script_dir / "templates"
    if templates.is_dir():
        return templates

    # Check relative to package data
    pkg_templates = Path(__file__).parent / "templates"
    if pkg_templates.is_dir():
        return pkg_templates

    return None


def _is_git_repo(path: Path) -> bool:
    """Check if path is inside a git repository."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True, text=True, cwd=path
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def _git_branch(path: Path) -> str:
    """Get current git branch name."""
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True, text=True, cwd=path
        )
        return result.stdout.strip() or "HEAD (detached)"
    except (FileNotFoundError, subprocess.SubprocessError):
        return "unknown"


def _progress_bar(done: int, total: int, width: int = 20) -> str:
    """Generate a simple progress bar."""
    if total == 0:
        return "[" + " " * width + "]"
    filled = int(width * done / total)
    bar = "#" * filled + "." * (width - filled)
    return f"[{bar}]"


# ============================================================
# Main Entry Point
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        prog="loopspec",
        description="LoopSpec v3 CLI - Self-correcting AI development protocol",
        epilog="https://github.com/ChahatUpadhyay/LoopSpec"
    )
    parser.add_argument("--version", action="version", version=f"loopspec {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init
    p_init = subparsers.add_parser("init", help="Initialize .loopspec/ in a project")
    p_init.add_argument("target", nargs="?", default=".", help="Target directory (default: current)")
    p_init.add_argument("--repair", action="store_true", help="Update protocol without overwriting user data")

    # status
    p_status = subparsers.add_parser("status", help="Show current protocol state")
    p_status.add_argument("target", nargs="?", default=".", help="Project directory")

    # validate
    p_validate = subparsers.add_parser("validate", help="Check .loopspec/ structural correctness")
    p_validate.add_argument("target", nargs="?", default=".", help="Project directory")

    # report
    p_report = subparsers.add_parser("report", help="Generate markdown progress report")
    p_report.add_argument("target", nargs="?", default=".", help="Project directory")
    p_report.add_argument("-o", "--output", help="Write report to file instead of stdout")

    # git-sync
    p_git = subparsers.add_parser("git-sync", help="Git integration - branch/commit suggestions")
    p_git.add_argument("target", nargs="?", default=".", help="Project directory")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    commands = {
        "init": cmd_init,
        "status": cmd_status,
        "validate": cmd_validate,
        "report": cmd_report,
        "git-sync": cmd_git_sync,
    }

    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main() or 0)
