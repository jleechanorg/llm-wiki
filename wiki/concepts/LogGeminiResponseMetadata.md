---
title: "_log_gemini_response_metadata"
type: concept
tags: [function, logging, gemini, llm-service]
sources: [log-gemini-response-metadata-tests]
last_updated: 2026-04-08
---

Function in `mvp_site.llm_service` module that logs Gemini API response metadata. Handles various finish_reason values including None, STOP, SAFETY, LENGTH, MAX_TOKENS, RECITATION.

## Bug Fix (PR #4099)
- **Issue**: None finish_reason values bypassed WARNING path due to Python falsy check
- **Fix**: Normalize None to "UNKNOWN" string and trigger WARNING
- **Additional**: Add candidate_index for multi-candidate debugging

## Logging Levels
- INFO: Normal STOP finish_reason
- WARNING: None (normalized to UNKNOWN), SAFETY, LENGTH, MAX_TOKENS, RECITATION
- DEBUG: Text length extraction failures
