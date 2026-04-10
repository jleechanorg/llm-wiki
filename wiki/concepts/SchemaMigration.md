---
title: "Schema Migration"
type: concept
tags: [database, migration, compatibility, firestore]
sources: []
last_updated: 2026-04-08
---

## Description
System for migrating legacy campaign state to current schema format. Includes session ID seeding for Firestore-compatibility, migration version tracking (SCHEMA_MIGRATION_VERSION=1), and the migrated_at timestamp field. Legacy campaigns are migrated once, then strict validation is enforced.

## Key Components
- **Legacy Session ID Seed**: Stable seed based on campaign_id/user_id or deterministic payload hash
- **Migration Version**: Tracks schema version for compatibility
- **Strict Validation Post-Migration**: Ensures migrated data meets current standards

## Connections
- [[GameStateClassDefinition]] — implements migration protocol
- [[FirestoreServiceDatabaseOperations]] — handles migration persistence
