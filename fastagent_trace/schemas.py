"""Schema and validation for explicit trace events."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from typing import Any


_VALID_STATUSES = {"started", "success", "error", "denied", "cancelled"}


class TraceValidationError(ValueError):
    """Raised when a trace event does not meet the supported contract."""


@dataclass(frozen=True)
class TraceEvent:
    """One explicit, JSON-serializable event from an agent execution."""

    trace_id: str
    step_id: str
    event_type: str
    status: str
    parent_step_id: str | None = None
    tool_name: str | None = None
    duration_ms: float | None = None
    error_code: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_empty_string(self.trace_id, "trace_id")
        _require_non_empty_string(self.step_id, "step_id")
        _require_non_empty_string(self.event_type, "event_type")
        _validate_optional_string(self.parent_step_id, "parent_step_id")
        _validate_optional_string(self.tool_name, "tool_name")
        _validate_optional_string(self.error_code, "error_code")

        if not isinstance(self.status, str) or self.status not in _VALID_STATUSES:
            allowed = ", ".join(sorted(_VALID_STATUSES))
            raise TraceValidationError(
                f"status must be one of: {allowed}; got {self.status!r}."
            )
        if self.duration_ms is not None:
            if isinstance(self.duration_ms, bool) or not isinstance(
                self.duration_ms, (int, float)
            ):
                raise TraceValidationError("duration_ms must be a number when provided.")
            if not math.isfinite(self.duration_ms) or self.duration_ms < 0:
                raise TraceValidationError("duration_ms must be a finite number greater than or equal to 0.")
        if not isinstance(self.metadata, dict) or not all(
            isinstance(key, str) for key in self.metadata
        ):
            raise TraceValidationError("metadata must be a dictionary with string keys.")

        try:
            serialized_metadata = json.dumps(self.metadata, allow_nan=False)
        except (TypeError, ValueError) as error:
            raise TraceValidationError("metadata must contain JSON-compatible values.") from error
        object.__setattr__(self, "metadata", json.loads(serialized_metadata))

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-friendly copy of this event."""
        return {
            "trace_id": self.trace_id,
            "step_id": self.step_id,
            "event_type": self.event_type,
            "status": self.status,
            "parent_step_id": self.parent_step_id,
            "tool_name": self.tool_name,
            "duration_ms": self.duration_ms,
            "error_code": self.error_code,
            "metadata": json.loads(json.dumps(self.metadata, allow_nan=False)),
        }


def _require_non_empty_string(value: object, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise TraceValidationError(f"{field_name} must be a non-empty string.")


def _validate_optional_string(value: object, field_name: str) -> None:
    if value is not None and (not isinstance(value, str) or not value.strip()):
        raise TraceValidationError(f"{field_name} must be a non-empty string when provided.")
