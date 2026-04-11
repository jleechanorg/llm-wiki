---
title: "Enhanced Post-Generation Validation with Retry Tests"
type: source
tags: [python, testing, entity-validation, retry-logic, narrative-generation]
source_file: "raw/test_enhanced_post_generation_validation_retry.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests for the Enhanced Post-Generation Validation with Retry module (Option 2 Enhanced). Tests validate entity presence detection, retry logic functionality, scoring algorithms, and prompt generation for improved entity tracking in story generation.

## Key Claims
- **EntityValidator**: Validates entity presence in generated narratives with confidence scoring
- **EntityRetryManager**: Manages retry logic for failed validations with suggestion generation
- **ValidationResult**: Unified result format with backward compatibility for legacy and new validation formats
- **Scoring Algorithm**: Calculates confidence scores based on direct mentions, action attribution, and partial name matches
- **Retry Prompt Generation**: Creates detailed retry instructions with location-specific suggestions

## Key Test Cases
1. `test_validate_entity_presence_success` - Validates successful entity detection with high confidence
2. `test_validate_entity_presence_missing_entities` - Tests detection of missing entities with retry flag
3. `test_calculate_entity_presence_score_direct_mention` - Direct mention scoring (0.8+)
4. `test_calculate_entity_presence_score_action_attribution` - Action attribution scoring (capped at 1.0)
5. `test_calculate_entity_presence_score_partial_match` - Partial name match scoring (0.3-0.8)
6. `test_generate_retry_suggestions_cassian` - Entity-specific retry suggestions
7. `test_generate_retry_suggestions_location_specific` - Location-aware suggestions
8. `test_create_retry_prompt` - Retry prompt creation with RETRY INSTRUCTIONS section

## Key Quotes
> "Test successful entity validation" — validates found_entities matches expected
> "Partial match should give some score (2/3 of name parts match)" — scoring rationale

## Connections
- [[EntityValidator]] — main class under test
- [[ValidationResult]] — result dataclass under test
- [[EntityRetryManager]] — retry management class
- [[Enhanced Post-Generation Validation with Retry]] — module being tested

## Contradictions
- None identified
