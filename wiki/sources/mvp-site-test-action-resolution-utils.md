---
title: "test_action_resolution_utils.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
Unit tests for the `NarrativeResponse` schema focusing on action_resolution field consolidation (Phases 2-4). Tests verify that action_resolution is the primary field name, reinterpreted field support works, and legacy fields (dice_rolls, dice_audit_events) are normalized to the new format. Tests also cover server warnings when action_resolution is missing.

## Key Claims
- `action_resolution` is accepted as the primary field name in NarrativeResponse and contains player_input, interpreted_as, reinterpreted, mechanics, and audit_flags
- The `reinterpreted` field defaults to False if not provided explicitly
- The `audit_flags` field defaults to empty list if not provided
- Legacy fields `dice_rolls` and `dice_audit_events` are normalized into action_resolution format with mechanics.rolls and mechanics.audit_events respectively
- Normalization sets a `normalized_from_legacy` flag in audit_flags when converting from legacy format
- When action_resolution is explicitly provided (even empty dict), legacy normalization does NOT occur — the provided data is used as-is
- When only outcome_resolution is provided (legacy field), _action_resolution_provided should be True so get_unified_action_resolution() returns the validated data instead of trying to normalize from dice_rolls
- In to_dict() output, both action_resolution and outcome_resolution fields contain identical validated data (not raw unvalidated outcome_resolution)
- Invalid action_resolution types (string, None) are handled gracefully by returning empty dict
- Missing action_resolution field triggers a server warning: "Missing action_resolution field (required for player actions)"
- Each response instance has exactly one warning (no duplicates) when action_resolution is missing

## Key Quotes
> "Bug fix: When only outcome_resolution (legacy) is provided, _action_resolution_provided should be True..." — test documenting a bug fix for backward compatibility
> "Test that outcome_resolution and action_resolution have consistent values in to_dict()." — test documenting another bug fix for field consistency

## Connections
- [[mvp-site-test-action-resolution]] — tests the same utility functions at the lower level (action_resolution_utils.py)
- [[mvp-site-test-action-resolution-backward-compat-end2end]] — end-to-end tests that verify the full API flow with schema validation
- [[mvp-site-narrative-response-schema]] — the schema module being tested