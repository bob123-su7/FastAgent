#!/usr/bin/env python3
"""Run the local, deterministic FastAgent evaluation example."""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from fastagent_eval import load_tasks, run_evaluation


def demo_agent(prompt: str) -> str:
    """A local agent with fixed responses; it never calls a model or network."""
    responses = {
        "Return exactly: FastAgent": "FastAgent",
        "Describe FastAgent": "FastAgent evaluation demo",
        "Return an unsafe status": "error: not approved",
    }
    return responses[prompt]


def main() -> None:
    """Load demo tasks, evaluate the agent, and print a readable summary."""
    tasks = load_tasks(PROJECT_ROOT / "evals" / "demo_tasks.jsonl")
    run = run_evaluation(demo_agent, tasks)

    print("FastAgent Evaluation")
    print("====================")
    print()
    for result in run.task_results:
        marker = "[PASS]" if result.passed else "[FAIL]"
        print(f"{marker} {result.task_id}")
    print()
    print(f"Passed: {run.summary.passed} / {run.summary.total}")
    print(f"Pass rate: {run.summary.pass_rate:.1%}")


if __name__ == "__main__":
    main()
