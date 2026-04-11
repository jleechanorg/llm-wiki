---
title: "Combat Turn Management & Resource Visibility Fix"
type: source
tags: [combat-system, dnd, bug-fix, turn-management, resource-visibility]
source_file: "raw/combat-turn-management-resource-visibility-fix.md"
sources: []
last_updated: 2026-04-07
---

## Summary
Fixes two critical combat bugs: (1) allies and enemies not taking automatic turns in initiative order, and (2) no combat resource visibility (HP, AC, actions) displayed to players. Implementation updates combat_system_instruction.md and narrative_system_instruction.md with mandatory turn processing and status block display rules.

## Key Claims
- **Bug 1 (No Automatic Turns)**: Root cause was lack of explicit requirement to process ALL combatants in initiative order; players could take consecutive turns without god mode intervention
- **Bug 2 (No Resource Visibility)**: Combat status display was suggested but not mandatory; players had no visibility into HP, AC, actions remaining, enemy stats, or ally status
- **Fix 1**: Added ABSOLUTE RULE in combat instructions requiring ALL combatants must take turns in strict initiative order with FORBIDDEN consecutive player turns
- **Fix 2**: Added CRITICAL REQUIREMENT for combat status block at START of EVERY round with formatted template showing all combatant info
- **Implementation**: Updated both combat_system_instruction.md (lines 15-61, 585-644) and narrative_system_instruction.md (line 19)

## Key Quotes
> "ALL combatants must take turns in strict initiative order"
> "FORBIDDEN: Consecutive player turns"
> "Display status block at START of EVERY round (MANDATORY)"

## Connections
- [[Initiative Order]] — core combat mechanic driving turn processing
- [[Combat Status Display]] — resource visibility requirement for players
- [[Turn Processing]] — systematic approach to handling all combatant actions

## Contradictions
- []
