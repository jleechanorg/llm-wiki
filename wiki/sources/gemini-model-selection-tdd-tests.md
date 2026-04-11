---
title: "Gemini Model Selection TDD Tests"
type: source
tags: [python, testing, tdd, gemini, model-selection, user-preferences]
source_file: "raw/test_gemini_model_selection.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Red-Green TDD test suite validating that both `continue_story()` and `get_initial_story()` respect user model preferences. Tests verify the user_id parameter flows through to `_select_provider_and_model()` to apply user's preferred Gemini model via `GEMINI_MODEL_MAPPING`.

## Key Claims
- **continue_story() accepts user_id**: The function now accepts user_id parameter and uses `_select_model_for_user()` helper to select appropriate model
- **User preferences respected**: User's `gemini_model` setting is properly read and applied via `GEMINI_MODEL_MAPPING`
- **get_initial_story() baseline**: Already correctly uses user's model preference via `_select_provider_and_model()`
- **Test mode guard bypass**: In test mode (`TESTING_AUTH_BYPASS=true`), the function has a guard that returns default model — tests patch to simulate user preferences

## Key Test Cases
| Test | Scenario | Expected |
|------|----------|----------|
| test_continue_story_respects_user_model_preference | User selects Gemini 2.0 Flash | API called with gemini-2.0-flash |
| test_get_initial_story_respects_user_model_preference | User selects Gemini 2.0 Flash | API called with gemini-2.0-flash |

## Connections
- [[StructuredResponse]] — JSON narrative format used in responses
- [[LLM-FirstStateManagement]] — state updates via structured JSON, not regex
- [[JSONParsingFallback]] — previous fallback pattern now removed

## Contradictions
- None identified
