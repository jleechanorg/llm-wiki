---
title: "Freeze Time Choice Behavior Tests"
type: source
tags: [python, testing, schema-validation, planning-blocks, boolean-coercion]
source_file: "raw/test_freeze_time_choice_behavior.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating freeze_time field behavior in planning block choices. When a planning block choice has freeze_time=true, selecting that choice should cause time to advance by only 1 microsecond (like Think Mode), rather than advancing normally. This is used for meta-game decisions like level-up choices that don't represent in-game time passing.

## Key Claims
- **freeze_time: true preserved**: Boolean true values in choices are maintained through schema validation
- **freeze_time: false preserved**: Boolean false values are correctly maintained
- **String coercion**: String values "true"/"false" are coerced to proper boolean types
- **No automatic injection**: When freeze_time is not present, it should not be added to validated choice

## Key Test Cases
1. `test_freeze_time_boolean_true_preserved` - Validates true boolean preserved through validation
2. `test_freeze_time_boolean_false_preserved` - Validates false boolean preserved
3. `test_freeze_time_string_true_coerced` - Validates "true" string coerced to True
4. `test_freeze_time_string_false_coerced` - Validates "false" string coerced to False
5. `test_freeze_time_missing_not_added` - Validates no automatic addition of field

## Connections
- [[NarrativeResponseSchema]] — schema class being tested
- [[FactionMinigame]] — uses freeze_time for meta-game decisions

## Contradictions
None identified.