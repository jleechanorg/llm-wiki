---
title: "Data Serialization"
type: concept
tags: [json, serialization, firestore, api]
sources: ["firestore-service-database-operations"]
last_updated: 2026-04-08
---

## Summary
Process of converting Python objects to/from JSON for Firestore storage, handling special types like datetime, UUID, and custom objects.

## Key Functions
- **json_default_serializer()**: Custom handler for non-serializable types
- **json_serial()**: Datetime conversion utility
- **_normalize_story_entry_contract_fields()**: Schema alignment for writes

## Patterns
- **Story Entry Contract**: Enforces `resources` as string, requires `reinterpreted` + `audit_flags` on action_resolution
- **Contract Validation**: Non-blocking warnings for schema violations

## Connections
- [[Firestore Service]] — uses serialization for all database writes
- [[GameState]] — serializes state for persistence
