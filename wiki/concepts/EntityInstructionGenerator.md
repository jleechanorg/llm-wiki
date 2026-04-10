---
title: "EntityInstructionGenerator"
type: concept
tags: [entity-instructions, prompt-engineering, code-under-test]
sources: [enhanced-explicit-entity-instructions-tests]
last_updated: 2026-04-08
---

EntityInstructionGenerator creates mandatory entity requirements for LLM prompts. Builds instruction templates, configures entity priorities, and generates enforcement text ensuring entities appear in generated narratives.

**Core methods:**
- _build_instruction_templates(): Creates templates for 5 categories
- _build_entity_priorities(): Sets priority levels (player_character=1, npc_referenced=1, story_critical=2, background=3)
- generate_entity_instructions(entities, player_references, location): Main entry point
- _create_entity_instruction(entity_name, player_references, location, location_owner): Creates individual instructions

**Test validation:**
- Template categories: player_character, npc_referenced, location_npc, story_critical, background
- Player references trigger mandatory requirements
- Location owners marked as background entities
- Output includes "=== MANDATORY ENTITY REQUIREMENTS ===" and enforcement clauses

**Related concepts:** [[EntityInstruction]], [[EntityEnforcementChecker]]
