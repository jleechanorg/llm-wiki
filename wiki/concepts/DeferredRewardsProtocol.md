---
title: "Deferred Rewards Protocol"
type: concept
tags: [game-mechanics, rewards, protocol]
sources: [deferred-rewards-protocol]
last_updated: 2026-04-08
---

The Deferred Rewards Protocol is a background system in WorldArchitect.AI that runs every 10 player turns to ensure players receive XP and loot they may have missed during normal gameplay.

## How It Works

1. **Trigger**: Runs automatically when `turn_number % 10 == 0` (GOD mode turns excluded)
2. **Scan**: Checks recent story for reward-eligible events not yet processed
3. **Deduplicate**: Verifies `rewards_processed` flags before awarding
4. **Award**: Fills gaps via `rewards_box` in response, integrating naturally into narrative

## Key Principle

> Fill gaps in rewards WITHOUT double-counting what was already awarded.

## Related Concepts

- [[Rewards Box]] — JSON output structure for deferred rewards
- [[Rewards Processed Flag]] — state tracking to prevent double-counting
- [[XP Verification]] — secondary heuristic when flags are ambiguous
- [[Level-Up Detection]] — automatic detection when deferred XP triggers level-up
