"""
Metrics tracking for LoopSpec v2.

Records iteration outcomes, timing, validation results, and drift events
to provide observability into the correction loop's effectiveness.
"""

import time
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from pathlib import Path


@dataclass
class IterationMetric:
    """Metrics for a single correction iteration."""
    iteration: int
    timestamp: float
    duration_ms: float
    passed: bool
    error_count: int
    warning_count: int
    drift_detected: bool
    correction_applied: bool
    metadata: Dict[str, Any] = field(default_factory=dict)


class MetricsTracker:
    """
    Collects and reports metrics across all correction loop iterations.

    Tracks success rates, average retries, drift frequency, and timing
    to help you understand how well the protocol is performing.
    """

    def __init__(self):
        self._metrics: List[IterationMetric] = []
        self._start_time: Optional[float] = None

    def start_iteration(self) -> None:
        """Mark the start of a new iteration for timing."""
        self._start_time = time.time()

    def record(
        self,
        iteration: int,
        passed: bool,
        error_count: int = 0,
        warning_count: int = 0,
        drift_detected: bool = False,
        correction_applied: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> IterationMetric:
        """Record the outcome of a correction iteration."""
        end_time = time.time()
        duration_ms = (end_time - (self._start_time or end_time)) * 1000

        metric = IterationMetric(
            iteration=iteration,
            timestamp=end_time,
            duration_ms=round(duration_ms, 2),
            passed=passed,
            error_count=error_count,
            warning_count=warning_count,
            drift_detected=drift_detected,
            correction_applied=correction_applied,
            metadata=metadata or {},
        )
        self._metrics.append(metric)
        self._start_time = None
        return metric

    @property
    def total_iterations(self) -> int:
        return len(self._metrics)

    @property
    def success_rate(self) -> float:
        if not self._metrics:
            return 0.0
        return sum(1 for m in self._metrics if m.passed) / len(self._metrics)

    @property
    def average_duration_ms(self) -> float:
        if not self._metrics:
            return 0.0
        return sum(m.duration_ms for m in self._metrics) / len(self._metrics)

    @property
    def drift_count(self) -> int:
        return sum(1 for m in self._metrics if m.drift_detected)

    @property
    def correction_count(self) -> int:
        return sum(1 for m in self._metrics if m.correction_applied)

    def summary(self) -> Dict[str, Any]:
        """Return an aggregate summary of all tracked metrics."""
        return {
            "total_iterations": self.total_iterations,
            "success_rate": round(self.success_rate, 4),
            "average_duration_ms": round(self.average_duration_ms, 2),
            "drift_events": self.drift_count,
            "corrections_applied": self.correction_count,
            "total_errors": sum(m.error_count for m in self._metrics),
            "total_warnings": sum(m.warning_count for m in self._metrics),
        }

    def export_json(self, path: str) -> None:
        """Export all metrics to a JSON file."""
        data = {
            "summary": self.summary(),
            "iterations": [
                {
                    "iteration": m.iteration,
                    "timestamp": m.timestamp,
                    "duration_ms": m.duration_ms,
                    "passed": m.passed,
                    "error_count": m.error_count,
                    "warning_count": m.warning_count,
                    "drift_detected": m.drift_detected,
                    "correction_applied": m.correction_applied,
                    "metadata": m.metadata,
                }
                for m in self._metrics
            ],
        }
        Path(path).write_text(json.dumps(data, indent=2))

    def print_summary(self) -> None:
        """Print a human-readable summary to stdout."""
        s = self.summary()
        print("\n╔══════════════════════════════════════╗")
        print("║       LoopSpec v2 Metrics Report     ║")
        print("╠══════════════════════════════════════╣")
        print(f"║  Iterations:    {s['total_iterations']:>18}  ║")
        print(f"║  Success Rate:  {s['success_rate']*100:>17.1f}%  ║")
        print(f"║  Avg Duration:  {s['average_duration_ms']:>15.1f}ms  ║")
        print(f"║  Drift Events:  {s['drift_events']:>18}  ║")
        print(f"║  Corrections:   {s['corrections_applied']:>18}  ║")
        print(f"║  Total Errors:  {s['total_errors']:>18}  ║")
        print(f"║  Total Warns:   {s['total_warnings']:>18}  ║")
        print("╚══════════════════════════════════════╝\n")