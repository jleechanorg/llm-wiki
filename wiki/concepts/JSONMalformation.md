---
title: "JSON Malformation"
type: concept
tags: [json, error-handling, testing]
sources: ["main-user-scenario-fix-god-mode-json"]
last_updated: 2026-04-08
---

Types of JSON malformation that can occur in AI-generated responses:

1. **Missing closing brace** — JSON string ends without final `}`
2. **Invalid JSON syntax** — missing commas between fields, unclosed strings
3. **Truncated response** — response cut off mid-sentence or mid-field

## Test Scenarios Covered
- Missing brace after valid-looking JSON
- Missing comma between object fields
- Cut-off response mid-sentence

## Expected Behavior
All malformed JSON should return standardized error message, never raw JSON structure.

## Related Concepts
- [[ParseStructuredResponse]] — handles malformed JSON gracefully
