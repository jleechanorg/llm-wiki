---
title: "Entity ID Schema"
type: concept
tags: [schema, entity-tracking, worldarchitect]
sources: [game-state-management-protocol]
last_updated: 2026-04-08
---

Entity ID Schema defines the required format for entity identifiers in state_updates. The format is `type_name_###` where:
- `type` is the entity type (character, enemy, npc, item, etc.)
- `name` is a lowercase identifier
- `###` is a zero-padded sequence number

**Examples**:
- `character_theron_001`
- `enemy_goblin_001`
- `npc_king_aldric_001`

**Purpose**: Ensures consistent, parseable entity references across all state updates

**Related Concepts**:
- [[EntityTrackingSystem]] — entity tracking implementation
- [[PydanticSchemaModelsEntityTracking]] — schema validation
- [[EntityValidatorShim]] — backward compatibility
