---
title: "GodModeAgent"
type: entity
tags: [agent, game-mode, administration]
sources: ["agent-architecture-end2end-integration-test", "spicy-mode-literary-intimate-content-system-instruction"]
last_updated: 2026-04-08
---

GodModeAgent handles administrative commands in WorldArchitect, allowing players to modify game state directly (set HP, add gold, change levels, teleport, etc.). Triggered by "GOD MODE:" prefix which bypasses intent classifier.

## Mode
- `MODE_GOD` (from constants)

## Commands Handled
- Set HP/inventory/level
- Reset combat encounters
- Teleport locations
- Fix quest state

## Related
- [[StoryModeAgent]] — narrative mode
- [[SpicyModeAgent]] — adult content variant
- [[IntentClassifier]] — normally determines routing
