# LLM Schema Non-Compliance Investigation

**Date:** 2026-02-17
**Bead:** REV-ofgqm
**Branch:** schema_followup

## Executive Summary

LLM is failing to produce valid JSON schema at concerning rates:
- **schema_validation_real_api**: 50% raw pass rate (5/10 scenarios failed)
- **schema_validation_extended**: 0% raw pass rate (5/5 scenarios failed)

The test suite shows 100% pass rates AFTER post-processing, but this masks significant raw LLM failures.

## Raw Failure Details

### schema_validation_real_api (50% raw failures)

| Scenario | Error |
|----------|-------|
| Update resources (gold, hit_dice) | "Raw response is not a JSON object" |
| Update spell slots | "RAW: resources is missing but expected" |
| Update experience | "Raw response is not a JSON object" |
| Update death saves | "Raw response is not a JSON object" |
| Social HP Challenge | "Raw response is not a JSON object" |

### schema_validation_extended (100% raw failures)

| Scenario | Error |
|----------|-------|
| Successful spell slot usage | "Raw response is not a JSON object" |
| Equip item from inventory | "RAW: equipment is missing but expected" |
| Use consumable item | "RAW: resources is missing but expected" |
| Level up | "core_memories: {'append': ...} is not of type 'array'" |
| Spend hero points | "Raw response is not a JSON object" |

## Root Cause Categories

1. **JSON Prefix Issue**: LLM returns `[Mode: STORY MODE]` prefix before JSON, causing parser to see `[` at start
2. **JSON Structure Errors (50%+)**: LLM returns array `[` instead of object `{`
3. **Missing Required Fields**: Resources, equipment fields not included in state_updates
4. **Type Errors**: Using `{"append": "string"}` instead of array methods for core_memories

## HTTP Payload Analysis

### Request Configuration
- **responseMimeType**: `application/json` (set correctly)
- **responseSchema**: NOT SET (missing - no schema provided to guide LLM)
- **temperature**: 0.9
- **maxOutputTokens**: 50000

### Issue Found: Mode Prefix in Response
The LLM is outputting `[Mode: STORY MODE]` as a prefix before the JSON response:
```
[Mode: STORY MODE]
{
  "session_header": ...
  ...
}
```

This prefix causes the JSON parser to see `[` at the start and incorrectly interpret the response as an array instead of an object.

### System Instruction
- **Length**: 259,429 characters (extremely long)
- **Contains**: Full JSON schema reference, D&D rules, dice instructions, resource tracking format
- **Issue**: No explicit instruction to NOT include prefix text before JSON output

## Root Cause: Bug in JSON Prefix Handling

### FIX APPLIED (2026-02-17)
Fixed in `mvp_site/narrative_response_schema.py` (lines 3678-3687):
- Added regex to detect and strip `[Mode: ...]` prefixes BEFORE bracket detection
- Pattern: `r"^\[Mode:\s*[^\]]+\]\s*"` matches mode prefixes like `[Mode: STORY MODE]`

### Previous Bug Behavior
The code in `narrative_response_schema.py` (lines 3683-3710) had recovery logic to strip prefixes before JSON, but it **incorrectly treated `[Mode: STORY MODE]` as a JSON array**.

When LLM returned:
```
[Mode: STORY MODE]
{
  "session_header": ...
}
```

The parser:
1. Found `[` at position 0 (from `[Mode:`)
2. Found `{` at position ~20
3. Since bracket_pos (0) < brace_pos (20), it tried to find matching `]` for the "array"
4. But `[Mode: STORY MODE]` is NOT a JSON array - it's just text with brackets
5. The matching logic failed, and JSON parsing failed

**This was a bug in the JSON recovery logic** - it should recognize `[Mode:` as a text prefix, not a JSON array.

## Evidence Locations

- `/tmp/worldarchitectai/schema_followup/schema_validation_real_api/latest/`
- `/tmp/worldarchitectai/schema_followup/schema_validation_extended/latest/`

## Next Steps

1. Inspect raw HTTP payloads sent to LLM
2. Identify instruction conflicts in prompts
3. Fix prompt instructions to enforce JSON object output
4. Add explicit schema examples to reduce ambiguity
