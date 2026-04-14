# REV: Orchestration retry doesn't pass cache_name

## Status: done
## Priority: medium
## Type: bug

## Summary

`_orchestrate_gemini_code_execution_tool_requests` accepts `cache_name` but the
`enable_faction_minigame` retry path at line ~3354 called `generate_json_mode_content`
without passing it. When cache is active, this caused an uncached retry that also sent
`system_instruction_text` (conflicting with the cached system instruction).

## Fix

Pass `cache_name` to the retry call. When `cache_name` is set, suppress
`system_instruction_text` (already in cache) to avoid the Gemini API conflict.

## Files Changed

- `mvp_site/llm_service.py`
