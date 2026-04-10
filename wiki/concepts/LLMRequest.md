---
title: "LLMRequest"
type: concept
tags: [python, llm, request, class]
sources: [llm-request-validation-tests]
last_updated: 2026-04-08
---

## Definition
Python class that constructs and validates requests to LLM APIs (primarily Gemini). Handles type checking, field validation, and payload size limits.

## Key Attributes
- `user_action`: User's input text
- `game_mode`: Game mode (character, story, etc.)
- `user_id`: User identifier
- `game_state`: Dictionary of game state
- `story_history`: List of story entries
- `core_memories`: List of string memories

## Validation Rules
- user_id and game_mode cannot be empty or whitespace-only
- game_state must be a dict
- story_history must be a list
- core_memories must be a list of strings
- user_action and checkpoint_block limited by MAX_STRING_LENGTH
- Total payload limited by MAX_PAYLOAD_SIZE

## Related Concepts
- [[ValidationError]] — raised on field validation failures
- [[PayloadTooLargeError]] — raised on oversized payloads
- [[Type Safety]] — enforced through type checking
