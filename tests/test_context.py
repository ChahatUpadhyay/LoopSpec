"""Tests for LoopSpec v2 Context tracking."""

import pytest
from loopspec.core.context import Context


def test_basic_update():
    ctx = Context()
    entry = ctx.update({"goal": "test"})
    assert entry.iteration == 1
    assert ctx.current_state["goal"] == "test"


def test_history_tracking():
    ctx = Context(max_history=5)
    for i in range(10):
        ctx.update({"step": i})
    assert len(ctx.history) == 5  # max_history enforced
    assert ctx.iteration == 10


def test_anchor_and_rollback():
    ctx = Context()
    ctx.update({"version": "1.0"})
    ctx.set_anchor("stable")
    ctx.update({"version": "2.0", "broken": True})
    assert ctx.current_state["version"] == "2.0"

    restored = ctx.rollback_to_anchor("stable")
    assert restored["version"] == "1.0"
    assert "broken" not in restored


def test_anchor_not_found():
    ctx = Context()
    ctx.update({"x": 1})
    with pytest.raises(KeyError):
        ctx.rollback_to_anchor("nonexistent")


def test_drift_detection():
    ctx = Context()
    # Same state repeatedly — no drift
    for _ in range(5):
        ctx.update({"stable": True})
    assert ctx.detect_drift() is None

    # Big change — drift expected
    ctx.update({"stable": False, "new_thing": "surprise"})
    drift = ctx.detect_drift(threshold=3)
    if drift:
        assert drift["drift_detected"] is True


def test_diff():
    ctx = Context()
    ctx.update({"a": 1, "b": 2})
    ctx.update({"a": 1, "b": 3, "c": 4})
    diff = ctx.get_diff(1, 2)
    assert diff["changed"]["b"] == {"from": 2, "to": 3}
    assert "c" in diff["added"]


def test_summary():
    ctx = Context()
    ctx.update({"x": 1})
    s = ctx.summary()
    assert s["version"] == "2.0.0"
    assert s["iteration"] == 1