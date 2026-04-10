---
title: "MissionHandler"
type: entity
tags: [class, firestore, testing, coverage]
sources: ["mission-handler-tests-firestore-service"]
last_updated: 2026-04-08
---

## Description
Static class in firestore_service.py that handles mission-related operations including list initialization, mission index lookup, and mission data processing.

## Key Methods
- **initialize_missions_list**: Ensures a key exists in state with an empty list, handling non-list values
- **find_existing_mission_index**: Searches missions list by mission_id, handling invalid objects gracefully
- **process_mission_data**: Adds new missions or updates existing ones with logging

## Test Coverage
Tests cover edge cases: missing keys, non-list values, empty lists, invalid mission objects, and mission_id lookup.

## Related
- [[FirestoreService]] — parent module
- [[Firestore Service Inventory Deduplication Tests]] — related test coverage
