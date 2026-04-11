---
title: "TDD Tests for Centralized Model Selection"
type: source
tags: [python, testing, tdd, model-selection, unittest]
source_file: "raw/mvp_site_all/test_centralized_model_selection.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest test suite validating that model selection is centralized through `_select_model_for_user` function, respecting user preferences and falling back to defaults appropriately. Tests cover five scenarios: base case (no user), valid preference, invalid preference, test model integration, and database error handling.

## Key Claims
- **Base Case**: No user_id returns DEFAULT_MODEL (gemini-3-flash-preview)
- **Valid Preference**: User's valid gemini_model preference (e.g., gemini-2.0-flash) is respected when test mode env vars are disabled
- **Invalid Fallback**: Invalid model preference falls back to DEFAULT_MODEL
- **Test Model Integration**: TEST_MODEL equals DEFAULT_MODEL (gemini-3-flash-preview as of Dec 2025)
- **Error Handling**: Database errors (None return) fall back to DEFAULT_MODEL

## Test Coverage
- `test_no_user_id_returns_default_model`: Validates base case fallback
- `test_valid_user_preference_is_respected`: Validates preference respecting with env var mocking
- `test_invalid_user_preference_falls_back_to_default`: Validates invalid model fallback
- `test_test_model_supports_code_execution`: Integration test verifying TEST_MODEL/DEFAULT_MODEL alignment
- `test_database_error_falls_back_to_default`: Error handling validation

## Key Quotes
> "FAIL: No user_id should return DEFAULT_MODEL ({DEFAULT_MODEL}), but got {result}" — test assertion message

> "Note: Must disable ALL test mode environment variables to allow user preferences." — critical test setup requirement

## Connections
- [[mvp_site.llm_service]] — module containing the model selection logic
- [[Gemini]] — the LLM provider being tested
- [[DEFAULT_MODEL]] — constant fallback value
- [[TEST_MODEL]] — test environment model constant

## Contradictions
- []
