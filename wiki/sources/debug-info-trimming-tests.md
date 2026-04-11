---
title: "Debug Info Trimming Tests"
type: source
tags: [python, testing, logging, storage, optimization, debug]
source_file: "raw/test_debug_info_trimming.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating that debug_info no longer stores bloated fields like system_instruction_text, raw_request_payload, and raw_response_text, while preserving lightweight metadata fields. Tests verify storage savings through conditional ellipsis logging and accurate length reporting.

## Key Claims
- **Bloated Field Removal**: debug_info no longer requires system_instruction_text, raw_request_payload, or raw_response_text
- **Lightweight Fields Preserved**: llm_provider, llm_model, system_instruction_files, system_instruction_char_count remain
- **Conditional Ellipsis**: Logging adds "..." only when string exceeds preview limit (2000 chars)
- **Accurate Length Reporting**: RAW_REQUEST and RAW_RESPONSE logs capture actual length before truncation
- **Storage Savings**: Trimmed debug_info reduces per-entry storage from ~36KB to lightweight metadata

## Key Quotes
> "These fields should NOT be required in debug_info"

## Connections
- [[NarrativeResponse]] — the response schema being tested
- [[DebugInfo]] — the metadata field being trimmed
- [[StorageOptimization]] — the goal of reducing debug_info bloat
- [[LLMService]] — where debug logging and truncation occurs

## Contradictions
- None
