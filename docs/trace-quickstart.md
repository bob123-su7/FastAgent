# FastAgent Trace Quickstart

## Why trace an agent?

An agent's final answer does not show how it reached that answer. A trace records
the ordered execution events—such as an agent step or tool result—so people and
future evaluation code can inspect what happened. Unlike a free-form log, each
event has a small, validated schema and can be exported consistently.

This MVP is local and explicit: the caller creates and records each event. It
does not automatically inspect prompts, tool arguments, environment variables,
or credentials.

## TraceEvent fields

`TraceEvent` requires `trace_id`, `step_id`, `event_type`, and a status from
`started`, `success`, `error`, `denied`, or `cancelled`. Optional fields are
`parent_step_id`, `tool_name`, `duration_ms`, `error_code`, and `metadata`.

`duration_ms` must be zero or greater. `metadata` must be a dictionary with
string keys and JSON-compatible values. Provide metadata deliberately; do not
record API keys, tokens, passwords, complete prompts, tool arguments, or
unauthorized personal data.

## Record events

```python
from fastagent_trace import TraceEvent, TraceRecorder

recorder = TraceRecorder(trace_id="run-001")
recorder.record(TraceEvent("run-001", "agent_start", "agent", "started"))
recorder.record(
    TraceEvent(
        "run-001",
        "calculator_result",
        "tool_result",
        "success",
        tool_name="calculator",
        duration_ms=1.2,
        metadata={"result": 4},
    )
)
```

`recorder.events` returns an immutable tuple in record order. `event.to_dict()`
and `recorder.to_dict()` return JSON-friendly data.

## Export JSONL

```python
recorder.write_jsonl("trace.jsonl")
```

The output uses UTF-8 and contains one stable JSON object per event line, in the
same order the events were recorded.

## Run the demo and tests

```bash
python3 examples/trace_demo.py
python3 -m unittest discover -s tests -v
```

## Current boundaries

This is not a telemetry platform. It does not implement OpenTelemetry, LangSmith,
cloud telemetry, dashboards, databases, provider integrations, LLM SDK hooks,
automatic instrumentation, distributed tracing, token or cost collection,
multi-agent graphs, async tracing, or tool-use evaluation.
