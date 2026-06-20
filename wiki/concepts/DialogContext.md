---
title: "DialogContext"
type: concept
tags: [dialog, game-state, agent-selection]
sources: []
last_updated: 2026-04-08
---

## Description
Game state attribute that tracks whether the game is currently in a dialog interaction. Represented as a dictionary with an `active` boolean flag.

## Usage
DialogAgent checks `dialog_context["active"]` when determining if it should handle the current game state.

## Related
- [DialogAgent](../entities/DialogAgent.md) uses this to determine agent selection
- [GameState](GameState.md) contains this attribute
