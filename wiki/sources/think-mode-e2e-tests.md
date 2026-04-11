---
title: "THINK MODE End-to-End Tests"
type: source
tags: [testing, e2e, think-mode, integration, prompt-engineering]
source_file: "raw/think-mode-e2e-tests.py"
sources: []
last_updated: 2026-04-08
---

## Summary
End-to-end integration tests for THINK MODE functionality, which enables strategic planning and tactical analysis WITHOUT narrative advancement. Tests mock external services (LLM provider APIs and Firestore DB) at the lowest level and verify the full flow including think mode prompt selection and response handling.

## Key Claims
- **Think Mode Time Advancement**: THINK MODE advances time by only 1 microsecond, allowing strategic planning without narrative progression
- **Prompt Selection**: Tests verify correct think mode prompt is selected when user invokes think mode
- **Response Handling**: Full response flow including session_header, narrative, planning_block, dice_rolls, and state_updates
- **Entity Tracking**: Player character identity (e.g., Shadow) preserved through entity validation
- **Mock Architecture**: Uses FakeFirestoreClient and FakeLLMResponse for boundary-level mocking

## Key Quotes
> "THINK MODE is for strategic planning and tactical analysis WITHOUT narrative advancement. Time advances by only 1 microsecond. The character thinks but does not act."

## Connections
- [[ThinkMode]] — the feature being tested
- [[EndToEndTesting]] — testing methodology used
- [[SessionHeader]] — session state management
- [[FirestoreMock]] — database mocking for tests

## Contradictions
- None identified in current wiki content