---
title: "End-to-end Integration Tests for Story Continuation"
type: source
tags: [python, testing, integration-testing, e2e, firestore, llm-providers, story-generation]
source_file: "raw/test_story_continuation_end2end.py"
sources: []
last_updated: 2026-04-08
---

## Summary
End-to-end integration test suite for continuing a story through the full application stack. Tests validate the complete flow from API endpoint through all service layers including context compaction, with external services (LLM provider APIs and Firestore DB) mocked at the lowest level.

## Key Claims
- **Full Stack Testing**: Tests entire request pipeline from API endpoint to Firestore persistence
- **Mock Strategy**: Mocks external services at lowest level to test real integration points
- **Context Compaction**: Validates story continuation works with context compaction enabled
- **Dual Provider Support**: Tests both Gemini and Cerebras LLM providers
- **Game State Persistence**: Validates story text, characters, locations, items, and combat_state persist correctly

## Key Test Classes
- `TestContinueStoryEnd2End`: Main test case for story continuation flow
- `_choices_by_id()`: Helper function for parsing planning block choices

## Test Setup Components
- `FakeFirestoreClient`: Mock Firestore for database operations
- `FakeLLMResponse`: Mock LLM API responses
- `End2EndBaseTestCase`: Base test case with common setup

## Connections
- [[ContextCompaction]] — tested as part of full stack
- [[Firestore]] — database layer under test
- [[LLMProviders]] — Gemini and Cerebras integration
