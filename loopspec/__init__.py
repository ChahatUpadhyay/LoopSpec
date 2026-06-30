"""LoopSpec v2.0 — Self-correcting, context-aware AI development protocol."""

__version__ = "2.0.0"

from loopspec.core.context import Context
from loopspec.core.loop import CorrectionLoop
from loopspec.core.validator import Validator
from loopspec.core.metrics import MetricsTracker

__all__ = ["Context", "CorrectionLoop", "Validator", "MetricsTracker"]