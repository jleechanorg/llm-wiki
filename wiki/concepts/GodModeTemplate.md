---
title: "God Mode Template"
type: concept
tags: [worldarchitect, character-creation, template]
sources: [character-creation-level-up-mode]
last_updated: 2026-04-08
---

## Definition
Campaign template feature in WorldArchitect.AI that pre-populates character data for the Character Creation Mode.

## Workflow
1. Campaign template provides `player_character_data` with complete character (name, race, class, stats, equipment)
2. Character Creation Mode presents the pre-generated character for review
3. User chooses "Edit Character" or "Finish Character Creation and Start Game"
4. Does NOT ask user to create character from scratch—character already exists

## Interaction Pattern
When receiving pre-populated character:
- Display character name, race, class, abilities, equipment
- Use tag: `[CHARACTER CREATION - Review]`
- Offer exactly two choices: Edit Character / Finish Character Creation and Start Game

## Connection to Character Creation Mode
Part of [[CharacterCreationLevelUpMode]] workflow—distinguishes between template-derived characters (presented for review) vs. manual creation (guided step-by-step).
