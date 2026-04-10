---
title: "Spy Operations"
type: concept
tags: [game-mechanics, intel, faction-management, stealth]
sources: []
last_updated: 2026-04-08
---

Mechanics for deploying spies in the WorldAI Faction Management system. Includes detection risk calculation and intel gathering based on spy count, target defenses, and modifier bonuses.

## Key Formulas
- Detection Risk: 30% base + target defenses - attacker bonuses, clamped 5-90%
- Spy Strength: spies × (1 + spymaster_mod × 0.1 + lineage_intrigue × 0.15)
- Intel tiers determined by spy strength vs target defense ratio

## Related Concepts
- [[ShadowNetworks]] — target counter-intel capability
- [[Wards]] — magical detection protection
- [[Spymaster]] — council position providing intel bonuses
- [[LineageIntrigue]] — lineage track level for intrigue bonuses
