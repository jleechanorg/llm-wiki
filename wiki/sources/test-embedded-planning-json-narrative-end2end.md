---
title: "Embedded Planning JSON Narrative End-to-End Test"
type: source
tags: [python, testing, e2e, bug-reproduction, json-parsing, firestore-mocking]
source_file: "raw/test_embedded_planning_json_narrative_end2end.py"
sources: []
last_updated: 2026-04-08
---

## Summary
End-to-end integration test that reproduces and validates the fix for embedded planning block JSON appearing raw in narrative text. Tests the full stack from API endpoint through service layers to Firestore, verifying `_strip_embedded_planning_json()` removes raw JSON from displayed narratives.

## Key Claims
- **Bug Reproduction**: When LLM returns narrative containing embedded JSON like `{"thinking": ..., "choices": ...}`, it should be stripped
- **Full Stack Validation**: Test mocks LLM provider at lowest level, verifying entire API-to-service flow
- **Edge Case Handling**: JSON keys like `"thinking"`, `"choices"`, `"magical_oaths_binding"`, `"analysis"` must be removed from displayed narrative
- **Planning Block Field**: Proper planning JSON should remain in separate `planning_block` field, not in narrative

## Test Structure
- **Class**: `TestEmbeddedJsonNarrativeEnd2End` extends `End2EndBaseTestCase`
- **Test Method**: `test_embedded_json_stripped_from_narrative_end2end`
- **Mock Setup**: Uses `FakeFirestoreClient`, patches `gemini_provider.generate_content_with_code_execution`
- **Test Data**: Contains embedded planning JSON with `thinking`, `choices` keys

## Key Test Components
- `End2EndBaseTestCase`: Base test class providing app creation and authentication
- `FakeFirestoreClient`: Mock Firestore for testing database operations
- `FakeLLMResponse`: Mock LLM responses for controlled testing
- Environment variables: `TESTING_AUTH_BYPASS`, `GEMINI_API_KEY`, `CEREBRAS_API_KEY`

## Connections
- Related to [[test-embedded-planning-json-bug-reproduction]] - unit test version
- Related to [[test-code-execution-artifact-json-parsing]] - JSON parsing logic

## Contradictions
- None identified
