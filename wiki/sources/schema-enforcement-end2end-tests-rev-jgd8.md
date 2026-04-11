---
title: "Schema Enforcement End-to-End Tests (REV-jgd8)"
type: source
tags: [e2e-testing, schema-enforcement, firestore, gemini, flask, canonical-field-placement, schema-validation]
source_file: "raw/test_schema_enforcement_end2end.py"
sources: []
last_updated: 2026-04-08
---

## Summary
End-to-end integration test validating schema enforcement throughout the full request path. REV-jgd8 provides CI-friendly tests that mock external services (Firestore + LLM provider) while exercising the real Flask API /interaction endpoint. Tests verify schema validation runs on every turn via GameState.to_validated_dict and validates canonical field placement for new writes (gold standard).

## Key Claims
- **Mocked External Services**: Only Firestore and LLM provider are mocked; Flask API runs real code
- **Schema Validation Every Turn**: GameState.to_validated_dict ensures schema enforcement on every interaction
- **Canonical Field Placement**: Tests validate gold standard (schema-compliant writes) and legacy fallback (backfill canonical)
- **CI-Friendly Design**: Uses TESTING_AUTH_BYPASS, MOCK_SERVICES_MODE, and Gemini stub client to avoid network calls
- **Debug Mode Verification**: Tests enable debug_mode to verify response includes state_updates for assertions

## Key Quotes
> "MOCK_SERVICES_MODE forces the Gemini provider into its stub client so token counting and generation never hit the network in CI."

> "Validates canonical field placement for new writes (gold)"

## Connections
- [[GameState]] — entity being validated for schema compliance
- [[Firestore]] — external service being mocked; validates state persistence
- [[GeminiProvider]] — LLM provider being stubbed for CI
- [[FlaskAPI]] — real API endpoint being tested (/interaction)
- [[REV-jgd8]] — PR this test was introduced for

## Contradictions
- []
