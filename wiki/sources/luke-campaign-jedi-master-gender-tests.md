---
title: "Luke Campaign Jedi Master Gender Consistency Tests"
type: source
tags: [python, testing, gender-consistency, npc, pydantic, narrative-generation]
source_file: "raw/test_luke_campaign_jedi_master_gender.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite validating the fix for Luke campaign Jedi Master gender consistency issue. Tests verify that NPC gender field prevents narrative generation bugs where female Jedi Masters were incorrectly referenced with male pronouns ("he/him") and male names ("Eldrin").

## Key Claims
- **Gender field enforces consistency**: NPC objects with gender="female" prevent male pronoun usage in narrative generation
- **Bug scenario prevented**: The specific Luke campaign bug where "young woman" Jedi Master later referenced with "Eldrin" (male name) and "he/him" pronouns is now blocked
- **Creative gender accepted**: Pydantic validation now accepts non-standard gender values ("shapeshifter") for LLM flexibility while still rejecting wrong types (integers)
- **Pronoun mapping enabled**: Gender field enables deterministic pronoun selection (she/her for female, he/him for male, they/them for non-binary)

## Key Test Cases
- test_jedi_master_female_consistency: Verifies female gender is stored and pronoun helpers return correct values
- test_prevent_luke_campaign_bug_scenario: Validates that gender field prevents male name/pronoun narrative generation
- test_creative_gender_acceptance: Confirms creative gender values ("shapeshifter") pass validation while invalid types (integers) fail

## Connections
- [[NPC]] — entity schema with gender field
- [[HealthStatus]] — NPC health tracking
- [[Pydantic]] — validation library enabling schema enforcement
- [[NarrativeGeneration]] — system that must respect gender field for pronoun consistency
