---
title: "LLM Service Context Extraction Tests"
type: source
tags: [python, testing, llm-service, streaming, context]
source_file: "raw/test_llm_service_context.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite validating llm_service.py context extraction logic, focusing on continue_story() extracting the most recent AI response from story_context and streaming path sharing preparation with the non-streaming path.

## Key Claims
- **continue_story extracts last AI response correctly**: Finds the MOST RECENT entry where actor is gemini from story_context
- **Streaming shares preparation helper**: continue_story_streaming must call _prepare_story_continuation()
- **Streaming emits tool and state events**: When tool requests exist, streaming path emits tool_start/tool_result/state events
- **last_ai_response parameter**: Passed to get_agent_for_input for semantic routing

## Key Test Cases
- test_continue_story_extracts_last_ai_response: Verifies correct AI response extraction from multi-entry story_context
- test_continue_story_streaming_uses_shared_preparation_helper: Phase 1 contract validation
- test_continue_story_streaming_emits_tool_and_state_events: End-to-end streaming event emission

## Connections
- [[LLMResponse]] — response object used in tests
- [[ContinueStory]] — core function being tested
- [[StreamingVsNonStreaming]] — architectural pattern for shared preparation
