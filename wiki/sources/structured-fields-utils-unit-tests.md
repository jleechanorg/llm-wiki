---
title: "Structured Fields Utils Unit Tests"
type: source
tags: [testing, python, unit-test, structured-data, mock]
source_file: "raw/structured-fields-utils-unit-tests.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests for `structured_fields_utils.extract_structured_fields` function. Tests validate extraction of session_header, planning_block, dice_rolls, resources, and debug_info from LLMResponse objects with structured_response attributes.


## Key Claims
- **Full Data Extraction**: extract_structured_fields correctly extracts all structured fields when present
- **Empty Field Handling**: Function returns empty strings/lists/dicts for empty fields while maintaining key presence
- **Missing Attribute Tolerance**: Function handles cases where structured_response lacks certain attributes

## Key Quotes
> "mock_gemini_response.structured_response = self.mock_structured_response"

## Connections
- [[StructuredFieldsUtils]] — module under test
- [[LLMResponse]] — response object containing structured_response
- [[NarrativeResponse]] — schema for structured response data

## Contradictions
- None identified
