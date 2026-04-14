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

## Rewards Engine Idempotency Requirement

When called by this protocol, `rewards_engine` **must be idempotent**: `canonicalize_rewards(x, y, z) == canonicalize_rewards(x, y, z)` regardless of how many times called. This is critical because the protocol runs every 10 turns — calling rewards logic multiple times must NOT double-count XP or loot. See [[RewardsEngineIdempotency]] for full details.

The idempotency invariant is achieved in v4 design via the [[SingleResponsibilityPipeline]] which calls `rewards_engine` exactly once per request, using a pre-LLM snapshot (`original_state_dict`) to detect whether state actually changed.

## Related Concepts

- [[Rewards Box]] — JSON output structure for deferred rewards
- [[Rewards Processed Flag]] — state tracking to prevent double-counting
- [[XP Verification]] — secondary heuristic when flags are ambiguous
- [[Level-Up Detection]] — automatic detection when deferred XP triggers level-up
- [[RewardsEngineIdempotency]] — idempotency requirement for rewards_engine called by this protocol
- [[SingleResponsibilityPipeline]] — v4 pipeline design: single call per request, no re-canonicalization
- [[RewardsBoxAtomicity]] — atomic pair enforcement for rewards_box + planning_block
- [[LevelUpCodeArchitecture]] — v3 architecture precedent
- [[Level-Up PR Chain Analysis (PRs #6262-#6268)]] — all broken PRs closed by v4 design
- [[Rewards Engine v4 Design|sources/level-up-engine-v4-design.md]] — canonical source document
