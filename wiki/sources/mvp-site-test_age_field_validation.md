---
title: "test_age_field_validation.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
Test suite for age field validation in NPC and PlayerCharacter Pydantic models. Tests verify that age is optional, accepts valid fantasy ages (1-50000), rejects negative ages and unreasonably high values, and enforces integer type. Enables narrative consistency by preventing inconsistent descriptions like a 16-year-old "grizzled veteran."

## Key Claims
- Age field is optional in both NPC and PlayerCharacter models
- Valid ages range from 0 to 50000 (supports fantasy races like elves and dwarves)
- Non-integer ages (floats, strings, lists, dicts) are rejected with ValidationError
- Narrative consistency helpers enable age-appropriate character descriptions

## Connections
- [[mvp-site-entities_pydantic]] — defines NPC and PlayerCharacter models
- [[mvp-site-HealthStatus]] — health model used in character creation