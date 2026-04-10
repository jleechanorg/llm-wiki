---
title: "mvp_site.llm_service"
type: entity
tags: [python-module, model-selection]
sources: []
last_updated: 2026-04-08
---

Module containing the centralized model selection logic for the MVP site. Exports `DEFAULT_MODEL`, `TEST_MODEL`, and `_select_model_for_user` function.

## Key Functions
- `_select_model_for_user(user_id)`: Returns appropriate model based on user settings or defaults
- `get_user_settings(user_id)`: Retrieves user preferences from database (mocked in tests)

## Constants
- `DEFAULT_MODEL`: Fallback model when no user or invalid preference (gemini-3-flash-preview)
- `TEST_MODEL`: Model used in test environments

## Related
- [[TDD Tests for Centralized Model Selection]] — source tests
- [[Gemini]] — LLM provider
