---
title: "Level-Up Centralization Learning 2026-04-17"
type: source
tags: [worldarchitect-ai, level-up, centralization, behavioral-equivalence, harness-learning]
date: 2026-04-17
source_file: raw/level-up-centralization-learning-2026-04-17.md
sources:
  - level-up-pr-drift-root-cause-harness-2026-04-17.md
  - level-up-engine-single-responsibility-design-2026-04-14.md
last_updated: 2026-04-17
---

## Summary

The reusable learning from the level-up PR drift is that centralization must be proven by behavioral equivalence and real integration evidence, not by design intent, grep gates, or similar function names. In this case, `rewards_engine.py` and `world_logic.py` had adjacent responsibilities but different semantics: causal XP-threshold computation versus stateful modal recovery and persisted-story projection. Agents drifted because they followed the target architecture language without first proving the old and new behavior matched.

## Key Claims

- Design-doc centralization is a target, not proof of replacement.
- Gated grep/import checks are insufficient for stateful behavior migration.
- Any level-up/rewards ownership move must include a behavioral-equivalence table across representative game states.
- `world_logic.py` changes can be legitimate when they are explicitly narrow modal/state recovery exceptions.
- Real-server real-LLM `testing_mcp` strict, stale-pending, and streaming evidence is required before claiming all level-up bugs are fixed.
- Autor-tagged/titled PRs are separate experiment artifacts and should not drive the level-up bugfix disposition unless explicitly promoted.

## Key Quotes

> "Centralization is complete only when the replacement path proves behavioral equivalence across the real states the old path handled."

> "The agent error was treating the roadmap as target-state truth and the current code as incidental."

## Connections

- [[BehavioralEquivalenceAudit]] - required preflight before replacement/deletion claims.
- [[LevelUpCodeArchitecture]] - architecture target and responsibility split.
- [[LevelUpVerificationStatus]] - evidence model for strict/stale/streaming proof.
- [[PR-6276-Worldarchitect]] - merged partial centralization case study.
- [[PR6339]] - reference/evidence branch.
- [[PR6351]] - current port attempt requiring cleanup/proof.
