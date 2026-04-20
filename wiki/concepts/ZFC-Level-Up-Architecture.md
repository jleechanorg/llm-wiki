---
title: "ZFC Level-Up Architecture"
type: concept
tags: [level-up, zfc, architecture, model-computes, rewards, worldai]
sources: [zfc-level-up-model-computes-2026-04-19]
last_updated: 2026-04-19
---

## Overview

ZFC Level-Up Architecture replaces backend-owned level-up judgment with a ZFC-compliant contract: **the model computes level-up facts; the backend validates, formats, and delivers them**. UI renders only server-provided payloads. This is the post-2026-04-14 evolution of [[LevelUpArchitecture]].

The key contract change: XP state must be expressed as two unambiguous totals — `previous_turn_exp` and `current_turn_exp` — rather than a backend threshold check.

## Core Tenets

### 1. ZFC Boundary

The model decides:
- Whether XP was earned
- The previous XP total before this turn
- The current XP total after this turn
- Whether a level-up is available
- The target level
- Which level-up choices or benefits to present
- Whether the response should include XP-only or full level-up prompt

The backend **must not decide** those semantic facts on the model-owned path.

### 2. Centralization Boundary

One canonical backend formatting path for model-owned level-up output:

```
level_up_signal
  -> rewards_engine.format_model_level_up_signal()
  -> canonicalize_rewards()
  -> world_logic modal wrapper
  -> response/persistence
  -> app.js render
```

No other file may independently interpret level-up signal semantics, recalculate threshold crossings, or synthesize competing level-up choices.

### 3. Single Responsibility Per File

| File | One Job | Must Not Do |
|------|---------|-------------|
| `prompts/*.md` | Tell the model exactly what to compute and emit | Hide backend assumptions or conflicting direct level mutation paths |
| `narrative_response_schema.py` | Accept structured model output shape | Decide level-up, compute thresholds, mutate game state |
| `rewards_engine.py` | Deterministically format explicit signals; preserve legacy fallback during migration | Make semantic level-up decisions on `level_up_signal` path, call model, persist state |
| `world_logic.py` | Wrap precomputed payloads with modal/story response semantics | Recompute rewards, detect thresholds, build level-up choices independently |
| `game_state.py` | Store state and provide deterministic mechanical primitives for legacy paths | Interpret model text or own new-path level-up decisions |

## Canonical Model Output

When XP is awarded (or level-up is otherwise relevant), the model emits `level_up_signal`:

**Level-Up Available:**
```json
{
  "level_up": true,
  "new_level": 5,
  "previous_turn_exp": 6200,
  "current_turn_exp": 6500,
  "total_exp_for_next_level": 6500,
  "additional_exp_to_next_level": 0,
  "source": "combat",
  "choices": [
    {"type": "hp", "description": "Gain hit points for Level 5"},
    {"type": "class_feature", "description": "Extra Attack"},
    {"type": "spellcasting", "description": "Unlock 3rd-level spell slots"}
  ],
  "rewards": {"gold": 150, "loot": ["Potion of Healing"]}
}
```

**XP Award Without Level-Up:**
```json
{
  "level_up": false,
  "current_level": 1,
  "next_level": 2,
  "previous_turn_exp": 200,
  "current_turn_exp": 250,
  "total_exp_for_next_level": 300,
  "additional_exp_to_next_level": 50,
  "source": "encounter",
  "rewards": {"gold": 0, "loot": ["None"]}
}
```

## Field Semantics

| Field | Required When | Meaning |
|-------|---------------|---------|
| `level_up` | Always | Model decision. `true` = present level-up UI; `false` = XP/rewards only. |
| `new_level` | `level_up=true` | Target level to offer. Must be 1–20. |
| `previous_turn_exp` | XP awarded | Total character XP before this user turn. |
| `current_turn_exp` | XP awarded | Total character XP after this user turn. |
| `total_exp_for_next_level` | XP awarded | Total lifetime XP threshold for `next_level`. |
| `additional_exp_to_next_level` | XP awarded | Remaining XP delta from `current_turn_exp` to `total_exp_for_next_level`. |
| `choices` | `level_up=true` only | Model-owned level-up choices. Must be omitted for `level_up=false`. |

## Fail-Closed Rules

| Case | Behavior |
|------|----------|
| `level_up=true` without `new_level` | Return `(None, None)`. Do not derive target level. |
| `level_up=true` with `new_level > 20` | Return `(None, None)`. Do not surface invalid level UI. |
| `level_up=true` without XP totals | Return `(None, None)`. Do not synthesize `0/0` progress. |
| `level_up=false` with `choices` | Drop choices. No `level_up_choices` in `rewards_box`. |
| Malformed false signal | Fall back to raw `rewards_box` if present. |

## Stage Pipeline (Streaming + Non-Streaming)

```
Stage 1: PROMPT          prompt files             -> model contract
Stage 2: MODEL           LLM                      -> level_up_signal
Stage 3: PARSE           narrative_response_schema.py -> typed response
Stage 4: EXTRACT         structured_fields_utils.py  -> structured_fields
Stage 5: FORMAT          rewards_engine.py        -> rewards_box/planning_block
Stage 6: MODAL WRAP      world_logic.py           -> modal lock/finish semantics
Stage 7: PERSIST/RETURN  llm_parser.py           -> Firestore + API/SSE payload
Stage 8: RENDER         frontend                 -> display only
```

Transport is allowed to differ; semantic and formatting code is **not**.

## Relationship to Pre-ZFC LevelUpArchitecture

The 2026-04-14 [[LevelUpArchitecture]] correctly centralized scattered rewards logic into `rewards_engine.py`, but still treated the server as the place that **decides** whether a player should level up. That violated ZFC byputting semantic judgment (threshold crossing detection) in application code.

ZFC Level-Up Architecture fixes this by shifting the semantic decision to the model while keeping the backend as a pure formatter boundary.

## See Also
- [[ZeroFrameworkCognition]] — ZFC framework this architecture is built on
- [[LevelUpArchitecture]] — pre-ZFC architecture this evolved from
- [[RewardsEngine]] — the single backend file that owns all reward/level-up formatting
- [[FailClosedValidation]] — validation philosophy for malformed model signals
- [[SemanticVsMechanicalJudgment]] — the dividing line this architecture enforces
