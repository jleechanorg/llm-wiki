---
title: "Code Block Parsing"
type: concept
tags: [json, parsing, markdown, extraction]
sources: [json-mode-preference-tests]
last_updated: 2026-04-08
---

## Definition
The JSON extraction logic handles two markdown code block formats: explicit ```json blocks and generic ``` code blocks containing JSON.

## Key Properties
- **Language-agnostic**: Works with ```json and plain ```
- **Nested extraction**: Parses narrative, entities_mentioned, and state_updates from JSON
- **Error handling**: Malformed JSON triggers error response rather than fallback

## Related Concepts
- [[JSON Mode]] — the higher-level parsing mode
- [[Safer JSON Cleanup]] — preserving narrative with JSON-like characters
