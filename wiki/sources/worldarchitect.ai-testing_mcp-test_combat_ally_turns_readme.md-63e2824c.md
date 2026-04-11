---
title: "Combat Ally Turns & Resource Visibility Test"
type: source
tags: [testing, combat, dnd, worldarchitect, e2e, ally-turns, resource-display]
sources: []
date: 2026-04-07
source_file: testing_mcp/test_combat_ally_turns.py
last_updated: 2026-04-07
---

## Summary
End-to-end test validating two critical combat issues: (1) allies taking automatic turns in initiative order, and (2) combat resource visibility (HP, AC, actions). Tests reproduce bugs from user combat logs where the LLM allowed multiple consecutive player turns without processing ally/enemy turns, and provided no combat status display.

## Key Claims
- **Issue 1 - Automatic Ally Turns**: The LLM allows the player to take multiple consecutive turns without processing ally or enemy turns, violating D&D 5E initiative order. Evidence: player took Divine Smite attack, then Shove attempt without any other combatant turns between them.
- **Issue 2 - No Resource Visibility**: Throughout combat, there is NO display of player HP vs max HP, remaining actions/bonus actions, enemy HP/AC/levels, or ally HP/status. Player cannot make informed tactical decisions.
- **Test Coverage**: Test verifies at least one ally turn appears in Round 2 narrative and that combat remains active. Also verifies round header + initiative display + combatant status lines (HP/AC/status).

## Key Quotes
> "**ROUND 3 - Initiative Order:** 🗡️ Kira (PC) - HP: 28/35 - [ACTIVE] ⚔️ Goblin Boss - HP: 22/45 - [Bloodied] 🐺 Wolf Companion - HP: 8/11 - [OK] 💀 Goblin 1 - HP: 0/7 - [Defeated] ⚔️ Goblin 2 - HP: 4/7 - [Wounded]" — Expected combat status format per combat_system_instruction.md:534-542

> "make sure my team is also taking combat turns automatically" — User god mode intervention required to trigger ally turns

## Connections
- [[Character Creation Flow Paths]] — Same testing_mcp directory, similar E2E test structure
- [[Testing MCP - Server-Level Tests with Real LLMs]] — Parent testing framework with no-mocks policy
- [[Preventing Scene Backtracking and Missed God-Mode Corrections]] — Related to god mode intervention patterns

## Contradictions
- None identified - this is a new test source documenting previously untested combat behavior
