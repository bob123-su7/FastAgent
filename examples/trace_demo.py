#!/usr/bin/env python3
"""Run a local, deterministic trace recording example."""

from pathlib import Path
import sys
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from fastagent_trace import TraceEvent, TraceRecorder


def main() -> None:
    """Record a fixed workflow and export its events to a temporary JSONL file."""
    trace_id = "demo-trace-001"
    recorder = TraceRecorder(trace_id=trace_id)
    events = [
        TraceEvent(trace_id, "agent_start", "agent", "started"),
        TraceEvent(
            trace_id,
            "calculator_call",
            "tool_call",
            "started",
            parent_step_id="agent_start",
            tool_name="calculator",
        ),
        TraceEvent(
            trace_id,
            "calculator_result",
            "tool_result",
            "success",
            parent_step_id="calculator_call",
            tool_name="calculator",
            duration_ms=1.0,
            metadata={"result": 4},
        ),
        TraceEvent(trace_id, "agent_end", "agent", "success", parent_step_id="agent_start"),
    ]
    for event in events:
        recorder.record(event)

    print(f"Trace: {trace_id}")
    for event in recorder.events:
        tool = f" tool={event.tool_name}" if event.tool_name else ""
        print(f"- {event.step_id}: {event.event_type} ({event.status}){tool}")

    with TemporaryDirectory() as temp_dir:
        output_path = Path(temp_dir) / "trace.jsonl"
        recorder.write_jsonl(output_path)
        print(f"Exported {len(output_path.read_text(encoding='utf-8').splitlines())} JSONL events.")


if __name__ == "__main__":
    main()
