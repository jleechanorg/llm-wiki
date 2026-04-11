---
title: "Entity ID validation with special characters"
type: source
tags: [python, testing, pydantic, validation, entities, sanitization]
source_file: "raw/test_entity_id_special_characters.py"
last_updated: 2026-04-08
---

## Summary
Unit tests validating entity ID sanitization and pattern validation for special characters in entity names. Tests handle apostrophes, hyphens, spaces, non-ASCII characters, and other special characters that could break entity ID generation.

## Key Claims
- **Apostrophe Handling**: Entity names with apostrophes like "Cazador's Spawn" are sanitized to "cazadors_spawn"
- **Special Character Stripping**: Non-alphanumeric characters are removed or replaced with underscores
- **Non-ASCII Handling**: Unicode characters like "Ñ" are handled (becomes "o")
- **Entity ID Pattern Validation**: entity_id field uses Pydantic pattern `^npc_\w+$` or `^pc_\w+$`
- **create_from_game_state Pipeline**: Full pipeline handles special characters without validation errors

## Key Test Functions
- `test_sanitize_entity_name_for_id`: Tests sanitization for various special character cases
- `test_npc_with_apostrophe_name`: Tests NPC creation with apostrophe in name
- `test_entity_id_validation_patterns`: Tests that invalid IDs raise ValidationError
- `test_create_from_game_state_with_special_chars`: Tests full pipeline with special characters

## Test Cases
| Input | Expected Output |
| --- | --- |
| "Cazador's Spawn" | "cazadors_spawn" |
| "Jean-Luc Picard" | "jean_luc_picard" |
| "Dr. Strange" | "dr_strange" |
| "The 'Chosen' One" | "the_chosen_one" |
| "Ñoño García" | "o_o_garc_a" |

## Connections
- [[EntitySchemaClassesUnitTests]] — validates Pydantic schemas for Stats, HealthStatus
- [[DefensiveNumericConverter]] — similar defensive conversion pattern for numeric fields
