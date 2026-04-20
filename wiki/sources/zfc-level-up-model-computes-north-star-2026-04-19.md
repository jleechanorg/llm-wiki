---
title: "ZFC Level-Up Architecture: Model Computes, Backend Formats — 2026-04-19"
type: source
tags: [zfc, architecture, level-up, rewards, model-computes]
date: 2026-04-19
source_file: roadmap/zfc-level-up-model-computes-2026-04-19.md
---

## Summary

The correct architecture under Zero Framework Cognition (ZFC) is **model computes level-up and rewards; backend is pure formatter**. The model outputs structured data with unambiguous XP totals (`{level_up: bool, new_level: int, previous_turn_exp: int, current_turn_exp: int, choices: [...], rewards: {...}}`); the backend (`rewards_engine.py`) parses and formats this into UI structures (`rewards_box` / `planning_block`). This makes backend-centralization that owns signal detection via `resolve_level_up_signal` the wrong target for new model-owned responses. Legacy fallback and stale-flag guards remain transitional compatibility code until characterization tests and live evidence prove safe deletion.

## Key Claims

- Model computes XP totals, detects level-up threshold, decides rewards — this is semantic judgment that belongs in the model, not Python
- Backend is pure formatter: parse model output, validate fields, format UI structures
- `_has_rewards_narrative` keyword scan in `world_logic.py` is a critical ZFC violation — fixed by LLM delegation
- `resolve_level_up_signal` triplication across `rewards_engine.py` / `game_state.py` / `world_logic.py` disappears from the model-owned path under model-computes — the function is quarantined as legacy before deletion
- `intent_classifier.py` FastEmbed classifier is an allowed ZFC exception — pure vector math (cosine similarity), not semantic judgment
- PRs #6370/#6377/#6379/#6387 are stale under this model — they fix bugs in the wrong architecture

## Key Quotes

> "Backend: XP math → detects level-up → builds UI pair → calls LLM for narrative" — current broken architecture

> "Model: computes XP, detects level-up, decides rewards → structured output; Backend: parses model output → formats rewards_box / planning_block UI" — ZFC-correct architecture

> "What `rewards_engine.py` does NOT do on the model-owned path: no semantic XP judgment, no level-up threshold detection, no class-benefit synthesis when model choices are missing." — formatter contract

## Connections

- [[ScopeDrift]] — PR #6370 scope drift is symptomatic of backend-centralization approach
- [[LevelUpCentralization]] — the Layer 2 centralization contract is irrelevant under model-computes
- [[ZeroFrameworkCognition]] — the governing architectural principle
- [[RewardsEngineArchitecture]] — rewards_engine.py transitions from business-logic owner to pure formatter
