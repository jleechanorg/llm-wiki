---
title: "LLMRequest Validation Tests"
type: source
tags: [python, testing, validation, type-safety, llm]
source_file: "raw/test_llm_request_validation.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite validating the LLMRequest class's validation features for type safety, field validation, and error handling. Tests cover empty/whitespace input validation, type checking for game_state/story_history/core_memories, item type validation for core_memories arrays, and string/payload length limits.

## Key Claims
- **Empty user_id validation**: Empty string raises ValidationError with "user_id cannot be empty"
- **Whitespace user_id validation**: Whitespace-only user_id raises ValidationError (not treated as valid)
- **Empty game_mode validation**: Empty string raises ValidationError with "game_mode cannot be empty"
- **Type validation**: game_state must be dict, story_history must be list, core_memories must be list
- **Item type validation**: core_memories items must be strings, not numbers or other types
- **String length validation**: user_action and checkpoint_block limited by MAX_STRING_LENGTH
- **Payload size validation**: Oversized JSON payloads raise PayloadTooLargeError

## Key Quotes
> "Test that empty user_id raises ValidationError"

## Connections
- [[LLMRequest]] — class under test
- [[ValidationError]] — exception for field validation failures
- [[PayloadTooLargeError]] — exception for oversized payloads
- [[Type Safety]] — concept being validated

## Contradictions
- None detected
