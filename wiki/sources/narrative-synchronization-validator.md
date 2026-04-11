---
title: "Narrative Synchronization Validator for Production Entity Tracking"
type: source
tags: [python, narrative-validation, entity-tracking, continuity, game-mechanics]
source_file: "raw/narrative-synchronization-validator.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Production-grade validator for preventing narrative desynchronization in WorldArchitect.AI. Refactored from Milestone 0.4 prototype to delegate all entity presence logic to EntityValidator while adding narrative-specific continuity checking and emotional state pattern detection.

## Key Claims
- **Delegation Pattern**: Refactored to delegate all entity validation to EntityValidator for single source of truth
- **Entity Presence Types**: Enum distinguishing physically_present, mentioned_absent, implied_present, and ambiguous presence
- **EntityContext Dataclass**: Stores name, presence_type, location, last_action, emotional_state, and physical_markers
- **ValidationResult Dataclass**: Structured result with entities_found, entities_missing, all_entities_present, confidence, warnings, and metadata
- **Continuity Checking**: Validates that previously noted physical states (e.g., "bandaged ear") are maintained in subsequent narrative
- **Emotional State Patterns**: Dictionary mapping emotional states (grief, anger, fear, guilt) to keyword patterns for narrative detection

## Key Classes
- **EntityPresenceType**: Enum with four presence states
- **EntityContext**: Dataclass for entity contextual information
- **ValidationResult**: Dataclass for validation outcomes
- **NarrativeSyncValidator**: Main validator class with continuity and emotional pattern detection

## Connections
- [[EntityValidator]] — delegates all entity presence validation to this component
- [[NarrativeDirectivesLite]] — validates narrative consistency against tabletop DM principles
- [[LivingWorldTriggerEvaluation]] — tracks entity states across turns for continuity

## Contradictions
- None identified
