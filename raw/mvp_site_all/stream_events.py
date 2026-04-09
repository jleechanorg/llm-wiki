"""Shared StreamEvent type for SSE streaming.

This module exists to avoid circular imports between:
- mvp_site.streaming_orchestrator (defines streaming flows)
- mvp_site.llm_service (streaming LLM orchestration)

Both need StreamEvent, but streaming_orchestrator also imports llm_service, so
StreamEvent must live in a small dependency leaf.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from mvp_site.serialization import json_default_serializer


@dataclass
class StreamEvent:
    """Represents a Server-Sent Event for streaming responses."""

    type: str
    payload: dict[str, Any] = field(default_factory=dict)

    def to_sse(self) -> str:
        data = json.dumps(
            {"type": self.type, "payload": self.payload},
            default=json_default_serializer,
        )
        return f"data: {data}\n\n"

    def to_dict(self) -> dict[str, Any]:
        return {"type": self.type, "payload": self.payload}

