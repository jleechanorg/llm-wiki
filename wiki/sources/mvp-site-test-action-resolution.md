---
title: "test_action_resolution.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
Unit tests for helper functions in `action_resolution_utils.py`. Tests cover extracting dice rolls and audit events from action_resolution structures, normalizing legacy fields, and detecting dice presence. Tests are organized into five test classes covering extraction, normalization, and helper functions.

## Key Claims
- `extract_dice_rolls_from_action_resolution()` correctly formats dice rolls as human-readable strings including notation, result, total, DC (when applicable), and success/failure status
- Multiple dice rolls can be extracted and formatted in order, with each roll getting its own formatted string including purpose, notation vs total, vs DC, and outcome
- Invalid roll formats (missing fields, wrong types) are handled gracefully and return empty lists without raising exceptions
- `extract_dice_audit_events_from_action_resolution()` can extract both string-based and dict-based audit events from the mechanics section
- `add_action_resolution_to_response()` normalizes legacy payloads by mapping `outcome_resolution` to `action_resolution` when the latter is missing, preserving the original data structure
- The `label` field is normalized to `purpose` for frontend compatibility while preserving existing `purpose` values if they already exist
- `has_action_resolution_dice()` returns True when either rolls or audit_events are present, False for empty or invalid structures

## Key Quotes
> "Test extraction of roll with DC and failure" — test case verifying DC and failure formatting: "1d20+5 = 17 vs DC 18 - Failure (Persuasion)"
> "Test that 'label' is normalized to 'purpose' for frontend compatibility." — comment explaining normalization behavior
> "Test that legacy payloads with only outcome_resolution backfill action_resolution." — test for backward compatibility with legacy field names

## Connections
- [[mvp-site-test-action-resolution-utils]] — tests the same utility functions but with schema validation and consolidation tests
- [[mvp-site-test-action-resolution-backward-compat-end2end]] — end-to-end tests that verify the full API flow with these utilities
- [[mvp-site-action-resolution-utils]] — the module being tested