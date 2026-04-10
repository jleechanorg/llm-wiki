---
title: "narrative_response_schema.py"
type: entity
tags: [schema, python, narrative-response]
sources: [narrative-response-social-hp-tests]
last_updated: 2026-04-08
---

`narrative_response_schema.py` is a Python module containing the [[NarrativeResponse]] Pydantic schema and validation functions for structured LLM responses.

## Key Functions
- `_find_matching_brace()`: Helper for JSON parsing
- `_validate_resources()`: Validates resource field
- `_validate_social_hp_challenge()`: Validates Social HP Challenge with tier checking
- `parse_structured_response()`: Main parser for raw LLM output

## Validation
The module implements strict tier validation for [[SocialHPChallenge]]:
- Logs warnings for invalid `npc_tier` values
- Validates `social_hp_max` is within tier-specific ranges
- Supports tier ranges: commoner (1-2), merchant/guard (2-3), noble/knight (3-5), lord/general (5-8), king/ancient (8-12), god/primordial (15+)
