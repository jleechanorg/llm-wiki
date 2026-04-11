---
title: "LLMResponse Structured Fields Parsing Tests"
type: source
tags: [python, testing, json, parsing, pydantic]
source_file: "raw/test_llm_response_structured_fields.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating LLMResponse parsing of structured fields from raw JSON responses. Tests cover parsing when all structured fields are present (session_header, planning_block with choices, dice_rolls, resources, action_resolution, debug_info) and when some fields are missing.

## Key Claims
- **Full structured field parsing**: LLMResponse.create() parses all structured fields from JSON when present
- **Partial field parsing**: Parser handles missing fields gracefully without raising errors
- **Choices dict normalization**: _choices_by_id helper normalizes choices from both dict and list formats
- **Session header parsing**: session_header extracted with format "Session N: Title\\nClass | HP: X/Y"
- **Planning block parsing**: planning_block.thinking and planning_block.choices extracted as dict

## Key Quotes
> "Verify LLMResponse has the structured_response"

## Connections
- [[LLMResponse]] — class being tested
- [[NarrativeResponse]] — Pydantic schema for structured response

## Contradictions
- None identified
