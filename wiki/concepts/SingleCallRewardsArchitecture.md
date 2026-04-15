---
title: "Single Call Rewards Architecture"
type: concept
tags: [rewards, architecture, single-call, worldai]
last_updated: 2026-04-14
---

## Summary

Single Call Rewards Architecture is a design principle that a player's rewards state should be updated in exactly one atomic operation per action, rather than multiple sequential updates.

## The Problem

Without single-call atomicity:
```
Action: Roll a natural 20 (3x rewards bonus)
Without: 
  1. Update rewards +base (step 1)
  2. Update rewards +bonus (step 2)  ← interleaved with another action
  3. Update level (step 3)
With interleaving: player sees partial rewards, wrong level

```

## The Solution

Exactly one Firestore document update per action:

```python
async def process_dice_roll(campaign_id: str, player_id: str, roll: DiceRoll) -> RewardsBox:
    # Single atomic transaction
    async with firestore.transaction():
        current = await get_rewards_box(campaign_id, player_id)
        updated = compute_new_state(current, roll)
        # ONE write, not multiple
        await set_rewards_box(campaign_id, player_id, updated)
    return updated
```

## Why This Matters

1. **No partial states visible** — Player always sees consistent state
2. **Simpler reasoning** — No need to track "which step are we on"
3. **Rollback simplicity** — Single abort undoes everything

## Connections
- [[RewardsBoxAtomicity]] — Atomicity patterns
- [[RewardsBoxSchema]] — Schema definition
- [[StateTransitions]] — State management
