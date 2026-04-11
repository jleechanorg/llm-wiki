---
title: "MVP Site Prompts - Character Template & Game State Protocols"
type: source
tags: [mvp-site, character-template, dnd-srd, game-state, dice-mechanics, rpg-development]
sources: []
source_file: world_reference/mvp_site_prompts_merged.md
date: 2026-04-07
last_updated: 2026-04-07
---

## Summary

This merged document contains three core prompt templates for building RPG game systems: a comprehensive character profile template with internal MBTI/alignment tracking, D&D 5E SRD system authority rules, and a critical game state management protocol enforcing mandatory dice rolling and state integrity. Together they form the foundation for AI-driven D&D game masters.

## Key Claims

- **Character Template**: Comprehensive framework with core identity, psychology (motivation, fear, traits), behavior under stress, speech patterns, backstory, and game mechanics. MBTI/alignment tracked internally only—never appears in narrative.
- **D&D 5E SRD Authority**: Mechanical rules override narrative preferences for all mechanical conflicts. Standard attributes (STR, DEX, CON, INT, WIS, CHA) with custom systems allowed per DM judgment.
- **Critical Dice Rule**: Dice values are UNKNOWABLE—must use tool_requests to OBSERVE actual rolls. Cannot predict, estimate, or fabricate results. Combat attacks MUST use dice tools.
- **Damage Validation**: Max Sneak Attack = 10d6 (20d6 on crit). All damage calculations must be verified.
- **Entity ID Format**: Required format `type_name_###` for all state updates.
- **Planning Block**: Thinking + snake_case choice keys with risk levels required in JSON responses.
- **Modes**: STORY (default), GOD (admin), DM (OOC/meta discussion).

## Key Quotes

> "Show personality through specific actions, objects, and speech patterns—not labels." — Character prose example technique

> "ABSOLUTE RULE: You cannot know dice values without executing tools to OBSERVE them." — Game State Protocol

> "🎲 DICE VALUES ARE UNKNOWABLE: You CANNOT predict, estimate, or fabricate dice results. Use tools to OBSERVE them." — ESSENTIALS directive

## Connections

- [[DungeonsAndDragons]] — 5E SRD rules foundation
- [[GameMaster]] — character template for NPC creation
- [[CharacterCreation]] — framework for player characters

## Contradictions

- None identified — these are foundational system prompts, not conflicting sources.