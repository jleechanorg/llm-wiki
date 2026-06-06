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

## Tool Configuration Parity

2026-06-06 WorldArchitect RCA: shared preparation is not sufficient when one
provider path applies tool-specific system instructions but the request config
does not attach the matching tool. The streaming Gemini path produced a
code-execution-only response while the non-streaming path attached the tool
correctly. Future streaming/non-streaming parity checks must include provider
config fields such as tools, response MIME/schema, max output, and response-part
extraction, not only agent selection and prompt assembly.

## Related Tests
- [[LLM Service Context Extraction Tests]]
- test_continue_story_streaming_uses_shared_preparation_helper
