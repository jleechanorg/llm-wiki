---
title: "Log Gemini Response Metadata Tests"
type: source
tags: [python, testing, logging, gemini, bug-fix, pr-4099]
source_file: "raw/test_log_gemini_response_metadata.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test coverage for `_log_gemini_response_metadata` function in llm_service. Tests validate bug fixes from PR #4099: None finish_reason normalization to UNKNOWN with WARNING trigger, candidate_index logging for multi-candidate debugging, and graceful edge case handling.

## Key Claims
- **None finish_reason handling**: Explicitly None values should be normalized to "UNKNOWN" and trigger WARNING level (not bypass via falsy check)
- **Candidate index logging**: Log messages include candidate_index for debugging multi-candidate responses
- **Debug logging**: Text length extraction failures logged at DEBUG level
- **FinishReason enum support**: Handles both string ("STOP") and enum ("FinishReason.STOP") forms

## Key Quotes
> "This was the bug reported by Cursor and CodeRabbit - None values were bypassing the warning path due to falsy check."

## Connections
- [[PR4099]] — the PR that fixed the None finish_reason bug
- [[LogGeminiResponseMetadata]] — function under test
- [[LLMService]] — module containing the function
- [[GeminiResponseMetadata]] — log message prefix (GEMINI_RESPONSE_META)

## Contradictions
- None
