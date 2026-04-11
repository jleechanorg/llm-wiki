---
title: "Generic Entity Tracking Tests"
type: source
tags: [python, testing, entity-tracking, generic-design]
source_file: "raw/test_entity_tracking_generic.py"
last_updated: 2026-04-08
---

## Summary
Unit tests validating that entity tracking system is truly generic and does not contain hardcoded campaign-specific references. Tests verify EntityInstructionGenerator, LocationEntityEnforcer, and related components work for any campaign type.

## Key Claims
- **No Hardcoded Sariel**: Entity instructions must not contain hardcoded references to Sariel, Cassian, Valerius, or Cressida
- **Generic PC Detection**: Player character detection must be dynamic, not hardcoded to specific names
- **Generic Location Rules**: Location enforcer returns empty rules for all locations (no hardcoded location-to-entity mappings)
- **Campaign-Agnostic**: System works for any campaign type (Space Opera, Fantasy, etc.)

## Key Test Cases
1. `test_entity_instructions_not_hardcoded_sariel` - Verifies no Sariel references in generated instructions
2. `test_player_character_detection_is_generic` - Verifies PC detection returns False for all names
3. `test_location_enforcer_not_hardcoded` - Verifies location enforcer returns empty rules
4. `test_location_mappings_are_generic` - Verifies location owner detection disabled
5. `test_entity_specific_instruction_is_generic` - Verifies entity-specific methods removed
6. `test_entity_tracking_with_different_campaign` - E2E test with Space Opera campaign

## Connections
- [[EntityInstructionGenerator]] — class being tested for generic behavior
- [[LocationEntityEnforcer]] — class being tested for hardcoded location removal
- [[EntityTracking]] — broader system this validates
- [[GenericDesign]] — design pattern being enforced
