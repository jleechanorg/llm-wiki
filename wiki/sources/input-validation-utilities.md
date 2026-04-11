---
title: "Input Validation Utilities"
type: source
tags: [validation, security, input-sanitization, production, utilities]
source_file: "raw/input-validation-utilities.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python utility functions for validating and sanitizing user input in production environments. Provides UUID/format validation for campaign and user IDs, string sanitization with Unicode normalization, and request/array size limits to prevent abuse.

## Key Claims
- **UUID format validation**: Validates campaign and user IDs against UUID pattern or alphanumeric with dash/underscore (max 128 chars)
- **String sanitization**: Removes null bytes, truncates to max length, applies NFC Unicode normalization
- **Request size validation**: Validates JSON payload size against configurable limit (default 1MB)
- **Array size validation**: Enforces maximum array element count (default 1000)
- **Export format validation**: Supports txt, pdf, json, docx formats

## Key Functions
- `validate_campaign_id(campaign_id: str) -> bool`
- `validate_user_id(user_id: str) -> bool`
- `sanitize_string(value: str, max_length: int) -> str`
- `sanitize_user_input(value: str) -> str`
- `validate_request_size(data: Any, max_size: int) -> bool`
- `validate_array_size(arr: list, max_size: int) -> bool`
- `validate_export_format(export_format: str) -> bool`

## Connections
- [[InputValidationUtilities]] — this module
- Related to: [[RequestSizeValidation]] — request payload limits
- Related to: [[StringSanitization]] — input sanitization patterns

## Contradictions
- None identified
