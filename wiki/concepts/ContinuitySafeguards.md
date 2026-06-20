---
title: "Continuity Safeguards"
type: concept
tags: [game-state, integrity, llm-defense, safeguards]
sources: [preventive-guards-continuity-safeguards]
last_updated: 2026-04-08
---

## Summary
Continuity Safeguards are defensive rules enforced by the Preventive Guards module to maintain game state consistency. They prevent LLM hallucinations from introducing backtracking, state inconsistencies, and exploits.

## Scope
- Social HP integrity enforcement (ANTI-BLITZ)
- World time consistency and progression
- Location progress tracking
- Core memory deduplication
- Resource checkpoint persistence
- DM notes persistence metadata
- God mode response extraction

## Implementation
The `enforce_preventive_guards` function applies ALL safeguards to every state update, returning an augmented state_changes dict. Callers MUST apply these changes to game state.

## Related Concepts
- [StateIntegrityEnforcement](StateIntegrityEnforcement.md) — The broader category of integrity enforcement
- [PreventiveGuards](../entities/PreventiveGuards.md) — The module implementing these safeguards
- [AntiBlitzProtection](AntiBlitzProtection.md) — Specific safeguard against Social HP exploits
