---
title: "State Integrity Enforcement"
type: concept
tags: [game-state, integrity, llm-defense, anti-hallucination]
sources: [preventive-guards-continuity-safeguards]
last_updated: 2026-04-08
---

## Summary
State Integrity Enforcement is the practice of hardening LLM-generated state changes before they are applied to the game. The Preventive Guards module serves as the LAST LINE OF DEFENSE in this enforcement chain.

## Key Principles
- **Take Raw Updates** — Accept state_updates from LLM response as potentially containing hallucinations
- **Apply Safeguards** — Run continuity checks (cooldown blocking, time progression, damage capping)
- **Silent Correction** — NEVER surface errors to users - apply corrections transparently
- **Complete Execution** — ALL safeguards MUST run on EVERY state update


## Violation Consequences
Skipping safeguards enables: game state inconsistency, exploit development (Social HP blitzing), and time travel bugs.

## Related Concepts
- [[ContinuitySafeguards]] — The specific safeguards enforced
- [[LLMResponse]] — Source of potentially hallucinated state updates
- [[GameState]] — Target of enforced state changes
