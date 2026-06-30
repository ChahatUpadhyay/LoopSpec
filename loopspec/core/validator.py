"""
Validation engine for LoopSpec v2.

Runs configurable validation rules against outputs to determine
if a correction iteration succeeded or needs retry.
"""

import re
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class ValidationResult:
    """Result of a single validation check."""
    rule_name: str
    passed: bool
    message: str
    severity: str = "error"  # "error", "warning", "info"
    details: Optional[Dict[str, Any]] = None


@dataclass
class ValidationReport:
    """Aggregated validation results."""
    results: List[ValidationResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        """True if all error-severity rules passed."""
        return all(r.passed for r in self.results if r.severity == "error")

    @property
    def warnings(self) -> List[ValidationResult]:
        return [r for r in self.results if r.severity == "warning" and not r.passed]

    @property
    def errors(self) -> List[ValidationResult]:
        return [r for r in self.results if r.severity == "error" and not r.passed]

    def summary(self) -> Dict[str, Any]:
        return {
            "passed": self.passed,
            "total_checks": len(self.results),
            "errors": len(self.errors),
            "warnings": len(self.warnings),
            "details": [
                {"rule": r.rule_name, "passed": r.passed, "severity": r.severity, "message": r.message}
                for r in self.results
            ],
        }


class Validator:
    """
    Configurable validation engine.

    Register rules as callables. Each rule receives the output and context,
    and returns a ValidationResult.
    """

    def __init__(self):
        self._rules: List[Dict[str, Any]] = []

    def add_rule(
        self,
        name: str,
        check_fn: Callable[[Any, Dict[str, Any]], bool],
        message: str = "",
        severity: str = "error",
    ) -> "Validator":
        """
        Register a validation rule.

        Args:
            name: Human-readable rule name.
            check_fn: Callable(output, context_state) -> bool. True = passed.
            message: Failure message.
            severity: "error" (blocks), "warning" (logs), or "info".

        Returns:
            self for chaining.
        """
        self._rules.append({
            "name": name,
            "check_fn": check_fn,
            "message": message,
            "severity": severity,
        })
        return self

    def add_not_empty(self, field_name: str = "output") -> "Validator":
        """Built-in rule: output must not be empty."""
        return self.add_rule(
            name=f"{field_name}_not_empty",
            check_fn=lambda output, ctx: bool(output),
            message=f"{field_name} must not be empty.",
        )

    def add_type_check(self, expected_type: type, field_name: str = "output") -> "Validator":
        """Built-in rule: output must be of expected type."""
        return self.add_rule(
            name=f"{field_name}_type_check",
            check_fn=lambda output, ctx: isinstance(output, expected_type),
            message=f"{field_name} must be of type {expected_type.__name__}.",
        )

    def add_contains(self, substring: str, field_name: str = "output") -> "Validator":
        """Built-in rule: string output must contain a substring."""
        return self.add_rule(
            name=f"{field_name}_contains_{substring}",
            check_fn=lambda output, ctx: isinstance(output, str) and substring in output,
            message=f"{field_name} must contain '{substring}'.",
        )

    def add_max_length(self, max_len: int, field_name: str = "output") -> "Validator":
        """Built-in rule: output length must not exceed max_len."""
        return self.add_rule(
            name=f"{field_name}_max_length",
            check_fn=lambda output, ctx: hasattr(output, "__len__") and len(output) <= max_len,
            message=f"{field_name} must not exceed {max_len} in length.",
        )

    def add_pattern(self, pattern: str, field_name: str = "output") -> "Validator":
        """Built-in rule: string output must match a regex pattern."""
        return self.add_rule(
            name=f"{field_name}_pattern_{pattern}",
            check_fn=lambda output, ctx: isinstance(output, str) and bool(re.search(pattern, output)),
            message=f"{field_name} must match pattern '{pattern}'.",
        )

    def add_custom(
        self,
        name: str,
        check_fn: Callable[[Any, Dict[str, Any]], bool],
        message: str = "Custom validation failed.",
        severity: str = "error",
    ) -> "Validator":
        """Add a fully custom validation rule."""
        return self.add_rule(name=name, check_fn=check_fn, message=message, severity=severity)

    def validate(self, output: Any, context_state: Optional[Dict[str, Any]] = None) -> ValidationReport:
        """
        Run all registered rules against the output.

        Args:
            output: The output to validate.
            context_state: The current context state dict.

        Returns:
            A ValidationReport with all results.
        """
        context_state = context_state or {}
        report = ValidationReport()

        for rule in self._rules:
            try:
                passed = rule["check_fn"](output, context_state)
            except Exception as e:
                passed = False
                rule["message"] = f"Rule raised exception: {e}"

            report.results.append(ValidationResult(
                rule_name=rule["name"],
                passed=passed,
                message=rule["message"] if not passed else "OK",
                severity=rule["severity"],
            ))

        return report