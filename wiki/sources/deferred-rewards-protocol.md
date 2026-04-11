---
title: "Deferred Rewards Protocol"
type: source
tags: [game-mechanics, dnd, rewards, xp-system, worldarchitect]
source_file: "raw/deferred-rewards-protocol.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Protocol that runs every 10 player turns (excluding GOD mode) to catch XP and loot rewards that may have been missed during normal gameplay. Scans recent story events and fills gaps WITHOUT double-counting already processed rewards.

## Key Claims
- **Automatic Execution**: Runs every 10 scenes (turn_number % 10 == 0), executes within same LLM call as story generation without interrupting narrative
- **Deduplication First**: Uses `rewards_processed` flags as primary deduplication; XP verification as secondary heuristic when flags are ambiguous
- **Reward Categories**: Checks combat victories, encounter completions, quest milestones, and social/roleplay awards for unprocessed rewards
- **State Integration**: Sets `rewards_processed: true` after awarding to prevent future double-counting

## Key Quotes
> "Fill gaps in rewards WITHOUT double-counting what was already awarded."

> "NEVER double-count - Always verify rewards_processed flags"

## Connections
- [[XP System]] — experience point tracking and level-up mechanics
- [[Combat System Protocol]] — combat victory rewards processing
- [[Rewards Box]] — JSON structure for deferred reward output

## Contradictions
- None detected
