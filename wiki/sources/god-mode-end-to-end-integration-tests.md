---
title: "GOD MODE End-to-End Integration Tests"
type: source
tags: [python, testing, e2e, god-mode, integration, firestore, llm-mocking]
source_file: "raw/test_god_mode_end2end.py"
sources: []
last_updated: 2026-04-08
---

## Summary
End-to-end integration test for GOD MODE functionality. Tests the full application stack including god mode prompt selection and response handling, using mocked external services (LLM and Firestore) at the lowest level.

## Key Claims
- **GOD MODE purpose**: For correcting mistakes and changing campaign state, NOT for playing
- **Prompt separation**: Uses a separate, focused prompt stack without narrative generation prompts
- **Test coverage**: Tests full flow from god mode request to response validation
- **Mock isolation**: Mocks at lowest level (LLM provider APIs and Firestore DB) for true integration testing
- **Response validation**: Uses validate_god_mode_response for output validation

## Key Quotes
> "GOD MODE is for correcting mistakes and changing campaign state, NOT for playing."

## Connections
- [[GOD MODE]] — core functionality under test
- [[FakeFirestoreClient]] — test infrastructure for DB mocking
- [[PromptBuilder]] — builds god mode prompts
- [[validate_god_mode_response]] — validates god mode responses

## Contradictions
- None identified
