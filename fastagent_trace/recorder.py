"""An in-memory recorder for explicitly supplied trace events."""

from __future__ import annotations

import json
from pathlib import Path

from .schemas import TraceEvent


class TraceRecorder:
    """Store trace events in call order and export them as JSONL."""

    def __init__(self, trace_id: str | None = None) -> None:
        self._trace_id = trace_id
        self._events: list[TraceEvent] = []

    @property
    def events(self) -> tuple[TraceEvent, ...]:
        """Return an immutable view of events in their recorded order."""
        return tuple(self._events)

    def record(self, event: TraceEvent) -> None:
        """Append one explicitly created event to the recorder."""
        if self._trace_id is not None and event.trace_id != self._trace_id:
            raise ValueError(
                f"Event trace_id {event.trace_id!r} does not match recorder trace_id {self._trace_id!r}."
            )
        self._events.append(event)

    def to_dict(self) -> list[dict[str, object]]:
        """Return JSON-friendly event dictionaries in recorded order."""
        return [event.to_dict() for event in self._events]

    def write_jsonl(self, path: str | Path) -> None:
        """Write one event per UTF-8 JSONL line in recorded order."""
        output_path = Path(path)
        with output_path.open("w", encoding="utf-8") as output_file:
            for event in self._events:
                output_file.write(json.dumps(event.to_dict(), sort_keys=True, allow_nan=False))
                output_file.write("\n")
