---
title: "Shared Type Definitions for WorldArchitect.AI"
type: source
tags: [typescript, python, typing, firestore, worldarchitect]
source_file: "raw/shared-type-definitions.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module containing common type definitions used across the WorldArchitect.AI application, including TypedDicts for Firebase data structures, type aliases, and Protocol definitions for better type safety.

## Key Claims
- **TypedDict Structures**: Six main TypedDict classes define Firebase data structures (CampaignData, StateUpdate, EntityData, MissionData, ApiResponse, LLMRequest, LLMResponse)
- **Type Aliases**: Seven type aliases (UserId, CampaignId, EntityId, SessionId, Timestamp, JsonValue, JsonDict) for common types
- **Protocol Definitions**: DatabaseService and AIService protocols define interface contracts for service implementations
- **Literal Types**: Validators for entity types, campaign states, and log levels using Literal types

## Key Connections
- [[Firebase]] — data storage backend using CampaignData, EntityData TypedDicts
- [[Firestore]] — NoSQL database integration via typed structures
- [[TypedDict]] — Python pattern used for structured dictionaries
- [[Protocol]] — structural subtyping for interface contracts
- [[TypeAlias]] — type shorthand for readability

## Type Definitions Detail

### TypedDicts
- **CampaignData**: Campaign metadata including name, prompt, narrative, entities, state_updates, timestamps
- **StateUpdate**: State change objects with type, key, value, description, category
- **EntityData**: Entity attributes including name, type, description, level, HP, attributes, equipment, spells
- **MissionData**: Quest/mission structure with id, title, description, status, objectives, rewards
- **ApiResponse**: Standard API response with success, message, data, error fields
- **LLMRequest**: Gemini API request structure
- **LLMResponse**: Gemini API response structure

### Protocols
- **DatabaseService**: Protocol defining get_campaign, update_campaign, delete_campaign methods
- **AIService**: Protocol defining generate_response, validate_response methods

### Constants
- VALID_ENTITY_TYPES: character, npc, creature, location, item
- VALID_CAMPAIGN_STATES: active, paused, completed, archived
- VALID_LOG_LEVELS: DEBUG, INFO, WARNING, ERROR, CRITICAL
