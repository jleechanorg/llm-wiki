---
title: "json_schema"
type: concept
tags: [api, structured-output, schema]
sources: []
last_updated: 2026-04-08
---

## Description
json_schema is a structured output format for LLM API calls that allows developers to specify a JSON schema defining the expected response structure. Unlike legacy `json_object`, json_schema provides explicit schema validation and supports the `strict:false` option allowing dynamic choice keys in planning_block structures.

## Key Properties
- **strict:false**: Allows dynamic/variable keys in the schema (e.g., planning_block with variable choice keys)
- **schema definition**: Includes properties like narrative, planning_block, entities_mentioned, state_updates, turn_summary, debug_info, god_mode_response

## Use Cases
- Structured narrative generation with planning_block
- Entity and state tracking in game narratives
- Debug information inclusion in responses
- God mode response routing

## Connections
- [[json_object]] — legacy format without schema validation
- [[NarrativeResponse]] — specific schema for narrative generation
- [[CerebrasProvider]] — provider supporting json_schema format
