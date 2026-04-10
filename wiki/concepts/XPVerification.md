---
title: "XP Verification"
type: concept
tags: [game-mechanics, xp, deduplication]
sources: [deferred-rewards-protocol]
last_updated: 2026-04-08
---

XP Verification is the secondary deduplication heuristic used when `rewards_processed` flags are insufficient or ambiguous.

## When Used

- `rewards_processed` flag is missing from state
- Flag state is ambiguous (e.g., true but XP unchanged)
- As a sanity check alongside flag verification

## Algorithm

1. Calculate expected XP from all eligible events
2. Check current player XP (`player_character_data.experience.current`)
3. Award DIFFERENCE between expected and actual
4. If player already has expected XP, award 0

## Examples

**Already processed:**
- Combat should have awarded 100 XP
- Player already has 100 XP more than before combat
- Award: 0 XP

**Missed reward:**
- Combat should have awarded 100 XP
- Player XP unchanged from before combat
- Award: 100 XP

## Related Concepts

- [[Deferred Rewards Protocol]] — protocol that uses this verification
- [[Rewards Processed Flag]] — primary deduplication mechanism
