"""Tests for LoopSpec v2 MetricsTracker."""

import json
import tempfile
from pathlib import Path
from loopspec.core.metrics import MetricsTracker


def test_record_and_summary():
    m = MetricsTracker()
    m.start_iteration()
    m.record(iteration=1, passed=True, error_count=0)
    m.start_iteration()
    m.record(iteration=2, passed=False, error_count=2)

    assert m.total_iterations == 2
    assert m.success_rate == 0.5


def test_export_json():
    m = MetricsTracker()
    m.start_iteration()
    m.record(iteration=1, passed=True)

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        m.export_json(f.name)
        data = json.loads(Path(f.name).read_text())
        assert data["summary"]["total_iterations"] == 1
        assert len(data["iterations"]) == 1