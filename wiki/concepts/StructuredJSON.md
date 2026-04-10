---
title: "Structured JSON"
type: concept
tags: [json, serialization, api, data-format]
sources: [llm-request-class-gemini-api.md]
last_updated: 2026-04-08
---

## Definition
A JSON data structure sent directly to an API as native JSON (not converted to concatenated strings), preserving the original data types of dict, list, and other structured types.

## Usage in This Project
The LLMRequest class uses structured JSON to send game state data directly to Gemini API, avoiding the previous json_input_schema approach that converted JSON back to strings.

## Related Concepts
- [[JSON Parsing Utilities]] — parsing JSON from LLM responses
- [[Runtime-generated Pydantic Models]] — dynamic JSON schema handling
