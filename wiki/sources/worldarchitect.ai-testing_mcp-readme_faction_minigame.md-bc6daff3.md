---
title: "WorldAI Faction Management Mini-Game Tests"
type: source
tags: [worldarchitect, testing, faction-minigame, game-state, god-mode, turn-based-strategy]
sources: []
date: 2026-04-07
source_file: raw/faction_minigame_tests.md
last_updated: 2026-04-07
---

## Summary
Server-level test suite for the WorldAI Faction Management mini-game — a turn-based faction strategy layer atop D&D 5e adventure gameplay. Contains 21 tests validating faction minigame state structure and persistence via GOD_MODE_UPDATE_STATE commands. Supports both deploy preview and local server testing modes.

## Key Claims

- **21 Test Scenarios**: Comprehensive coverage across state creation (3), buildings (2), unit classification (3), ranking/power (2), research (1), council (2), alliances (1), prestige/lineage (2), apotheosis win condition (1), intel operations (2), and state modification (2)
- **Dual Testing Modes**: Can run against GCP deploy preview (`MCP_SERVER_URL`) or local server (`http://127.0.0.1:8001`), with optional auto-start local server
- **Faction Minigame Mechanics**: Players manage territory, citizens, resources, buildings, and units (soldiers, spies, elites) while competing against 200 AI factions for ranking dominance

## Key Quotes
> "The faction minigame system allows players to: manage a domain with territory, citizens, and resources; build structures and recruit units; compete against 200 AI factions for ranking dominance; conduct intel operations with spies; form alliances and manage prestige/lineage; pursue the Apotheosis Ritual win condition"

## Connections
- [[WorldArchitect.AI]] — host platform for the faction minigame
- [[Testing MCP Agent Instructions]] — testing framework standards this test follows

## Contradictions
