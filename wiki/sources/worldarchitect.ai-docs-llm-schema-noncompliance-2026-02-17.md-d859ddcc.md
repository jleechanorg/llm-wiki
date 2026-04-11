---
title: "LLM Schema Non-Compliance Investigation"
type: source
tags: [schema-validation, llm-json, worldarchitect.ai, debugging, json-parsing, prompt-engineering]
sources: []
date: 2026-02-17
last_updated: 2026-04-07
---

## Summary

Investigation into LLM failing to produce valid JSON schema at concerning rates. Found 50% raw failure rate in `schema_validation_real_api` and 100% raw failure rate in `schema_validation_extended` scenarios. Root cause identified as `[Mode: STORY MODE]` prefix being incorrectly parsed as a JSON array instead of text prefix.

## Key Claims

- **50% Raw Failure Rate**: `schema_validation_real_api` had 5/10 scenarios fail with JSON parsing errors
- **100% Raw Failure Rate**: `schema_validation_extended` had all 5 scenarios fail
- **Root Cause Identified**: `[Mode: STORY MODE]` prefix before JSON causing parser to see array instead of object
- **Bug in JSON Recovery Logic**: Code incorrectly treated text prefix as JSON array bracket
- **Fix Applied**: Added regex to detect and strip `[Mode: ...]` prefixes BEFORE bracket detection

## Key Quotes

> "The code in `narrative_response_schema.py` (lines 3683-3710) had recovery logic to strip prefixes before JSON, but it **incorrectly treated `[Mode: STORY MODE]` as a JSON array**."

> "When LLM returned `[Mode: STORY MODE]` followed by `{`, the parser found `[` at position 0 and `{` at position ~20, incorrectly interpreting it as an array."

## Root Cause Categories

1. **JSON Prefix Issue**: LLM returns `[Mode: STORY MODE]` prefix before JSON, causing parser to see `[` at start
2. **JSON Structure Errors (50%+)**: LLM returns array `[` instead of object `{`
3. **Missing Required Fields**: Resources, equipment fields not included in state_updates
4. **Type Errors**: Using `{"append": "string"}` instead of array methods for core_memories

## Fix Details

**Location**: `mvp_site/narrative_response_schema.py` (lines 3678-3687)

**Pattern Added**: `r"^\[Mode:\s*[^\]]+\]\s*"` matches mode prefixes like `[Mode: STORY MODE]`

**Behavior Change**: Regex now detects and strips `[Mode: ...]` prefixes BEFORE bracket detection logic runs.

## Next Steps

1. Inspect raw HTTP payloads sent to LLM
2. Identify instruction conflicts in prompts
3. Fix prompt instructions to enforce JSON object output
4. Add explicit schema examples to reduce ambiguity

## Connections

- Related to [[Streaming Flows E2E Test]] — streaming responses with JSON payloads
- Related to [[Claude Code System Prompt]] — system instructions influence JSON output
- Connects to schema validation issues in other test documents

## Contradictions

- Post-processing achieves 100% pass rate, masking significant raw LLM failures — this suggests the fix is workarounds, not addressing root cause in LLM prompting
