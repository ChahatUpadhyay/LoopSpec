"""
LoopSpec v2 CLI — initialize projects, check status, and generate reports.
"""

import argparse
import json
import sys
from pathlib import Path

LOOPSPEC_DIR = ".loopspec"
CONFIG_FILE = "loopspec.json"


def cmd_init(args):
    """Initialize a LoopSpec v2 project in the current directory."""
    project_dir = Path(LOOPSPEC_DIR)
    project_dir.mkdir(exist_ok=True)

    config = {
        "version": "2.0.0",
        "project_name": args.name or Path.cwd().name,
        "max_retries": args.max_retries,
        "validation_rules": [],
        "anchors": [],
        "metrics_output": str(project_dir / "metrics.json"),
    }

    config_path = project_dir / CONFIG_FILE
    config_path.write_text(json.dumps(config, indent=2))

    # Create template correction handler
    handler_path = project_dir / "correction_handler.py"
    if not handler_path.exists():
        handler_path.write_text('''"""
LoopSpec v2 — Custom correction handler template.

Implement your correction logic here. This function is called
when validation fails, and should return a corrected input dict.
"""


def handle_correction(correction_context: dict) -> dict:
    """
    Called when a validation check fails.

    Args:
        correction_context: Dict with keys:
            - attempt: current attempt number
            - errors: list of validation errors
            - warnings: list of validation warnings
            - error_type: "validation" or "exception"
            - previous_input: the input that produced the bad output
            - previous_output: the output that failed validation
            - context_state: current context state
            - drift: drift report if detected

    Returns:
        A corrected input dict for the next attempt.
    """
    previous_input = correction_context["previous_input"]
    errors = correction_context.get("errors", [])

    # Example: append error info to the prompt for self-correction
    error_summary = "; ".join(e["message"] for e in errors)
    corrected = previous_input.copy()
    corrected["correction_hint"] = f"Previous attempt failed: {error_summary}. Please fix."
    corrected["attempt"] = correction_context["attempt"] + 1

    return corrected
''')

    print(f"✅ LoopSpec v2 initialized in {project_dir.resolve()}")
    print(f"   Config: {config_path}")
    print(f"   Correction handler: {handler_path}")
    print(f"   Max retries: {config['max_retries']}")


def cmd_status(args):
    """Show the status of the current LoopSpec project."""
    config_path = Path(LOOPSPEC_DIR) / CONFIG_FILE
    if not config_path.exists():
        print("❌ No LoopSpec project found. Run `loopspec init` first.")
        sys.exit(1)

    config = json.loads(config_path.read_text())
    metrics_path = Path(config.get("metrics_output", ""))

    print(f"\n📋 LoopSpec v{config['version']} Project Status")
    print(f"   Project: {config['project_name']}")
    print(f"   Max retries: {config['max_retries']}")
    print(f"   Validation rules: {len(config.get('validation_rules', []))}")

    if metrics_path.exists():
        metrics = json.loads(metrics_path.read_text())
        summary = metrics.get("summary", {})
        print(f"\n📊 Last Metrics:")
        print(f"   Iterations: {summary.get('total_iterations', 'N/A')}")
        print(f"   Success Rate: {summary.get('success_rate', 'N/A')}")
        print(f"   Drift Events: {summary.get('drift_events', 'N/A')}")
    else:
        print(f"\n   No metrics recorded yet.")


def cmd_report(args):
    """Generate a metrics report."""
    config_path = Path(LOOPSPEC_DIR) / CONFIG_FILE
    if not config_path.exists():
        print("❌ No LoopSpec project found. Run `loopspec init` first.")
        sys.exit(1)

    config = json.loads(config_path.read_text())
    metrics_path = Path(config.get("metrics_output", ""))

    if not metrics_path.exists():
        print("❌ No metrics file found. Run your correction loop first.")
        sys.exit(1)

    metrics = json.loads(metrics_path.read_text())

    if args.format == "json":
        print(json.dumps(metrics, indent=2))
    else:
        summary = metrics.get("summary", {})
        print("\n╔══════════════════════════════════════╗")
        print("║       LoopSpec v2 Metrics Report     ║")
        print("╠══════════════════════════════════════╣")
        for key, val in summary.items():
            print(f"║  {key:<20} {str(val):>14}  ║")
        print("╚══════════════════════════════════════╝")

        iterations = metrics.get("iterations", [])
        if iterations:
            print(f"\n  Iteration Details ({len(iterations)} total):")
            for it in iterations:
                status = "✅" if it["passed"] else "❌"
                print(f"    {status} #{it['iteration']} — {it['duration_ms']:.1f}ms — errors: {it['error_count']}")


def main():
    parser = argparse.ArgumentParser(
        prog="loopspec",
        description="LoopSpec v2 — Self-correcting AI development protocol CLI",
    )
    subparsers = parser.add_subparsers(dest="command")

    # init
    init_parser = subparsers.add_parser("init", help="Initialize a new LoopSpec project")
    init_parser.add_argument("--name", type=str, default=None, help="Project name")
    init_parser.add_argument("--max-retries", type=int, default=3, help="Default max retries")

    # status
    subparsers.add_parser("status", help="Show project status")

    # report
    report_parser = subparsers.add_parser("report", help="Generate metrics report")
    report_parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")

    args = parser.parse_args()

    if args.command == "init":
        cmd_init(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "report":
        cmd_report(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()