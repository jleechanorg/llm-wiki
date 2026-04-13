---
title: "System Restore Mechanic"
type: concept
tags: [game-mechanic, campaign-feature, testing]
sources: [nocturne-bg3-v6-bug-repro-test-entry-001, nocturne-bg3-v6-bug-repro-test-entry-002, nocturne-bg3-v6-bug-repro-test-entry-003]
last_updated: 2026-04-12
---

## Definition
The System Restore Mechanic is a campaign feature used in the Nocturne BG3 V6 bug-repro-test campaign that allows the game state to be restored to a specific moment. This is particularly useful for testing purposes, allowing developers and players to verify game behavior by returning to a known state and reproducing specific scenarios.

## How It Appears in the Campaigns
- [[nocturne-bg3-v6-bug-repro-test-campaign]]: The campaign specifically tests SYSTEM RESTORE functionality. Character verification and game state restoration are performed at the start of the session to ensure accurate testing conditions

## Related Systems
- Character verification: Ensures all stats and mechanics are correctly restored
- Game state versioning: Tracks changes to enable restoration to specific points

## Connections
- [[NocturneSosukeBugRepro]] — character used in testing
- [[ShatteredSanctum]] — location where testing occurs