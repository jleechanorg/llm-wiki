---
title: "Input Field Translation Validation Tests"
type: source
tags: [python, testing, integration, frontend, backend, translation-layer]
source_file: "raw/test_input_field_translation.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite validating input field translation between frontend → main.py → world_logic.py architectural layers. Tests ensure the bidirectional field mapping works correctly: frontend sends `{"input": "..."}`, main.py extracts and translates to `{"user_input": "..."}` for MCP protocol, and world_logic.py correctly receives via `KEY_USER_INPUT = "user_input"`.

## Key Claims
- **Frontend sends "input" field**: Frontend requests use `{"input": "..."}` key for user messages
- **main.py translates to "user_input"**: Translation layer converts `input` → `user_input` for MCP protocol
- **Legacy compatibility**: main.py supports both `input` (preferred) and `user_input` (legacy) keys
- **world_logic.py expects "user_input"**: MCP handler receives user input via `KEY_USER_INPUT = "user_input"`
- **Bidirectional field mapping**: Tests validate both forward (frontend→MCP) and backward (legacy fallback) flows

## Key Quotes
> "Frontend sends: {\"input\": \"...\"} → main.py receives: data.get(\"input\") with KEY_USER_INPUT = \"input\"} → main.py sends to MCP: {\"user_input\": \"...\"} → world_logic.py receives: request_data.get(\"user_input\") with KEY_USER_INPUT = \"user_input\"}"

## Connections
- [[main.py]] — Flask application entry point handling HTTP request translation
- [[world_logic.py]] — MCP protocol handler receiving translated field names
- [[Input Field Translation]] — Concept describing the field mapping layer

## Contradictions
- None detected — tests validate consistency between layers
