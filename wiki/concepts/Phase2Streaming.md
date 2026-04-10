---
title: "Phase 2 Streaming"
type: concept
tags: [streaming, llm, phases]
sources: []
last_updated: 2026-04-08
---

## Definition
The second phase of the two-phase story generation flow. After Phase 1 executes tool requests (like dice rolls), Phase 2 generates the narrative response. When Phase 2 returns empty chunks (no narrative generated), it triggers validation failures.

## Key Characteristics
- **Trigger**: Starts after phase_transition event with reset_text=True
- **Failure Mode**: Empty raw_response_text causes validation to fail
- **User Impact**: Frontend displays "[Error: Empty response from server]"
- **Recovery**: System must detect empty and yield error event, not done event

## Related Concepts
- [[StreamingOrchestrator]] — manages phase transitions
- [[ValidationFailure]] — occurs when response validation fails
- [[ToolExecution]] — Phase 1 executes tools before Phase 2 begins
