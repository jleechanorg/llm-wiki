---
title: "RewardsAgent"
type: entity
tags: [worldarchitect.ai, agent-architecture, rewards]
sources: [feedback-2026-08-23-verify-agent-call-independence-empirically]
last_updated: 2026-08-23
---

## Summary

`RewardsAgent` is one of WorldArchitect.AI's "secondary agent" turn types
(alongside faction, dialog, dialog_heavy, and combat). It **replaces**
`StoryModeAgent` for a turn when routed — mutually-exclusive routing, not a
concurrent call. `DeferredRewardsAgent` is a variant that injects rewards
instructions into the same `StoryModeAgent` LLM call via prompt injection
(its own docstring: "Runs IN PARALLEL with story mode (same LLM call)"),
which is a different mechanism from RewardsAgent's turn-level replacement.

Confirmed empirically: a BigQuery join on
`worldarchitecture-ai.llm_forensics.llm_payloads` by
`(campaign_id, turn_index)` over a 14-day window found only 1 of 161
RewardsAgent turns also had a StoryModeAgent row at the same turn (160/161
mutual exclusivity) — see
[[feedback-2026-08-23-verify-agent-call-independence-empirically]].

## Known limitation

`DeferredRewardsAgent` hardcodes `agent_mode=MODE_REWARDS` even when the
underlying call is really a story-mode call carrying extra rewards content
— flagged as a possible mode-tagging mismatch for PR #9137's circuit-
breaker degradation logic (which keys degrade-vs-hard-fail behavior off
`agent_mode`). Tracked as bead `rev-oyjx5`, not yet fixed.

Updated with MechanicalAgent pattern reference and design constraints (see
prior wiki history for that note's original source, not re-derived here).

## Connections

- [[EmpiricalConcurrencyVerification]] — the verification pattern this
  entity's investigation established
- [[worldarchitect.ai]]
