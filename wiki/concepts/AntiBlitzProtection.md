---
title: "Anti-Blitz Protection"
type: concept
tags: [anti-exploit, game-balance, server-enforcement, social-combat]
sources: [preventive-guards-continuity-safeguards]
last_updated: 2026-04-08
---

## Summary
Anti-Blitz Protection is a specific safeguard within Preventive Guards that prevents players from spamming social interactions to rapidly drain NPC Social HP. This protection is SERVER-ENFORCED and cannot be bypassed through LLM manipulation or prompt engineering.

## Mechanism
The `_ensure_social_hp_integrity` function:
1. Checks if cooldown is active (cooldown > 0)
2. If cooldown active, forces damage to 0 (blocks attack)
3. Caps damage at current HP (prevents over-damage exploits)

## Why Server-Enforced
Unlike prompt-based restrictions, server-enforced cooldown blocking operates at the code level after LLM response generation, making it impossible to bypass through prompt engineering.

## Related Concepts
- [[SocialHP]] — The mechanic being protected
- [[ContinuitySafeguards]] — The broader safeguard system
- [[PreventiveGuards]] — The module implementing this protection
