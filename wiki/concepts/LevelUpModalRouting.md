---
title: "Level-Up Modal Routing"
type: concept
tags: [routing, modal, state-machine, level-up]
sources: ["level-up-modal-routing-scenarios"]
last_updated: 2026-04-08
---

A state-machine-based routing system that determines when to display the level-up modal in a D&D game interface. Uses multiple state flags to handle edge cases like stale reactivation and in-progress overrides.


## State Flags
- **level_up_pending**: True when XP threshold met, awaiting user action
- **level_up_in_progress**: True when user actively in level-up flow
- **level_up_pending=false**: Explicit false blocks reactivation even with pending rewards


## Decision Tree
1. If character_creation_in_progress → CharacterCreationAgent
2. Else if level_up_in_progress → LevelUpAgent  
3. Else if level_up_pending + valid XP → LevelUpAgent
4. Else → No modal
