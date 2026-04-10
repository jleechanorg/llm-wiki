---
title: "StreamEvent"
type: concept
tags: [streaming, events, dataclass, sse]
sources: []
last_updated: 2026-04-08
---

## Definition
A Python dataclass representing individual events in an SSE streaming response. Contains type and payload fields, with methods for SSE formatting and dictionary conversion.

## Attributes
- **type**: Event type (chunk, done, error, state)
- **payload**: Dictionary containing event data (text, sequence, full_narrative, etc.)

## Methods
- `to_sse()` — Converts event to SSE format: `data: {\"type\": \"chunk\", \"payload\": {...}}\n\n`
- `to_dict()` — Converts event to dictionary representation

## Usage
```python
event = StreamEvent(type="chunk", payload={"text": "Hello", "sequence": 0})
sse = event.to_sse()  # "data: {\"type\": \"chunk\", ...}\n\n"
```

## Related Concepts
- [[StreamingOrchestrator]] — Module that creates StreamEvent instances
- [[ServerSentEvents]] — Protocol for transmitting events

## Connections
- Tested by [[StreamingOrchestratorModuleTests]]
