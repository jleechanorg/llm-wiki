---
title: "Structured Fields Parsing"
type: concept
tags: [json, parsing, structured-data]
sources: [llm-response-structured-fields-parsing-tests]
last_updated: 2026-04-08
---

## Overview
Structured fields parsing refers to the process of extracting typed fields from JSON responses rather than relying on regex or string matching. The LLMResponse class uses Pydantic models (NarrativeResponse) to validate and parse structured data.

## Key Patterns
- **JSON-first parsing**: Raw response parsed as JSON before any text extraction
- **Pydantic validation**: NarrativeResponse schema validates structure
- **Graceful degradation**: Missing fields result in default/None values rather than errors
- **Choice normalization**: _choices_by_id helper handles both dict and list choice formats

## Related Pages
- [[LLMResponse]] — implements structured parsing
- [[NarrativeResponse]] — schema definition
