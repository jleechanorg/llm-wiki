---
title: "JSON Cleanup"
type: concept
tags: [json, parsing, error-handling]
sources: []
last_updated: 2026-04-08
---

## Summary
Techniques for handling malformed or corrupted JSON in LLM responses. The narrative_response_schema.py module includes legacy cleanup code (lines 500-557) that attempts to extract usable content from broken JSON strings.

## Key Techniques
- **Aggressive cleanup**: Removes severely malformed JSON structure
- **Artifact removal**: Strips embedded JSON markers like `"narrative":` from text
- **Whitespace normalization**: Normalizes excessive spaces and newlines
- **Fallback parsing**: Attempts minimal extraction when full JSON parsing fails

## Related
- [[NarrativeResponse]] — The target schema that JSON is parsed into
- [[parseStructuredResponse]] — Function that performs JSON parsing and cleanup
