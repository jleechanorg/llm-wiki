---
title: "Game State Management Protocol"
type: source
tags: [game-state, protocol, json-schema, session-header, validation, dice-mechanics]
source_file: "raw/game-state-management-protocol.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Comprehensive protocol for managing game state in WorldArchitect.AI, covering JSON response formatting, session headers, state updates, entity ID schemas, and mandatory game mechanics including dice rolls, combat, inventory validation, and faction minigames.

## Key Claims
- **JSON Structure Required**: All responses must include session_header, narrative, and planning_block in structured JSON format
- **Entity ID Format**: State updates require entity IDs with format `type_name_###` (e.g., character_theron_001)
- **Dice Execution Protocol**: All combat attacks must use dice tools — never auto-succeed or fabricate results
- **Inventory Validation**: Players can only use items from their `equipment` or `backpack` slots — reject claims to non-existent items
- **Level Display Mandatory**: All character names in narrative must include level (e.g., "Theron (Lvl 5)")
- **Faction Minigame Mandatory**: Must suggest enabling faction minigame when army strength >= 100, strongly recommend at >= 500
- **Turn vs Scene Distinction**: Scene counts AI responses only; turn counts all entries (user + AI)

## Key Quotes
> "DICE VALUES ARE UNKNOWABLE: You cannot predict, estimate, or fabricate dice results. Use tools to OBSERVE them."

> "VISIBILITY RULE: Users see ONLY the narrative text. state_updates, rewards_pending are invisible to players."

## Connections
- [[GameStateExamples]] — session header format and response JSON schema
- [[DiceMechanicsUtilitiesModule]] — logging utilities for dice fabrication detection
- [[DiceValuesAreUnknowable]] — code execution protocol requiring random.randint()
- [[DiceStrategySelection]] — provider-based dice strategy selection
- [[FactionMinigameStateAccessUtilities]] — extraction of faction_minigame from game_state
- [[FactionArmyManagementSystem]] — mandatory suggestion protocol for faction minigame

## Contradictions
- None detected
