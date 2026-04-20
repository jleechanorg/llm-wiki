---
title: "ZFC North Star"
type: concept
tags: [zfc, architecture, model-computes]
sources: [zfc-level-up-model-computes-north-star-2026-04-19]
last_updated: 2026-04-20
---

**ZFC North Star** — The architectural principle that under Zero Framework Cognition, the model computes semantic game state and the backend is pure formatter.

## Core Contract

```
Model owns semantic level-up computation.
Backend owns deterministic validation, formatting, persistence, and delivery.
UI owns rendering only.
```

## Model Output Schema

The model must output structured data:
- `level_up: bool` — whether character leveled up
- `new_level: int` — the new level (if leveled up)
- `previous_turn_exp: int` — total character XP before the current user turn
- `current_turn_exp: int` — total character XP after the current user turn
- `choices: [...]` — available player choices
- `rewards: {...}` — rewards box content

## Backend Contract

The backend (`rewards_engine.py`) acts as pure formatter:
- Parse model output
- Validate required fields
- Format UI structures (`rewards_box`, `planning_block`)
- Compute deterministic display values:
  - `xp_gained = current_turn_exp - previous_turn_exp`
  - `progress_percent = current_turn_exp / total_exp_for_next_level`

## Fail-Closed Rules

- If a true level-up signal is missing required fields → fail closed by suppressing the malformed level-up UI
- If model output is malformed → do not attempt repair, fail closed
- Never infer level-up from threshold crossings (model computes)

## Connections

- [[ZeroFrameworkCognition]] — governing principle
- [[ModelComputes]] — technical implementation pattern
- [[BackendFormats]] — backend responsibility
- [[RewardsEngineArchitecture]] — rewards_engine.py role
