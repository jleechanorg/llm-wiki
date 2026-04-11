---
title: "Circuit Breaker Agent Selection"
type: concept
tags: [agent-selection, infinite-loop, reliability, safety-net]
sources: []
last_updated: 2026-04-11
---

## Description
An agent selection circuit breaker prevents an agent from being selected too many consecutive times, which can cause infinite loops or starvation of other agents.

## Pattern
Agent matching logic (`matches_game_state()`) can return `True` indefinitely if its guard condition never flips. Without a circuit breaker, a single agent can be selected 50+ consecutive times.

## Symptoms
- Single agent selected 52+ consecutive times ( RewardsAgent in campaign kuXKa6vrYY6P99MfhWBn)
- `combat_state.rewards_processed` stuck at `False` — guard never transitions
- All other agent types starved — no chance to process the stuck state

## Root Cause
Agent routing has no per-agent consecutive-selection cap. Only the matching guard condition controls selection. If the state never changes, the same agent wins every turn.

## Fix
Add a circuit breaker at the selection layer:
```python
# Per-agent consecutive selection cap
MAX_CONSECUTIVE_SAME_AGENT = 3
if agent == last_agent and consecutive_count >= MAX_CONSECUTIVE_SAME_AGENT:
    return None  # skip this agent, let others run
```

## Connections
- [[DeterministicFeedbackLoops]] — related: feedback loop without termination
- [[LLM-as-Judge-Pattern]] — monitoring layer that should detect this
- [[Compound-Loops]] — related: nested retry loops without exit condition
