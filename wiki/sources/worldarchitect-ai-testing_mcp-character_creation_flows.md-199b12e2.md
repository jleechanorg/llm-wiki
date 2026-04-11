---
title: "Character Creation Flow Paths"
type: source
tags: [worldarchitect-ai, character-creation, D&D-5e, testing, lifecycle, game-mechanics]
sources: []
date: 2026-04-07
source_file: mvp_site/prompts/character_creation_instruction.md
last_updated: 2026-04-07
---

## Summary
Comprehensive specification of all possible paths through D&D 5e character creation and level-up for the WorldArchitect.AI game system. Defines the TIME FREEZE principle where world progression halts during character mechanics, enabling comprehensive lifecycle testing across race/class/background combinations.

## Key Claims
- **TIME FREEZE**: World time is FROZEN during character creation/level-up. No story progression, world changes, or narrative advancement until character mechanics are complete.
- **Three Main Flows**: Full Character Creation (new campaign), Level-Up (existing character), Pre-Defined Character (God Mode templates)
- **Ability Score Assignment**: Three paths — Standard Array (15,14,13,12,10,8), Point Buy (27 points), or Custom/Rolled values
- **12 D&D 5e Classes**: Barbarian, Bard, Cleric, Druid, Fighter, Monk, Paladin, Ranger, Rogue, Sorcerer, Warlock, Wizard — each with unique mechanics
- **9 PHB Races**: Dwarf, Elf, Halfling, Human, Dragonborn, Gnome, Half-Elf, Half-Orc, Tiefling
- **ASI Triggers**: Ability Score Improvements at levels 4, 8, 12, 16, 19 — can take +2 to one ability, +1 to two abilities, or a feat

## Key Quotes
> "**CRITICAL**: World time is FROZEN during character creation/level-up. No story progression, no world changes, no narrative advancement until character mechanics are complete."

> "Completion: Set `character_creation_in_progress: False`, set `level_up_in_progress: False`, **UNFREEZE TIME**: Story can now progress"

## Connections
- [[DungeonsAndDragons5e]] — core rule system
- [[CharacterLevelUpMechanics]] — related level-up flow
- [[GodModeTemplates]] — pre-defined character system
- [[WorldTimeProgression]] — time freeze mechanism

## Contradictions
- None detected — this is foundational game mechanics documentation
