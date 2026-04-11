---
title: "LLMRequest Class for Structured JSON Input to Gemini API"
type: source
tags: [gemini-api, json-serialization, api-client, request-handling]
source_file: "raw/llm-request-class-gemini-api.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python dataclass that replaces the flawed json_input_schema approach which converted JSON back to concatenated strings. Provides structured JSON sent directly to Gemini API without string conversion, preserving data types and enabling larger payload handling.

## Key Claims
- **Structured JSON Over Concatenation**: Sends actual JSON to Gemini API rather than concatenated strings, preserving dict and list types
- **Payload Size Increase**: Increased to 10MB limit for Gemini 2.5 Flash (supports up to 500MB input natively)
- **Flat JSON Structure**: No nested "context" wrapper — fields sent directly at top level
- **Validation-First Design**: Custom exception hierarchy for validation and payload size errors
- **Similar Pattern to GeminiResponse**: Mirrors the response class pattern for request handling

## Key Classes
- `LLMRequestError` — base exception with HTTP status code
- `PayloadTooLargeError` — raised when JSON exceeds 10MB or 1MB string limits
- `ValidationError` — raised when required fields fail validation (user_id, game_mode, user_action)

## Key Fields
- `user_action`, `game_mode`, `user_id` — core identification
- `game_state`, `story_history`, `entity_tracking` — structured game data
- `core_memories`, `selected_prompts`, `sequence_ids` — context fields
- `system_corrections` — LLM self-correction protocol for server-detected discrepancies
- `character_prompt`, `generate_companions`, `world_data` — story generation fields

## Connections
- [[Gemini Code Execution Evidence Helpers]] — related Gemini API integration
- [[Gemini Explicit Cache Manager]] — related caching for Gemini API
- [[Runtime-generated Pydantic Models]] — dynamic model generation pattern

## Contradictions
- None identified
