"""Tests for LoopSpec v2 Validator."""

from loopspec.core.validator import Validator


def test_not_empty_pass():
    v = Validator().add_not_empty()
    report = v.validate("hello")
    assert report.passed


def test_not_empty_fail():
    v = Validator().add_not_empty()
    report = v.validate("")
    assert not report.passed
    assert len(report.errors) == 1


def test_type_check():
    v = Validator().add_type_check(list)
    assert v.validate([1, 2, 3]).passed
    assert not v.validate("string").passed


def test_contains():
    v = Validator().add_contains("hello")
    assert v.validate("say hello world").passed
    assert not v.validate("goodbye").passed


def test_max_length():
    v = Validator().add_max_length(5)
    assert v.validate("abc").passed
    assert not v.validate("abcdef").passed


def test_pattern():
    v = Validator().add_pattern(r"^\d+$")
    assert v.validate("12345").passed
    assert not v.validate("abc").passed


def test_custom_rule():
    v = Validator().add_custom(
        name="is_even",
        check_fn=lambda output, ctx: output % 2 == 0,
        message="Must be even.",
    )
    assert v.validate(4).passed
    assert not v.validate(3).passed


def test_multiple_rules():
    v = Validator()
    v.add_not_empty()
    v.add_type_check(str)
    v.add_contains("ok")

    report = v.validate("this is ok")
    assert report.passed

    report = v.validate("this is not")
    assert not report.passed
    assert len(report.errors) == 1


def test_warning_severity():
    v = Validator().add_rule(
        name="soft_check",
        check_fn=lambda o, c: False,
        message="Just a warning",
        severity="warning",
    )
    report = v.validate("anything")
    assert report.passed  # warnings don't block
    assert len(report.warnings) == 1