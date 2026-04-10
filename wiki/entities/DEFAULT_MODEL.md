---
title: "DEFAULT_MODEL"
type: entity
tags: [constant, model, fallback]
sources: []
last_updated: 2026-04-08
---

Constant defining the fallback LLM model used when no user is specified or user preference is invalid. Current value: gemini-3-flash-preview.

## Usage
- Returned when `user_id` is None
- Returned when user settings database call fails (returns None)
- Returned when user has invalid model preference

## Related
- [[mvp_site.llm_service]] — module defining this constant
- [[TEST_MODEL]] — test environment equivalent
- [[TDD Tests for Centralized Model Selection]] — validation tests
