---
title: "Model Computes"
type: concept
tags: [zfc, architecture, model, semantic-judgment]
sources: [zfc-level-up-model-computes-north-star-2026-04-19]
last_updated: 2026-04-20
---

**Model Computes** — ZFC architectural pattern where the LLM owns semantic judgment, as opposed to backend inference from text.

## Definition

The model computes pattern means the LLM is responsible for:
- XP totals before and after the current turn
- Level-up threshold detection
- Reward eligibility determination
- Choice generation
- Narrative content generation

Instead of backend code scanning prompt output for keywords like `_has_rewards_narrative`, the model is prompted to output explicit structured data.

## Background

The pre-ZFC approach had backend code (`world_logic.py`) scanning model output for keywords to detect rewards eligibility. This is a critical ZFC violation — semantic judgment must be delegated to the model, not performed by application code.


## Implementation

Model prompt includes explicit schema asking for:
```json
{
  "level_up": true/false,
  "new_level": 5,
  "previous_turn_exp": 850,
  "current_turn_exp": 1000,
  "choices": [...],
  "rewards": {...}
}
```

Backend validates and formats this output for UI.

## Connections

- [[ZFCNorthStar]] — architectural principle
- [[BackendFormats]] — complementary pattern
- [[RewardsBox]] — UI structure for rewards display
- [[PlanningBlock]] — UI structure for choice planning
