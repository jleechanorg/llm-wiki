---
title: "mvp_site firestore_service"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/firestore_service.py
---

## Summary
Firestore Service for WorldArchitect.AI providing comprehensive database operations: campaign CRUD, game state serialization/persistence, complex state update processing with merge logic, mission management, and JSON serialization utilities. Uses Firebase Admin SDK with defensive programming patterns.

## Key Claims
- Campaign CRUD operations: create, read, update, delete campaigns
- Game state synchronization with merge logic for partial updates
- NumericFieldConverter for data type handling
- JSON serialization via json_default_serializer for Firestore compatibility
- DELETE_TOKEN for marking fields for deletion in state updates
- Legacy data cleanup and migration support
- MAX_TEXT_BYTES = 1000000 for text field limits

## Connections
- [[GameState]] — game state serialization and persistence
- [[Serialization]] — JSON serialization utilities for Firestore
