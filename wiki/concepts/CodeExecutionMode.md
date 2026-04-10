---
title: "Code Execution Mode"
type: concept
tags: [gemini, code-execution, structured-response]
sources: []
last_updated: 2026-04-08
---

## Summary
A Gemini API mode where the model can execute code and return both code output (stdout, artifacts) and a structured JSON response. Common in dice rolling scenarios where code outputs dice roll results first (array), then the main narrative response follows (object).

## Key Characteristics
- Code executes on Gemini's server
- Output can include whitespace, stdout, or arrays before JSON
- The JSON parsing must handle mixed output patterns

## Related
- [[parse_structured_response]] — function that handles this mode
- [[StructuredResponseParsing]] — broader concept
