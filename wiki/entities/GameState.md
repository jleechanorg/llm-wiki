---
title: "GameState"
type: entity
tags: [game-state, data-model, entity-tracking]
sources: []
last_updated: 2026-04-08
---

## Description
Core game state object in mvp_site.game_state module that tracks player character data, NPCs, world data, and combat state throughout a campaign session.

## Usage
Used in end-to-end tests to verify game state persists correctly through the full application stack from API endpoint to Firestore storage.

## Related
- [[End2EndBaseTestCase]] - test base class
- [[FirestoreService]] - persistence layer
- [[ThorinTheBold]] - sample player character
- [[Gandalf]] - sample NPC companion
