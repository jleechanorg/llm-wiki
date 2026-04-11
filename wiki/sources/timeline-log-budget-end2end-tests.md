---
title: "Timeline Log Budget End-to-End Tests"
type: source
tags: [testing, e2e, guardrails, timeline, firestore, story-context]
source_file: "raw/timeline-log-budget-tests.py"
sources: []
last_updated: 2026-04-08
---

## Summary
End-to-end regression tests for timeline_log budgeting guardrails, specifically testing a "dormant duplication guard" that prevents large story contexts from causing issues. Tests simulate 80-turn story contexts to verify GameState handles timeline budgets correctly.

## Key Claims
- **Dormant Duplication Guard**: Tests verify the guardrail that prevents duplicated entries in timeline_log when story_context grows large
- **Large Story Context Handling**: 80-turn story context created to trigger edge case in timeline budgeting
- **Fake Service Layer**: Uses FakeFirestoreClient and FakeLLMResponse for full E2E mocking
- **GameState Integration**: Validates story_context, characters, locations, items, npc_data, and world_data flow through Firestore

## Test Setup
- FakeFirestore for campaign and game_state persistence
- FakeLLM for LLM response mocking
- Test user: test-user-timeline-budget
- Campaign: Timeline Log Bug Test

## Connections
- [[FakeFirestoreClient]] — mock Firestore for E2E tests
- [[FakeLLMResponse]] — mock LLM responses
- [[End2EndBaseTestCase]] — base test class
- [[GameState]] — the data structure being tested
