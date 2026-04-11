---
title: "Enhanced Pydantic Entity Integration Tests"
type: source
tags: [python, testing, pydantic, validation, entities, schema]
source_file: "raw/mvp_site_all/test_entities_pydantic_integration.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite validating Pydantic entity models (NPC, PlayerCharacter, HealthStatus, Stats) with integrated fields from entities_simple.py and game_state_instruction.md. Tests gender validation requirements for NPCs, age validation with fantasy-appropriate ranges, and MBTI personality type validation.

## Key Claims
- **Gender Mandatory for NPCs**: NPCs require gender field for narrative consistency; creation fails with "Gender is required for NPCs" error
- **Gender Optional for PCs**: PlayerCharacter entities allow optional gender
- **Creative Genders Accepted**: Permissive validation allows creative gender values beyond traditional categories
- **Age Validation**: Fantasy-appropriate age ranges from 0 to 50,000 years accepted; negative ages and ages >50,000 rejected
- **MBTI Validation**: Validates 16 standard MBTI personality types (INTJ, INTP, ENTJ, ENTP, INFJ, INFP, ENFJ, ENFP, ISTJ, ISFJ, ESTJ, ESFJ, ISTP, ISFP, ESTP, ESFP)

## Key Test Functions
- `test_npc_gender_validation_mandatory`: Verifies NPC creation fails without gender
- `test_npc_gender_validation_valid`: Tests valid gender values (male, female, non-binary, other)
- `test_npc_creative_gender_accepted`: Confirms creative gender values pass validation
- `test_pc_gender_optional`: Validates gender is optional for PlayerCharacter
- `test_age_validation_fantasy_ranges`: Tests fantasy age ranges (0-50,000 years)
- `test_age_validation_invalid_ranges`: Verifies rejection of negative and excessive ages
- `test_mbti_validation`: Validates all 16 MBTI personality types

## Connections
- [[EntitiesPydantic]] — module under test
- [[NPC]] — entity type being validated
- [[PlayerCharacter]] — entity type with optional gender
- [[HealthStatus]] — embedded Pydantic model
- [[PydanticValidation]] — validation patterns being tested
