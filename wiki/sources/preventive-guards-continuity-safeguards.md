---
title: "Preventive Guards - Continuity Safeguards and State Integrity Enforcement"
type: source
tags: [game-state, continuity, safeguards, anti-blitz, state-integrity, llm-hallucination]
source_file: "raw/preventive_guards.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Defensive module enforcing continuity safeguards and state integrity rules to prevent LLM hallucinations from breaking game state consistency. Serves as the LAST LINE OF DEFENSE before state changes are applied to the game, with SILENT enforcement - users never see corrections.

## Key Claims
- **Anti-Blitz Protection** — Social HP integrity enforcement prevents players from spamming social interactions to rapidly drain NPC HP. Cooldown blocking is SERVER-ENFORCED and cannot be bypassed through LLM manipulation.
- **Silent Enforcement** — Hardens structured responses to prevent backtracking WITHOUT surfacing errors to users.
- **All Safeguards Run** — Every state update MUST run ALL safeguard checks - skipping enables exploits.
- **State Changes Augmentation** — Takes raw state_updates from LLM response, applies safeguards, returns augmented dict.

## Key Functions
- `enforce_preventive_guards` — Main entry point, applies ALL safeguards
- `_ensure_social_hp_integrity` — Enforces cooldown blocking and damage caps (ANTI-BLITZ)
- `_ensure_world_time` — Prevents time travel by ensuring time progression consistency
- `_ensure_location_progress` — Tracks valid location transitions
- `_ensure_core_memory` — Deduplicates core memories
- `_ensure_resource_checkpoint` — Persists resource checkpoints
- `_ensure_dm_notes_persistence` — Preserves DM notes across turns

## Strict Boundaries
- ✅ MUST: Take raw state_updates from LLM response
- ✅ MUST: Apply continuity safeguards
- ✅ MUST: Return augmented state_changes dict
- ❌ MUST NOT: Mutate game state directly
- ❌ MUST NOT: Surface errors to users
- ❌ MUST NOT: Skip any safeguard checks

## Connections
- [[GameMechanicsProtocol]] — Character creation and combat rules this module protects
- [[NarrativeDirectives]] — Narrative generation this module defends against
- [[WorldLogic]] — Caller that applies state_changes to game state

## Contradictions
[]
