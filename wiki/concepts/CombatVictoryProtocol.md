---
title: "Combat Victory Protocol"
type: concept
tags: [combat, dnd-5e, xp-rewards]
sources: []
last_updated: 2026-04-08
---

## Definition
Protocol for processing combat end state, including XP calculation, state updates, and victory narration. MUST execute before any post-combat actions (loot, interrogation, etc.).

## Execution Order (Non-Negotiable)
1. Set `combat_phase: "ended"` in state_updates
2. Set `combat_summary: { xp_awarded: <sum of enemy CR XP>, enemies_defeated: [...] }`
3. Update `player_character_data.experience.current` with SAME xp_awarded value
4. Display COMBAT VICTORY box in narrative with XP breakdown
5. Then narrate loot/interrogation/victory

## Critical Rules
- XP value in combat_summary.xp_awarded MUST match XP added to experience.current
- XP breakdown MUST appear in narrative text (users cannot see state_updates)
- User commands do NOT override this protocol

## Related Concepts
- [[CombatSystemProtocol]] — parent protocol
- [[XP Awarding]] — mechanics of computing combat XP
