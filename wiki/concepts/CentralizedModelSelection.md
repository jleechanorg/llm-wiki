---
title: "Centralized Model Selection"
type: concept
tags: [architecture, model-routing, fallback]
sources: []
last_updated: 2026-04-08
---

Pattern where LLM model selection is handled by a single function (e.g., `_select_model_for_user`) that determines which model to use based on user settings, with appropriate fallbacks to defaults.

## Selection Logic
1. If user_id is None → use DEFAULT_MODEL
2. If user settings unavailable (database error) → use DEFAULT_MODEL
3. If user preference is invalid/unsupported → use DEFAULT_MODEL
4. If user preference is valid and test mode disabled → use user's preference
5. If test mode enabled (env vars set) → use TEST_MODEL

## Test Mode Environment Variables
- `TESTING_AUTH_BYPASS`
- `MOCK_SERVICES_MODE`
- `FORCE_TEST_MODEL`

All must be disabled for user preferences to be respected.

## Related
- [[mvp_site.llm_service]] — implementation module
- [[DEFAULT_MODEL]] — fallback constant
- [[TDD Tests for Centralized Model Selection]] — validation tests
