---
title: "TDD Tests for Cerebras json_schema with strict:false support"
type: source
tags: [python, testing, tdd, cerebras, json-schema, provider]
source_file: "raw/test_cerebras_json_schema.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest and pytest test suite validating Cerebras provider's json_schema support with `strict:false` configuration. Tests cover payload format, schema echo detection, nested wrapper unwrapping, and structured JSON responses across Qwen-3, GLM-4.6, and Llama-3.3 models.

## Key Claims
- **json_schema Payload**: Uses json_schema format (not legacy json_object) with strict:false to allow dynamic choice keys in planning_block
- **Schema Echo Detection**: Detects when API returns schema config instead of actual content via CerebrasSchemaEchoError
- **Nested Wrapper Unwrap**: Extracts content from `{"json": {...}}` wrapper structures
- **Model Compatibility**: Qwen-3, GLM-4.6, and Llama-3.3 all return valid structured JSON responses

## Test Coverage
- `test_uses_json_schema_format_in_payload`: Validates request uses json_schema with strict:false
- `test_json_schema_has_narrative_response_structure`: Validates NarrativeResponse fields (narrative, planning_block, entities_mentioned, state_updates, turn_summary, debug_info, god_mode_response)
- `test_detects_schema_echo_response`: Validates CerebrasSchemaEchoError detection for schema config returned as content
- `test_nested_wrapper_unwrap`: Validates content extraction from nested json wrapper
- `test_valid_json_schema_response_qwen3`: Validates Qwen-3 returns valid structured JSON
- `test_valid_json_schema_response_glm46`: Validates GLM-4.6 returns valid structured JSON
- `test_valid_json_schema_response_llama33`: Validates Llama-3.3 returns valid structured JSON

## Connections
- [[CerebrasProvider]] — provider being tested
- [[CerebrasSchemaEchoError]] — error type for schema echo detection
- [[NarrativeResponse]] — response structure schema
