---
title: "Simplified Structured Narrative Generation Schemas"
type: source
tags: [python, schemas, json, narrative-generation, error-handling]
source_file: "raw/simplified-structured-narrative-generation-schemas.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module providing structured narrative generation schemas for WorldArchitect.AI without pydantic dependency. Implements JSON parsing utilities, error handling, boolean coercion, and validation helpers for the Milestone 0.4 Combined approach.

## Key Claims
- **No Pydantic Dependency**: Self-contained implementation using only standard library and mvp_site utilities
- **JSON Parse Error Handling**: Comprehensive error logging with context extraction around failure points
- **Standardized Error Marker**: JSON_PARSE_FALLBACK_MARKER provides single source of truth for parse failure messages
- **Threshold-Based Warning System**: Per-server-process warning escalation (INFO → WARNING → ERROR)
- **Boolean Coercion**: Shared helper for consistent truthy/falsey handling across validation and sanitization

## Key Functions
- `_log_thresholded_warning()`: Escalating warning system with warn_at/error_at thresholds
- `_log_json_parse_error()`: Full diagnostic logging for malformed JSON with context around error position
- `_coerce_bool()`: Consistent boolean coercion for truthy/falsey inputs
- `JSON_MARKDOWN_PATTERN` / `GENERIC_MARKDOWN_PATTERN`: Precompiled regex for code block extraction

## Constants
- `JSON_PARSE_FALLBACK_MARKER`: Error string returned on parse failure
- `MIN_NARRATIVE_LENGTH`: 100 characters - threshold for "suspiciously short" detection

## Connections
- [[JSONParsingUtilities]] — helper functions used here (extract_best_json, find_matching_brace)
- [[NumericConverters]] — coerce_int_safe imported from numeric_converters
- [[InputValidationUtilities]] — schema validation functions from schemas.validation
- [[MVPSite]] — parent module providing logging_util and json_utils

## Contradictions
- None identified
