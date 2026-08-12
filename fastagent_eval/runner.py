"""Load JSONL evaluation tasks and run deterministic checks against an agent."""

from __future__ import annotations

import json
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .graders import contains_all, contains_none, exact_match
from .schemas import EvaluationTask, TaskValidationError

AgentFunction = Callable[[str], str]


@dataclass(frozen=True)
class TaskResult:
    """The output and configured grader outcomes for one task."""

    task_id: str
    passed: bool
    output: str
    checks: dict[str, bool]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""
        return {
            "task_id": self.task_id,
            "passed": self.passed,
            "output": self.output,
            "checks": self.checks,
        }


@dataclass(frozen=True)
class EvaluationSummary:
    """Aggregate counts for one evaluation run."""

    total: int
    passed: int
    failed: int
    pass_rate: float

    def to_dict(self) -> dict[str, int | float]:
        """Return a JSON-serializable representation."""
        return {
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "pass_rate": self.pass_rate,
        }


@dataclass(frozen=True)
class EvaluationRunResult:
    """Per-task results and their aggregate summary."""

    task_results: tuple[TaskResult, ...]
    summary: EvaluationSummary

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""
        return {
            "results": [result.to_dict() for result in self.task_results],
            "summary": self.summary.to_dict(),
        }


def load_tasks(path: str | Path) -> list[EvaluationTask]:
    """Load and validate evaluation tasks from a JSONL file.

    Blank lines are ignored. Invalid JSON and invalid task fields name the
    source line so malformed suites are never silently skipped.
    """
    tasks: list[EvaluationTask] = []
    task_path = Path(path)

    with task_path.open(encoding="utf-8") as task_file:
        for line_number, raw_line in enumerate(task_file, start=1):
            if not raw_line.strip():
                continue
            try:
                data = json.loads(raw_line)
            except json.JSONDecodeError as error:
                raise TaskValidationError(
                    f"Invalid JSON in {task_path} line {line_number}: {error.msg}"
                ) from error
            try:
                tasks.append(EvaluationTask.from_dict(data))
            except TaskValidationError as error:
                raise TaskValidationError(
                    f"Invalid task in {task_path} line {line_number}: {error}"
                ) from error

    return tasks


def run_evaluation(
    agent_fn: AgentFunction, tasks: Iterable[EvaluationTask]
) -> EvaluationRunResult:
    """Run an ``agent_fn(prompt: str) -> str`` against tasks in order."""
    results: list[TaskResult] = []

    for task in tasks:
        output = agent_fn(task.input)
        if not isinstance(output, str):
            raise TypeError(
                f"Agent output for task '{task.id}' must be a string, got {type(output).__name__}."
            )
        checks = _grade(task, output)
        results.append(
            TaskResult(
                task_id=task.id,
                passed=all(checks.values()),
                output=output,
                checks=checks,
            )
        )

    passed = sum(result.passed for result in results)
    total = len(results)
    summary = EvaluationSummary(
        total=total,
        passed=passed,
        failed=total - passed,
        pass_rate=passed / total if total else 0.0,
    )
    return EvaluationRunResult(task_results=tuple(results), summary=summary)


def _grade(task: EvaluationTask, output: str) -> dict[str, bool]:
    checks: dict[str, bool] = {}
    if task.expected is not None:
        checks["exact"] = exact_match(output, task.expected)
    if task.expected_contains:
        checks["expected_contains"] = contains_all(output, task.expected_contains)
    if task.forbidden_contains:
        checks["forbidden_contains"] = contains_none(output, task.forbidden_contains)
    return checks
