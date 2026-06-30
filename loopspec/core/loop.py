"""
CorrectionLoop — the core self-correcting execution engine for LoopSpec v2.

Takes a task callable, runs it, validates the output, and retries with
correction context if validation fails. Tracks everything via Context
and MetricsTracker.
"""

import time
from typing import Any, Callable, Dict, List, Optional

from loopspec.core.context import Context
from loopspec.core.validator import Validator, ValidationReport
from loopspec.core.metrics import MetricsTracker


class CorrectionLoop:
    """
    Self-correcting execution loop.

    Usage:
        loop = CorrectionLoop(max_retries=3)
        loop.validator.add_not_empty()
        result = loop.run(my_task_fn, initial_input={"prompt": "..."})
    """

    def __init__(
        self,
        max_retries: int = 3,
        context: Optional[Context] = None,
        validator: Optional[Validator] = None,
        metrics: Optional[MetricsTracker] = None,
        on_correction: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
    ):
        """
        Args:
            max_retries: Maximum number of correction attempts before giving up.
            context: Optional Context instance (created if not provided).
            validator: Optional Validator instance (created if not provided).
            metrics: Optional MetricsTracker instance (created if not provided).
            on_correction: Optional callback(correction_context) -> modified_input.
                          Called when validation fails, receives error details,
                          and should return a corrected input for the next attempt.
        """
        self.max_retries = max_retries
        self.context = context or Context()
        self.validator = validator or Validator()
        self.metrics = metrics or MetricsTracker()
        self.on_correction = on_correction
        self._results: List[Dict[str, Any]] = []

    def run(
        self,
        task_fn: Callable[[Dict[str, Any]], Any],
        initial_input: Dict[str, Any],
        anchor_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Execute the task with self-correction.

        Args:
            task_fn: Callable that takes an input dict and returns output.
            initial_input: The initial input to the task.
            anchor_name: Optional anchor name to set before starting.

        Returns:
            A result dict with keys:
                - "success": bool
                - "output": the final output
                - "iterations": number of iterations taken
                - "validation": final ValidationReport summary
                - "metrics": MetricsTracker summary
                - "context": Context summary
        """
        current_input = initial_input.copy()

        # Record initial context
        self.context.update(
            {"phase": "init", "input": current_input},
            metadata={"source": "correction_loop"},
        )

        if anchor_name:
            self.context.set_anchor(anchor_name)

        final_output = None
        final_report = None

        for attempt in range(1, self.max_retries + 1):
            self.metrics.start_iteration()

            # Check for drift
            drift = self.context.detect_drift()
            drift_detected = drift is not None

            # Execute the task
            try:
                output = task_fn(current_input)
            except Exception as e:
                # Task itself raised an error
                self.context.update(
                    {"phase": "error", "attempt": attempt, "error": str(e)},
                    metadata={"exception_type": type(e).__name__},
                )
                self.metrics.record(
                    iteration=attempt,
                    passed=False,
                    error_count=1,
                    drift_detected=drift_detected,
                    correction_applied=False,
                    metadata={"exception": str(e)},
                )
                # Build correction context for retry
                if self.on_correction and attempt < self.max_retries:
                    correction_ctx = {
                        "attempt": attempt,
                        "error": str(e),
                        "error_type": "exception",
                        "previous_input": current_input,
                        "context_state": self.context.current_state,
                    }
                    current_input = self.on_correction(correction_ctx)
                continue

            # Validate the output
            report = self.validator.validate(output, self.context.current_state)
            final_output = output
            final_report = report

            # Update context with results
            self.context.update(
                {
                    "phase": "validate",
                    "attempt": attempt,
                    "passed": report.passed,
                    "error_count": len(report.errors),
                },
                metadata={"validation_summary": report.summary()},
            )

            self.metrics.record(
                iteration=attempt,
                passed=report.passed,
                error_count=len(report.errors),
                warning_count=len(report.warnings),
                drift_detected=drift_detected,
                correction_applied=not report.passed and attempt < self.max_retries,
            )

            if report.passed:
                # Success
                result = {
                    "success": True,
                    "output": output,
                    "iterations": attempt,
                    "validation": report.summary(),
                    "metrics": self.metrics.summary(),
                    "context": self.context.summary(),
                }
                self._results.append(result)
                return result

            # Validation failed — build correction context
            if self.on_correction and attempt < self.max_retries:
                correction_ctx = {
                    "attempt": attempt,
                    "errors": [
                        {"rule": e.rule_name, "message": e.message}
                        for e in report.errors
                    ],
                    "warnings": [
                        {"rule": w.rule_name, "message": w.message}
                        for w in report.warnings
                    ],
                    "error_type": "validation",
                    "previous_input": current_input,
                    "previous_output": output,
                    "context_state": self.context.current_state,
                    "drift": drift,
                }
                current_input = self.on_correction(correction_ctx)

        # Exhausted all retries
        result = {
            "success": False,
            "output": final_output,
            "iterations": self.max_retries,
            "validation": final_report.summary() if final_report else {},
            "metrics": self.metrics.summary(),
            "context": self.context.summary(),
        }
        self._results.append(result)
        return result

    @property
    def results(self) -> List[Dict[str, Any]]:
        """All results from all run() calls."""
        return self._results