"""Tests for the local trace recorder MVP."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from fastagent_trace import TraceEvent, TraceRecorder, TraceValidationError


class TraceEventTests(unittest.TestCase):
    def test_valid_event_creation(self) -> None:
        event = TraceEvent("trace-1", "step-1", "agent", "started", metadata={"attempt": 1})

        self.assertEqual(event.trace_id, "trace-1")
        self.assertEqual(event.metadata, {"attempt": 1})

    def test_empty_required_fields_are_rejected(self) -> None:
        for field_name in ("trace_id", "step_id", "event_type"):
            values = {"trace_id": "trace", "step_id": "step", "event_type": "agent"}
            values[field_name] = ""
            with self.subTest(field_name=field_name):
                with self.assertRaisesRegex(TraceValidationError, field_name):
                    TraceEvent(status="started", **values)

    def test_invalid_status_is_rejected(self) -> None:
        with self.assertRaisesRegex(TraceValidationError, "status must be one of"):
            TraceEvent("trace", "step", "agent", "pending")
        with self.assertRaisesRegex(TraceValidationError, "status must be one of"):
            TraceEvent("trace", "step", "agent", [])  # type: ignore[arg-type]

    def test_negative_duration_is_rejected(self) -> None:
        with self.assertRaisesRegex(TraceValidationError, "duration_ms"):
            TraceEvent("trace", "step", "agent", "success", duration_ms=-0.1)

    def test_non_json_metadata_is_rejected(self) -> None:
        with self.assertRaisesRegex(TraceValidationError, "JSON-compatible"):
            TraceEvent("trace", "step", "agent", "started", metadata={"bad": {1, 2}})

    def test_to_dict_is_json_serializable(self) -> None:
        event = TraceEvent("trace", "step", "tool_result", "success", metadata={"items": [1, 2]})

        self.assertEqual(json.loads(json.dumps(event.to_dict())), event.to_dict())


class TraceRecorderTests(unittest.TestCase):
    def test_recorder_preserves_order_and_trace_id(self) -> None:
        recorder = TraceRecorder(trace_id="trace-1")
        first = TraceEvent("trace-1", "start", "agent", "started")
        second = TraceEvent("trace-1", "end", "agent", "success")

        recorder.record(first)
        recorder.record(second)

        self.assertEqual([event.step_id for event in recorder.events], ["start", "end"])
        self.assertEqual({event.trace_id for event in recorder.events}, {"trace-1"})
        self.assertIsInstance(recorder.events, tuple)

    def test_recorder_rejects_another_trace_id_when_configured(self) -> None:
        recorder = TraceRecorder(trace_id="trace-1")

        with self.assertRaisesRegex(ValueError, "does not match"):
            recorder.record(TraceEvent("trace-2", "step", "agent", "started"))

    def test_write_jsonl_preserves_order(self) -> None:
        recorder = TraceRecorder()
        recorder.record(TraceEvent("trace", "first", "agent", "started"))
        recorder.record(TraceEvent("trace", "second", "agent", "success"))

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "trace.jsonl"
            recorder.write_jsonl(output_path)
            lines = output_path.read_text(encoding="utf-8").splitlines()

        self.assertEqual(len(lines), 2)
        self.assertEqual([json.loads(line)["step_id"] for line in lines], ["first", "second"])
