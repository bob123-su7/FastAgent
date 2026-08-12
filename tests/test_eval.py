"""Tests for the deterministic evaluation MVP."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from fastagent_eval.graders import contains_all, contains_none, exact_match
from fastagent_eval.runner import load_tasks, run_evaluation
from fastagent_eval.schemas import EvaluationTask, TaskValidationError


class GraderTests(unittest.TestCase):
    def test_exact_match_strips_outer_whitespace(self) -> None:
        self.assertTrue(exact_match("  FastAgent\n", "FastAgent"))

    def test_exact_match_failure(self) -> None:
        self.assertFalse(exact_match("fastagent", "FastAgent"))

    def test_expected_contains_pass_and_fail(self) -> None:
        self.assertTrue(contains_all("FastAgent evaluation", ["FastAgent", "evaluation"]))
        self.assertFalse(contains_all("FastAgent", ["FastAgent", "evaluation"]))

    def test_forbidden_contains_pass_and_fail(self) -> None:
        self.assertTrue(contains_none("FastAgent is ready", ["error", "failed"]))
        self.assertFalse(contains_none("error: failed", ["error", "failed"]))


class RunnerTests(unittest.TestCase):
    def test_multiple_graders_are_aggregated(self) -> None:
        task = EvaluationTask(
            id="combined",
            input="prompt",
            expected="FastAgent",
            expected_contains=("Fast",),
            forbidden_contains=("error",),
        )

        run = run_evaluation(lambda prompt: " FastAgent ", [task])

        result = run.task_results[0]
        self.assertTrue(result.passed)
        self.assertEqual(
            result.checks,
            {"exact": True, "expected_contains": True, "forbidden_contains": True},
        )

    def test_runner_summary(self) -> None:
        tasks = [
            EvaluationTask(id="pass", input="one", expected="one"),
            EvaluationTask(id="fail", input="two", expected="other"),
        ]

        run = run_evaluation(lambda prompt: prompt, tasks)

        self.assertEqual(run.summary.total, 2)
        self.assertEqual(run.summary.passed, 1)
        self.assertEqual(run.summary.failed, 1)
        self.assertEqual(run.summary.pass_rate, 0.5)

    def test_agent_must_return_a_string(self) -> None:
        task = EvaluationTask(id="type", input="prompt")
        with self.assertRaisesRegex(TypeError, "must be a string"):
            run_evaluation(lambda prompt: 1, [task])  # type: ignore[return-value]


class TaskLoadingTests(unittest.TestCase):
    def test_malformed_task_has_a_clear_error(self) -> None:
        with self.assertRaisesRegex(TaskValidationError, "missing required field 'input'"):
            EvaluationTask.from_dict({"id": "missing-input"})

    def test_jsonl_task_loading(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        tasks = load_tasks(project_root / "evals" / "demo_tasks.jsonl")

        self.assertEqual([task.id for task in tasks], ["basic_001", "basic_002", "basic_003"])
        self.assertEqual(tasks[0].expected, "FastAgent")
        self.assertEqual(tasks[1].expected_contains, ("FastAgent", "evaluation"))

    def test_invalid_jsonl_includes_line_number(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            task_file = Path(temp_dir) / "invalid.jsonl"
            task_file.write_text('{"id": "ok", "input": "prompt"}\nnot-json\n', encoding="utf-8")

            with self.assertRaisesRegex(TaskValidationError, r"line 2"):
                load_tasks(task_file)
