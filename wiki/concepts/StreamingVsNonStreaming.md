---
title: "Streaming vs Non-Streaming Paths"
type: concept
tags: [architecture, streaming, llm]
sources: []
last_updated: 2026-04-08
---

## Description
Architectural pattern where both streaming and non-streaming code paths share the same preparation logic via _prepare_story_continuation(). This ensures consistency in agent selection, token calculation, and system instructions.

## Phase 1 Contract
Both paths must:
1. Call _prepare_story_continuation() for preparation
2. Use prepared.agent.requires_action_resolution in parse path
3. Emit tool_start/tool_result/state events when tools are requested

## Related Tests
- [[LLM Service Context Extraction Tests]]
- test_continue_story_streaming_uses_shared_preparation_helper
