"""Schemas and validation for evaluation tasks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


_ALLOWED_TASK_FIELDS = {
    "id",
    "input",
    "expected",
    "expected_contains",
    "forbidden_contains",
}


class TaskValidationError(ValueError):
    """Raised when an evaluation task does not match the supported schema."""


@dataclass(frozen=True)
class EvaluationTask:
    """One prompt and its deterministic expectations."""

    id: str
    input: str
    expected: str | None = None
    expected_contains: tuple[str, ...] = ()
    forbidden_contains: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "EvaluationTask":
        """Validate a JSON-compatible mapping and create an evaluation task."""
        if not isinstance(data, Mapping):
            raise TaskValidationError("Task must be a JSON object.")
        unknown_fields = set(data) - _ALLOWED_TASK_FIELDS
        if unknown_fields:
            fields = ", ".join(sorted(unknown_fields))
            raise TaskValidationError(f"Task has unsupported field(s): {fields}.")

        task_id = _required_string(data, "id")
        prompt = _required_string(data, "input")
        expected = _optional_string(data, "expected")
        expected_contains = _string_list(data, "expected_contains")
        forbidden_contains = _string_list(data, "forbidden_contains")
        if expected is None and not expected_contains and not forbidden_contains:
            raise TaskValidationError(
                "Task must configure at least one grader: 'expected', "
                "non-empty 'expected_contains', or non-empty 'forbidden_contains'."
            )

        return cls(
            id=task_id,
            input=prompt,
            expected=expected,
            expected_contains=expected_contains,
            forbidden_contains=forbidden_contains,
        )


def _required_string(data: Mapping[str, Any], field: str) -> str:
    if field not in data:
        raise TaskValidationError(f"Task is missing required field '{field}'.")
    value = data[field]
    if not isinstance(value, str) or not value:
        raise TaskValidationError(f"Task field '{field}' must be a non-empty string.")
    return value


def _optional_string(data: Mapping[str, Any], field: str) -> str | None:
    if field not in data:
        return None
    value = data[field]
    if not isinstance(value, str):
        raise TaskValidationError(f"Task field '{field}' must be a string.")
    return value


def _string_list(data: Mapping[str, Any], field: str) -> tuple[str, ...]:
    if field not in data:
        return ()
    value = data[field]
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise TaskValidationError(f"Task field '{field}' must be a list of strings.")
    return tuple(value)
