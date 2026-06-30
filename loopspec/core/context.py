"""
Context tracking for LoopSpec v2.

Maintains a rolling context window with history, drift detection,
and state snapshots so the correction loop knows what changed and why.
"""

import time
import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from collections import deque


@dataclass
class ContextEntry:
    """A single context snapshot."""
    timestamp: float
    iteration: int
    state: Dict[str, Any]
    fingerprint: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class Context:
    """
    Tracks the evolving state of an AI development session.

    Maintains a history of context snapshots, detects drift between
    iterations, and provides rollback capabilities.
    """

    def __init__(self, max_history: int = 100):
        self.max_history = max_history
        self._history: deque[ContextEntry] = deque(maxlen=max_history)
        self._current_state: Dict[str, Any] = {}
        self._iteration: int = 0
        self._anchors: Dict[str, ContextEntry] = {}

    @property
    def iteration(self) -> int:
        return self._iteration

    @property
    def current_state(self) -> Dict[str, Any]:
        return self._current_state.copy()

    @property
    def history(self) -> List[ContextEntry]:
        return list(self._history)

    def _compute_fingerprint(self, state: Dict[str, Any]) -> str:
        """Create a hash fingerprint of the current state for drift detection."""
        serialized = json.dumps(state, sort_keys=True, default=str)
        return hashlib.sha256(serialized.encode()).hexdigest()[:16]

    def update(self, state: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> ContextEntry:
        """
        Record a new context snapshot.

        Args:
            state: The current state dict (goals, constraints, outputs, etc.)
            metadata: Optional metadata (source, confidence, etc.)

        Returns:
            The created ContextEntry.
        """
        self._iteration += 1
        self._current_state.update(state)

        entry = ContextEntry(
            timestamp=time.time(),
            iteration=self._iteration,
            state=self._current_state.copy(),
            fingerprint=self._compute_fingerprint(self._current_state),
            metadata=metadata or {},
        )
        self._history.append(entry)
        return entry

    def set_anchor(self, name: str) -> ContextEntry:
        """
        Save the current state as a named anchor for rollback.

        Anchors are like "known good" checkpoints. If the AI drifts,
        the correction loop can roll back to an anchor.
        """
        if not self._history:
            raise ValueError("No context history to anchor. Call update() first.")
        entry = self._history[-1]
        self._anchors[name] = entry
        return entry

    def rollback_to_anchor(self, name: str) -> Dict[str, Any]:
        """Restore state to a previously saved anchor."""
        if name not in self._anchors:
            raise KeyError(f"Anchor '{name}' not found. Available: {list(self._anchors.keys())}")
        anchor = self._anchors[name]
        self._current_state = anchor.state.copy()
        return self._current_state

    def detect_drift(self, threshold: int = 3) -> Optional[Dict[str, Any]]:
        """
        Detect if the context has drifted significantly from recent history.

        Compares the current fingerprint against the last `threshold` entries.
        If the fingerprint hasn't appeared in recent history, drift is detected.

        Returns:
            A drift report dict if drift detected, None otherwise.
        """
        if len(self._history) < threshold + 1:
            return None

        current_fp = self._compute_fingerprint(self._current_state)
        recent_fps = [e.fingerprint for e in list(self._history)[-threshold - 1:-1]]

        if current_fp not in recent_fps:
            return {
                "drift_detected": True,
                "current_fingerprint": current_fp,
                "recent_fingerprints": recent_fps,
                "iteration": self._iteration,
                "suggestion": "Context has diverged from recent history. Consider rollback or re-anchoring.",
            }
        return None

    def get_diff(self, iteration_a: int, iteration_b: int) -> Dict[str, Any]:
        """Compare two iterations and return what changed."""
        entries = {e.iteration: e for e in self._history}

        if iteration_a not in entries or iteration_b not in entries:
            raise ValueError(f"Iteration(s) not found in history.")

        state_a = entries[iteration_a].state
        state_b = entries[iteration_b].state

        added = {k: state_b[k] for k in state_b if k not in state_a}
        removed = {k: state_a[k] for k in state_a if k not in state_b}
        changed = {
            k: {"from": state_a[k], "to": state_b[k]}
            for k in state_a
            if k in state_b and state_a[k] != state_b[k]
        }

        return {"added": added, "removed": removed, "changed": changed}

    def summary(self) -> Dict[str, Any]:
        """Return a summary of the current context state."""
        return {
            "version": "2.0.0",
            "iteration": self._iteration,
            "history_size": len(self._history),
            "anchors": list(self._anchors.keys()),
            "current_fingerprint": self._compute_fingerprint(self._current_state),
            "current_state_keys": list(self._current_state.keys()),
        }