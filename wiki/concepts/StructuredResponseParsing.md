---
title: "Structured Response Parsing"
type: concept
tags: [json, parsing, api, gemini]
sources: []
last_updated: 2026-04-08
---

## Summary
Pattern where LLM APIs return JSON-structured responses that must be parsed from potentially mixed output. Critical when code execution mode is used, as whitespace, stdout, or other artifacts may precede the actual JSON.

## Key Techniques
- Whitespace stripping before JSON detection
- Prefer JSON object { over array [ for main response
- Error recovery for malformed JSON prefixes

## Related
- [[CodeExecutionMode]] — produces artifacts requiring this parsing
- [[parse_structured_response]] — implementation in mvp_site.narrative_response_schema
