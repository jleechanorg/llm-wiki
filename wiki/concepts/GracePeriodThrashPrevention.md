---
title: "Grace Period Thrash Prevention"
type: concept
tags: [pairv2, feature-pattern, automation]
sources: []
last_updated: 2026-04-13
---

## Description

The grace period thrash prevention pattern adds a delay after restarting a stuck agent before re-checking for stalls. This prevents the system from repeatedly restarting the same agent in a tight loop, known as thrashing.

## Why It Matters

When an agent stalls and is restarted, immediately checking for stall again can cause thrashing — the system keeps restarting the agent without giving it time to make progress. A grace period allows the restarted agent time to execute meaningful work before being checked again.

## Key Technical Details

- **Grace period duration**: 60 seconds (PAIRV2_RESTART_GRACE_SECONDS = 60)
- **Per-agent tracking**: Each agent has its own grace period timer
- **Scope**: `.claude/pair/pair_execute_v2.py`
- **Related concepts**: AgentStallRecovery

## Related Beads

- BD-pairv2-monitor-restart
