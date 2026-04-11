---
title: "Social HP Challenge Schema-Derived Enums Tests"
type: source
tags: [tdd, unit-testing, social-hp, schema-validation, python, unittest]
source_file: "raw/social-hp-challenge-schema-derived-enums-tests.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating that social HP challenge enums (request severity, skills) are derived from schema_validation module rather than hardcoded. Tests cover normalization behavior and fallback defaults for invalid values.

## Key Claims
- **Request Severity Normalization**: Invalid request severity values default to "information" (lowercase)
- **Schema-Derived Enums**: Both game_state and narrative_response_schema modules import valid enum values from schema_validation
- **Normalization**: request_severity is normalized to lowercase in NarrativeResponse

## Key Test Functions
- `test_social_hp_challenge_normalizes_request_severity_and_resistance`: Validates "Submission" → "submission" normalization
- `test_social_hp_challenge_invalid_request_severity_defaults_to_information`: Tests invalid severity defaults to "information"
- `test_game_state_social_hp_enums_are_schema_derived`: Validates _VALID_SOCIAL_REQUEST_SEVERITY comes from schema_validation
- `test_narrative_response_social_hp_enums_are_schema_derived`: Validates VALID_SOCIAL_HP_REQUEST_SEVERITY comes from schema_validation

## Connections
- [[Schema Validation]] — source of enum values
- [[NarrativeResponse]] — model being tested
- [[Game State]] — module being tested
