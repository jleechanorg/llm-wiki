---
title: "Firestore Service - Database Operations and Game State Management"
type: source
tags: [python, firestore, database, game-state, firebase]
source_file: "raw/firestone-service-database-operations.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Comprehensive database operations module for WorldArchitect.AI providing campaign CRUD, game state serialization, complex state updates with merge logic, and defensive data integrity patterns using Firebase Firestore.

## Key Claims
- **Campaign CRUD**: Create, Read, Update, Delete operations for campaigns
- **Game State Serialization**: Robust JSON serialization utilities for Firestore compatibility
- **Complex State Updates**: Merge logic for updating nested game state structures
- **Mission Management**: Smart data conversion and mission handling
- **Defensive Programming**: Data integrity validation and comprehensive error handling
- **Legacy Migration**: Support for cleaning up and migrating legacy data formats

## Key Components
### FirestoreWriteError
Custom exception raised when Firestore writes return unexpected responses.

### _normalize_story_entry_contract_fields()
Normalizes story entry fields to satisfy StoryEntry contract:
- Converts `resources` from dict to string
- Ensures `action_resolution` includes `reinterpreted` + `audit_flags`

### json_default_serializer()
Custom JSON serializer for Firestore compatibility, handling datetime, UUID, and custom objects.

## Connections
- [[Firebase]] — underlying database service
- [[GameState]] — state management class
- [[NumericFieldConverter]] — data type handling
- [[Defensive Numeric Converter]] — range validation for D&D fields

## Contradictions
- None currently documented
