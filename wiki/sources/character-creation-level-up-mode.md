---
title: "Character Creation & Level-Up Mode"
type: source
tags: [character-creation, dnd-5e, level-up, game-mechanics, modal-agent, worldarchitect]
source_file: "raw/character-creation-level-up-mode.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Focused character creation and level-up flow using D&D 5e rules. Operates as a "pause menu" for character building—does NOT advance narrative or start stories. Provides guided creation through AI-generated, standard D&D, or custom class methods, with mandatory choice-based interaction requiring "Finish Character Creation and Start Game" as final choice.

## Key Claims
- **Pause Menu Principle**: Character creation mode is a dedicated "pause menu" for character building, not narrative progression
- **Mandatory Choice Format**: Every response must include explicit planning_block with choices, following structured JSON schema
- **Finish Choice Protocol**: Must always include "Finish Character Creation and Start Game" as last option, even if character is not yet complete
- **Time Freeze**: World time is frozen during character creation—no narrative events, NPCs, combat, or story progression
- **Modal Agent Constraints**: While character_creation_in_progress==true, classifier is disabled and only CharacterCreationAgent/GodModeAgent are accessible
- **Review Stage Protocol**: When character_creation_stage=="review", the character is PRE-POPULATED and user must explicitly confirm before story begins

## Connections
- [[LevelUpAgent]] — handles level-up flows separately from character creation
- [[GodModeAgent]] — accessible via "GOD MODE:" prefix during character creation
- [[DialogAgent]] — blocked during character creation mode (classifier disabled)
- [[CombatAgent]] — blocked during character creation mode (classifier disabled)
- [[WorldArchitect]] — platform this mode operates within

## Contradictions
- []
