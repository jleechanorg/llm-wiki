---
title: "Spell Validation"
type: concept
tags: [game-state, validation, spells, dnd-5e]
sources: ["game-state-examples"]
last_updated: 2026-04-08
---

## Description
System for validating spell casting in WorldArchitect.AI, tracking available spell slots per level and enforcing slot availability rules.

## Validation Rules
1. **Slot Tracking**: Monitor available slots per spell level
2. **Exhaustion Rejection**: Cannot cast if slot level exhausted
3. **Upcasting**: Higher-level slot can replace lower-level slot

## Upcasting Logic
- Player has L2 slot but no L1
- Player attempts to cast L1 spell (Healing Word)
- System prompts: can use L2 slot instead (upcast)

## Connection to D&D 5E
Implements standard D&D spell slot mechanics:
- Spell levels 1-9
- Slot consumption on casting
- Upcasting at higher levels

## Connections
- [[DNDSRD]] — core spellcasting rules
- [[GameStateSchema]] — spell slot tracking in character data
- [[GameStateExamples]] — spell validation examples
