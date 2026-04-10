---
title: "Gemini Response Metadata Logging"
type: concept
tags: [logging, gemini, debugging]
sources: [log-gemini-response-metadata-tests]
last_updated: 2026-04-08
---

Log message prefix `GEMINI_RESPONSE_META` used in `_log_gemini_response_metadata` function. Provides debugging information for Gemini API responses including:

- finish_reason
- candidate_index (for multi-candidate responses)
- text_length extraction status
- safety_ratings

## Log Levels
- INFO: Normal response completion
- WARNING: Non-STOP or UNKNOWN finish_reason
- DEBUG: Extraction failures
