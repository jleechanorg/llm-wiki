---
title: "EntityInstruction"
type: concept
tags: [entity-instructions, prompt-engineering, tdd]
sources: [enhanced-explicit-entity-instructions-tests]
last_updated: 2026-04-08
---

EntityInstruction is a data class that represents mandatory entity requirements for LLM prompts. Contains entity_name, instruction_type (mandatory, background), priority level, and specific_instruction text.

**Key attributes:**
- entity_name: Name of the entity
- instruction_type: "mandatory" or "background"
- priority: 1-3 priority level
- specific_instruction: Detailed instruction text

**Usage in tests:**
- Test entity instruction creation for player characters (background type)
- Test NPC referenced instruction creation (mandatory type, priority=1)
- Test location owner instruction creation (background type, priority=3)

**Related entities:** [[Sariel]], [[Cassian]], [[Valerius]]
