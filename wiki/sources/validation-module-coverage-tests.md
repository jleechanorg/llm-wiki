---
title: "Validation Module Coverage Tests"
type: source
tags: [testing, coverage, validation, jsonschema, game-state, tdd]
source_file: "raw/validation_coverage_tests.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Coverage tests targeting the uncovered functions in mvp_site.schemas.validation module. Goals to bring coverage from 28% to 60%+, focusing on check_datetime, _enrich_validation_message, is_valid_game_state, get_common_field_paths, and related utilities.

## Key Claims
- **Module Target**: mvp_site.schemas.validation module with Draft202012Validator
- **Coverage Goal**: Increase from 28% to 60%+
- **Test Focus**: check_datetime (RFC 3339 validation), validation message enrichment, game state validity
- **Helper Functions**: String normalization, near-match suggestions, field path extraction

## Key Test Cases
- check_datetime: Validates RFC 3339 format with UTC, positive/negative offsets, microseconds
- _enrich_validation_message: Enriches player_character_data validation hints with GOD_MODE_UPDATE_STATE guidance
- is_valid_game_state: Boolean validity check for game state objects
- _normalize_for_similarity: String normalization (lowercase, hyphens/spaces to underscores)

## Connections
- [[JSONSchemaValidation]] — uses Draft202012Validator for schema validation
- [[GameStateValidation]] — validates game_state_version and structure
- [[ValidationMessageEnrichment]] — provides hints for player_character_data updates

## Contradictions
- None identified in this test source
