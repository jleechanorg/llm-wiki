---
title: "Firestore Persistence"
type: concept
tags: [firestore, database, persistence, google-cloud, nosql]
sources: []
last_updated: 2026-04-08
---

## Definition
Google Firestore NoSQL database used for persisting game state. The system uses non-blocking schema validation to ensure writes succeed even with warning-level issues.

## Key Behavior
- Non-blocking validation allows writes to proceed with warnings logged
- Ensures gameplay continuity during schema issues
- Debug information available via validation logs

## Related
- [[GameState]] — object persisted to Firestore
- [[SchemaValidation]] — applied before persistence
- [[REV-9zs]] — implements non-blocking behavior
