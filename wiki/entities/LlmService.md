---
title: "LLMService"
type: entity
tags: [service, llm, backend]
sources: []
last_updated: 2026-04-08
---

## Description
Backend service module handling LLM API calls, response parsing, and story continuation logic. Contains continue_story(), continue_story_streaming(), and _prepare_story_continuation() functions.

## Key Functions
- continue_story(): Non-streaming story continuation
- continue_story_streaming(): Streaming story continuation
- _prepare_story_continuation(): Shared preparation helper used by both paths
- get_agent_for_input(): Agent selection with last_ai_response parameter
- parse_structured_response(): JSON response parsing

## Test Coverage
- [[LLM Service Context Extraction Tests]]
- [[LLMResponse Object TDD Tests]]
- [[Gemini Response Validation Tests]]
