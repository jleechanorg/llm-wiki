---
title: "test_action_resolution_backward_compat_end2end.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
End-to-end tests for action_resolution backward compatibility through the full application stack. Tests cover the complete flow from LLM response through the API to ensure backward compatibility with outcome_resolution, null safety for None values, persistence to Firestore, and dice fabrication detection/correction. Only mocks external services (Gemini API and Firestore DB) at the lowest level.

## Key Claims
- When LLM returns action_resolution (new field), it appears in API response as a dict with player_input, interpreted_as, reinterpreted mechanics.rolls, and audit_flags — no null values leak
- When LLM returns ONLY outcome_resolution (legacy format), API response includes both action_resolution (mapped) and outcome_resolution (for backward compatibility)
- When action_resolution is None, the field is absent from response (not null) or present as empty dict if needed
- When both action_resolution and outcome_resolution are provided, action_resolution takes precedence but both appear in API output
- The llm_response.action_resolution property falls back to outcome_resolution when action_resolution is missing, enabling backward compatibility at the property level
- action_resolution is persisted to Firestore story entries — fixes bug where it was added to unified_response but not persisted
- Dice fabrication detection: dice_integrity._is_code_execution_fabrication() detects fabricated dice rolls (dice provided without code_execution tool usage) and generates correction text from processing_metadata
- Spoofing prevention: llm_service.py clears LLM-provided _server_* fields to prevent security bypass — server-generated values are not overwritten by LLM input
- Corrections persist to game_state.pending_system_corrections and are sent to LLM on next turn, then cleared after consumption
- Correction text is generated dynamically (not hardcoded) and mentions "CORRECTION", "code_execution", and "random.randint"

## Key Quotes
> "Only mocks external services (Gemini API and Firestore DB) at the lowest level." — test scope definition
> "This validates the fix for the bug where action_resolution was added to unified_response but not persisted to Firestore." — test documenting bug fix
> "SECURITY VIOLATION: LLM-provided _server_dice_fabrication_correction was not cleared!" — security assertion message

## Connections
- [[mvp-site-test-action-resolution]] — lower-level unit tests for action_resolution_utils
- [[mvp-site-test-action-resolution-utils]] — schema validation unit tests
- [[mvp-site-test-dice-fabrication-correction-e2e]] — companion E2E tests for dice fabrication detection