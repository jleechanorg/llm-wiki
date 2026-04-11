---
title: "Mock Firestore Service Wrapper"
type: source
tags: [python, firestore, mock, testing, service-wrapper]
source_file: "raw/mock-firestore-service-wrapper.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module providing a mock implementation of the Firestore service interface for testing purposes. Wraps MockFirestoreClient to deliver the same API as the real firestore_service module, enabling tests to run with either mock or real backends.

## Key Claims
- **Interface Parity**: Provides identical function signatures to real firestore_service for seamless swapping
- **Module-Level Singleton**: Uses global `_client` instance for consistent state across calls
- **Backward Compatibility**: Supports both legacy `story_entry` parameter and new structured parameters
- **Sentinel Pattern**: Uses `DELETE_FIELD` sentinel for field deletion operations
- **Deep Merge**: Implements intelligent state merging for partial updates

## Key Functions
- **Campaign Management**: `get_campaigns_for_user`, `get_campaign_by_id`, `create_campaign`, `update_campaign`, `delete_campaign`
- **Game State**: `get_game_state`, `update_game_state`, `update_state_with_changes`, `get_campaign_game_state`, `update_campaign_game_state`
- **Story Management**: `add_story_entry`, `get_story_context` with backward compatibility

## Connections
- [[MockFirestoreClient]] — underlying mock implementation
- [[FirestoreService]] — real service this mocks
- [[RealModeTestingFramework]] — framework enabling mock/real switching

## Contradictions
- None identified
