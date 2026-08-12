# FastAgent Evaluation Quickstart

## Why evaluate agents?

An agent that looks correct in one chat can still fail on the next input. A fixed
task suite makes expected behavior explicit and gives changes a repeatable pass
rate. This MVP is deliberately small: it evaluates a Python function locally,
with no model provider, API key, network call, or paid usage.

## What this MVP includes

The evaluation flow is:

```text
JSONL tasks -> agent_fn(prompt: str) -> deterministic graders -> results + summary
```

The runner is framework-agnostic. It only needs a callable with this contract:

```python
def agent_fn(prompt: str) -> str:
    return "agent output"
```

## Write tasks in JSONL

Use one JSON object per line. `id` and `input` are required; all expectation
fields are optional.

```json
{"id": "basic_001", "input": "Return exactly: FastAgent", "expected": "FastAgent"}
{"id": "basic_002", "input": "Describe FastAgent", "expected_contains": ["FastAgent", "Agent"]}
{"id": "basic_003", "input": "Return a status", "forbidden_contains": ["error", "failed"]}
```

Invalid JSON or task fields raise a clear `TaskValidationError` with the file
and line number. Blank lines are ignored.

## Deterministic graders

- `expected` uses exact match after stripping leading and trailing whitespace.
  Matching remains case-sensitive and internal whitespace is unchanged.
- `expected_contains` requires every configured string to occur in the output.
- `forbidden_contains` fails when any configured string occurs in the output.

When a task configures more than one grader, all configured checks must pass.
Each result records its individual checks along with the final `passed` value.

## Run the demo

From the repository root:

```bash
python3 examples/eval_demo.py
```

The demo agent is a local dictionary lookup. It intentionally has one failing
task so the output shows both PASS and FAIL plus the calculated pass rate.

## Use the runner

```python
from fastagent_eval import load_tasks, run_evaluation


def my_agent(prompt: str) -> str:
    return prompt


tasks = load_tasks("evals/demo_tasks.jsonl")
run = run_evaluation(my_agent, tasks)
print(run.summary.to_dict())
```

`run.task_results` contains per-task `task_id`, `output`, `passed`, and
`checks`. Both individual results and summaries provide `to_dict()` methods for
JSON-friendly serialization.

## Run tests

```bash
python3 -m unittest discover -s tests -v
```

## Current boundaries and future work

This MVP evaluates only text input and text output, synchronously and in task
order. It does not evaluate tool use, traces, latency, token or cost metrics,
LLM-as-a-Judge scoring, or safety and permission behavior. Those are possible
future extensions once a project needs them.
