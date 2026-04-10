---
title: "Reinterpreted Field"
type: concept
tags: [schema, field-defaults, llm-interpretation]
sources: [action-resolution-field-consolidation-tests]
last_updated: 2026-04-08
---

## Definition
A boolean flag in action_resolution indicating whether the LLM reinterpreted the player's input. When True, the player said one thing but the system interpreted it differently (e.g., "The king agrees" → "persuasion_attempt").

## Default Behavior
- Defaults to False if not explicitly provided
- Can be explicitly set to True with audit_flags like "player_declared_outcome"

## Use Case
Used for audit and transparency — players can see when their input was reinterpreted rather than taken literally.

## Related Concepts
- [[ActionResolution]] — parent field
- [[AuditFlags]] — related audit tracking field
