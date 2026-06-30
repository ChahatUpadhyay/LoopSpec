"""
LoopSpec v2 Demo — Self-Correcting Loop in Action

This example shows a task that generates a list of numbers.
The validator checks that the list is sorted and has the right length.
The correction handler fixes the input on each retry.
"""

import random
from loopspec import CorrectionLoop, Validator


def number_generator(input_dict: dict) -> list:
    """
    Simulates a task that generates a list of numbers.
    On early attempts it may produce unsorted or wrong-length results.
    The correction_hint helps it "learn" to produce correct output.
    """
    count = input_dict.get("count", 5)
    attempt = input_dict.get("attempt", 1)

    # Simulate imperfect output on first attempts
    if attempt <= 1:
        # First attempt: wrong length and unsorted
        return [random.randint(1, 100) for _ in range(count - 1)]
    elif attempt == 2:
        # Second attempt: right length but unsorted
        return [random.randint(1, 100) for _ in range(count)]
    else:
        # Third attempt: correct — sorted and right length
        return sorted([random.randint(1, 100) for _ in range(count)])


def correction_handler(ctx: dict) -> dict:
    """Fix the input based on what went wrong."""
    corrected = ctx["previous_input"].copy()
    corrected["attempt"] = ctx["attempt"] + 1

    errors = ctx.get("errors", [])
    error_msgs = [e["message"] for e in errors]
    print(f"  🔧 Correction #{ctx['attempt']}: fixing errors: {error_msgs}")

    return corrected


def main():
    print("=" * 50)
    print("  LoopSpec v2 Demo — Self-Correcting Loop")
    print("=" * 50)

    # Set up validation rules
    validator = Validator()
    validator.add_type_check(list)
    validator.add_custom(
        name="correct_length",
        check_fn=lambda output, ctx: isinstance(output, list) and len(output) == 5,
        message="Output must have exactly 5 elements.",
    )
    validator.add_custom(
        name="is_sorted",
        check_fn=lambda output, ctx: isinstance(output, list) and output == sorted(output),
        message="Output must be sorted in ascending order.",
    )

    # Create and run the correction loop
    loop = CorrectionLoop(
        max_retries=5,
        validator=validator,
        on_correction=correction_handler,
    )

    result = loop.run(
        task_fn=number_generator,
        initial_input={"count": 5, "attempt": 1},
        anchor_name="demo_start",
    )

    # Print results
    print(f"\n{'=' * 50}")
    print(f"  Result: {'✅ SUCCESS' if result['success'] else '❌ FAILED'}")
    print(f"  Output: {result['output']}")
    print(f"  Iterations: {result['iterations']}")
    print(f"{'=' * 50}")

    # Print metrics
    loop.metrics.print_summary()

    # Export metrics
    loop.metrics.export_json(".loopspec/demo_metrics.json")
    print("  📄 Metrics exported to .loopspec/demo_metrics.json")


if __name__ == "__main__":
    main()