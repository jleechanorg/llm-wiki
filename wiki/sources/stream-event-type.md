---
title: "StreamEvent Type for SSE Streaming"
type: source
tags: [python, sse, streaming, dataclass, worldarchitect]
source_file: "raw/stream-event-type.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Shared `StreamEvent` dataclass type for Server-Sent Events (SSE) streaming responses. Exists to avoid circular imports between `mvp_site.streaming_orchestrator` and `mvp_site.llm_service` modules.

## Key Claims
- **Circular Import Resolution**: StreamEvent lives in a small dependency leaf to break circular dependency between streaming_orchestrator and llm_service
- **SSE Format**: Provides `to_sse()` method for proper SSE data formatting with `data: {...}\n\n`
- **Dict Conversion**: Provides `to_dict()` method for payload access
- **JSON Serialization**: Uses custom `json_default_serializer` for dataclass serialization

## Key Code Patterns
```python
@dataclass
class StreamEvent:
    type: str
    payload: dict[str, Any] = field(default_factory=dict)
    
    def to_sse(self) -> str:
        data = json.dumps({"type": self.type, "payload": self.payload}, ...)
        return f"data: {data}\n\n"
```

## Connections
- [[StreamingOrchestrator]] — defines streaming flows, imports StreamEvent
- [[LlmService]] — streaming LLM orchestration, imports StreamEvent
- [[JsonDefaultSerializer]] — custom serializer for JSON encoding
- [[ServerSentEvents]] — the SSE protocol this type implements

## Contradictions
- None identified
