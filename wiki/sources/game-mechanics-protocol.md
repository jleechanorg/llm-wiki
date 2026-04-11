---
title: "Game Mechanics Protocol"
type: source
tags: [dnd, game-mechanics, character-creation, combat, rpg, xp-system]
source_file: "raw/game-mechanics-protocol.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Comprehensive D&D 5e game mechanics protocol defining character creation flow, combat rules, XP systems, and mass combat for 20+ forces. Enforces meta-game-only character creation with three methods (AIGenerated, StandardDND, CustomClass) and strict player input handling with mandatory planning blocks.

## Key Claims
- **Meta-Game Character Creation**: Character creation is META-GAME only—no narrative until approval. Three options: AIGenerated, StandardDND, CustomClass
- **Firebase Sanity Check**: First response must echo loaded data exactly to confirm correctness
- **Player Input Mandate**: NEVER ignore player input. Must acknowledge, explain why it can't be used, and offer override/alternatives
- **XP by CR Table**: CR 0=10, 1/8=25, 1/4=50, 1/2=100, 1=200, 2=450, 3=700, 4=1100, 5=1800 XP
- **No Paper Enemies**: CR must match HP—see combat_system_instruction.md
- **Mass Combat (20+ forces)**: Strategic combat with unit blocks (10 soldiers), daily upkeep, morale system
- **Milestone Leveling**: Recommend +1-3 levels per arc, may exceed Level 20 for epic/mythic campaigns
- **Attunement**: Configurable (Standard=3, Loose=5-6, None=unlimited)
- **High-Magic Balance**: T1=3-4 encounters/day, T2=5-7 encounters+resource pressure, T3=elite groups+counter-buffs, T4=set-pieces+artifact-level

## Key Quotes
> "NO NARRATIVE DURING CHARACTER CREATION - META-GAME process only: stats, abilities, equipment. Story begins AFTER approval."

> "🚨 CRITICAL: Never Ignore Player Input - If you can't use something the player provided, you MUST: 1) Acknowledge what they requested, 2) Explain why it can't be used as-is, 3) Offer the option to override your concerns or provide alternatives"

## Connections
- [[GameStateSchemaJSON]] — game state structure that stores character data
- [[FirestoreService]] — persists character sheets and campaign state
- [[LivingWorldTriggerEvaluation]] — turn/time-based combat trigger logic

## Contradictions
- None—aligns with existing [[GameMechanicsProtocol]] entry
