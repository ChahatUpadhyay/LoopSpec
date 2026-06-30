"""Tests for LoopSpec v2 CorrectionLoop."""

from loopspec import CorrectionLoop, Validator


def test_immediate_success():
    """Task passes on first try — no correction needed."""
    v = Validator().add_not_empty()
    loop = CorrectionLoop(max_retries=3, validator=v)
    result = loop.run(lambda inp: "good output", initial_input={})
    assert result["success"]
    assert result["iterations"] == 1


def test_correction_on_failure():
    """Task fails first, correction handler fixes it, succeeds on retry."""
    call_count = {"n": 0}

    def task(inp):
        call_count["n"] += 1
        if call_count["n"] < 3:
            return ""  # empty = fails not_empty check
        return "fixed"

    def corrector(ctx):
        return ctx["previous_input"]

    v = Validator().add_not_empty()
    loop = CorrectionLoop(max_retries=5, validator=v, on_correction=corrector)
    result = loop.run(task, initial_input={})
    assert result["success"]
    assert result["iterations"] == 3


def test_exhausted_retries():
    """Task always fails — should exhaust retries and report failure."""
    v = Validator().add_not_empty()
    loop = CorrectionLoop(max_retries=2, validator=v, on_correction=lambda c: c["previous_input"])
    result = loop.run(lambda inp: "", initial_input={})
    assert not result["success"]
    assert result["iterations"] == 2


def test_exception_handling():
    """Task raises an exception — loop should catch and retry."""
    call_count = {"n": 0}

    def task(inp):
        call_count["n"] += 1
        if call_count["n"] == 1:
            raise ValueError("boom")
        return "recovered"

    v = Validator().add_not_empty()
    loop = CorrectionLoop(max_retries=3, validator=v, on_correction=lambda c: c["previous_input"])
    result = loop.run(task, initial_input={})
    assert result["success"]


def test_metrics_tracked():
    """Metrics should be recorded for each iteration."""
    v = Validator().add_not_empty()
    loop = CorrectionLoop(max_retries=3, validator=v)
    loop.run(lambda inp: "ok", initial_input={})
    assert loop.metrics.total_iterations == 1
    assert loop.metrics.success_rate == 1.0