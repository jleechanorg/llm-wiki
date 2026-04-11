---
title: "Enhanced Explicit Entity Instructions Tests"
type: source
tags: [python, testing, entity-instructions, enforcement, tdd]
source_file: "raw/test_entity_instructions.py"
last_updated: 2026-04-08
---

## Summary
Unit tests for Enhanced Explicit Entity Instructions (Option 5 Enhanced) testing entity instruction generation and enforcement checking. Tests cover EntityInstructionGenerator and EntityEnforcementChecker classes with player character, NPC, location, and background entity handling.

## Key Claims
- **Template Building**: Instruction templates properly built for player_character, npc_referenced, location_npc, story_critical, background categories
- **Entity Priorities**: Priority levels configured (player_character=1, npc_referenced=1, story_critical=2, background=3)
- **Mandatory Entity Requirements**: Generated instructions include REQUIRED and MUST appear directives with DO NOT complete your response without including enforcement
- **Player Reference Detection**: Cassian marked as mandatory because player specifically mentioned them
- **Location Owner Handling**: Valerius marked as background entity when generating instructions for "Valerius's Study"
- **Entity Instruction Types**: Different types for player characters (background), referenced NPCs (mandatory), location owners (background), and random entities (background)

## Key Quotes
> "The player specifically mentioned Cassian" — triggers mandatory entity requirement
> "DO NOT complete your response without including" — enforcement clause in generated instructions

## Connections
- [[EntityInstruction]] — core instruction class being tested
- [[EntityEnforcementChecker]] — enforcement verification module
- [[EntityInstructionGenerator]] — generates mandatory entity requirements for prompts

## Contradictions
None identified.
