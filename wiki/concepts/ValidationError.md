---
title: "ValidationError"
type: concept
tags: [python, exception, validation]
sources: [llm-request-validation-tests]
last_updated: 2026-04-08
---

## Definition
Exception raised when field validation fails in LLMRequest. Indicates invalid input that violates defined constraints.

## Causes
- Empty or whitespace-only user_id
- Empty or whitespace-only game_mode
- Wrong type for game_state (must be dict)
- Wrong type for story_history (must be list)
- Wrong type for core_memories (must be list)
- Non-string items in core_memories array
- String exceeding MAX_STRING_LENGTH

## Related Concepts
- [[LLMRequest]] — class that raises this error
- [[PayloadTooLargeError]] — related exception for size limits
- [[Type Safety]] — concept being enforced
