---
title: "Rewards Box Observability"
type: concept
tags: [rewards, observability, metrics, monitoring, worldai]
last_updated: 2026-04-14
---

## Summary

RewardsBox Observability is the set of practices for understanding what happens inside the rewards computation pipeline — tracking rewards flows, detecting anomalies, and debugging unexpected values.

## Key Metrics

**Rewards volume**:
- Total rewards issued per campaign per day
- Distribution of reward sizes
- Anomalous spikes or drops

**Processing latency**:
- Time from LLM response to rewards box update
- Time from user action to rewards reflected in UI

**Error rates**:
- Failed normalization attempts
- Schema validation failures
- Timeout rates in rewards computation

## Tracing

Every rewards box update should emit a trace:
```python
with tracer.start_span("rewards_box_update") as span:
    span.set_attribute("campaign_id", campaign_id)
    span.set_attribute("player_id", player_id)
    span.set_attribute("rewards_delta", delta)
    span.set_attribute("source", source)
    # ... computation ...
    span.set_attribute("final_rewards", final_total)
```

## Dashboards

Key dashboards for rewards observability:
1. **Rewards flow** — Real-time rewards pipeline throughput
2. **Anomaly detection** — Unusual rewards patterns
3. **Schema compliance** — Normalization success rate

## Alerting

Alert on:
- Normalization failure rate > 1%
- Rewards value out of expected range [0, MAX_REWARDS]
- Processing latency p99 > 5s

## Connections
- [[RewardsBoxSchema]] — Schema definition
- [[RewardsBoxAtomicity]] — Atomic update semantics
- [[StreamingPassthroughNormalization]] — Normalization pipeline
