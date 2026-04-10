---
title: "Campaign Management"
type: concept
tags: [crud, database, campaign, persistence]
sources: ["firestore-service-database-operations"]
last_updated: 2026-04-08
---

## Summary
System for Create, Read, Update, Delete operations on campaign data in Firestore.

## Key Operations
- **Create**: New campaign initialization with default game state
- **Read**: Load campaign with game state deserialization
- **Update**: Complex merge logic for nested state updates
- **Delete**: Campaign removal with cleanup options

## Patterns
- **Defensive Programming**: Validation before writes
- **Legacy Migration**: Automatic schema upgrades
- **Atomic Updates**: Token-based field deletion (`__DELETE__`)

## Connections
- [[Firestore Service]] — implements campaign CRUD
- [[GameState]] — manages campaign state object
