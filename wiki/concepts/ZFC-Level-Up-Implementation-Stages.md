---
title: "ZFC Level-Up Implementation Stages"
type: concept
tags: [level-up, implementation, zfc, migration, worldai]
sources: [zfc-level-up-model-computes-2026-04-19]
last_updated: 2026-04-19
---

## Overview

The ZFC Level-Up implementation follows a deliberately cleanup-first 5-stage plan to avoid the ambiguity trap of the 2026-04-14 stack: adding new centralization layers while old recovery paths stayed alive, making every test failure ambiguous — either the model contract was wrong, the formatter was wrong, or a legacy repair path quietly rewrote the result.

## Stage 0: Delete No-Op and Duplicate Logic First

**Goal**: Reduce live level-up logic before adding more behavior.

**Scope**:
- Remove transient review/trigger comments and no-op scaffolding
- Delete or quarantine unreachable legacy branches inside `rewards_engine._canonicalize_core()`
- Isolate `project_level_up_ui()` behind a transitional call site
- Classify every `resolve_level_up_signal()` call site as: keep (legacy compat), replace (with formatter), or delete (signal already explicit)

**Acceptance**: Grep returns no tracked transient scaffolding; doc lists every remaining legacy call site with rationale.

## Stage 1: MVP Real-Model Compliance Probe

**Goal**: Measure whether the LLM reliably computes level-up facts before deleting legacy safety nets.

**MVP contract** — two canonical signals:

```json
// XP award without level-up
{ "level_up": false, "previous_turn_exp": 200, "current_turn_exp": 250,
  "xp_to_next_level": 300, "source": "encounter",
  "rewards": { "gold": 0, "loot": ["None"] } }

// Level-up available
{ "level_up": true, "new_level": 5, "previous_turn_exp": 6200,
  "current_turn_exp": 6500, "xp_to_next_level": 6500, "source": "combat",
  "choices": [{"type": "class_feature", "description": "Extra Attack"}],
  "rewards": { "gold": 150, "loot": ["Potion of Healing"] } }
```

**Compliance counts to record**:
- Valid signal
- Missing `previous_turn_exp`
- Missing `current_turn_exp`
- Inconsistent `current_turn_exp < previous_turn_exp`
- True level-up without `new_level`
- True level-up without choices

**Acceptance**: Real streaming evidence shows model emits new fields; formatter rejects malformed true signals; failures classified as model-compliance, not hidden by backend repairs.

## Stage 2: Formatter Narrowing

**Goal**: Make `rewards_engine.py` the only production file that translates model level-up fields into UI payloads.

**Work**:
- `format_model_level_up_signal()` accepts canonical names first (`previous_turn_exp`, `current_turn_exp`, `xp_to_next_level`)
- Compute `xp_gained` from those totals
- Make `choices` illegal for `level_up=false`
- Remove/gate fallback that builds missing choices from class data when `level_up_signal` present

**Acceptance**: Unit tests prove canonical fields work without legacy aliases; alias tests labeled for deletion.

## Stage 3: Transport Parity

**Goal**: Streaming and non-streaming both converge on the same formatter with same fail-closed behavior.

**Work**:
- Confirm `llm_parser.py` streaming calls `canonicalize_rewards()` exactly once
- Confirm non-streaming `world_logic.process_action_unified` uses the same helper
- Move transport-specific reward formatting into `rewards_engine.py` or delete if duplicate

**Acceptance**: Grep gate proves only canonical formatter path formats `level_up_signal`; both transports persist same `structured_response.rewards_box` and `structured_response.planning_block` shape.

## Stage 4: Delete Legacy Backend Inference

**Goal**: Remove old Python-owned level-up decision path after evidence shows model contract works.

**Deletion candidates**:
- `resolve_level_up_signal()` new-path usage
- `project_level_up_ui()` polling/recovery usage
- Any backend code comparing old/current XP to decide level-up after `level_up_signal` exists
- Any code synthesizing ASI/class choices from level data to repair missing model choices on new path

**Acceptance**: Real model evidence passes for XP-only and level-up; UI evidence shows rewards-only and level-up states; legacy deletion PR removes code, not alternate inference.

## Stage 5: Enforcement

**Goal**: Stop future drift.

**Work**:
- Add grep gates for old prompt algorithms and duplicate inference call sites
- Add architecture test that fails when new file interprets `level_up_signal` outside `rewards_engine.py`
- Require PR descriptions to state whether production level-up behavior changed

## Relationship to Design Invariants

The 10 design invariants in [[ZFC Level-Up Architecture]] — particularly **Model decides; backend formats**, **One formatter path**, and **Fail-closed for malformed true signals** — are enforced incrementally across Stages 1–5 rather than all at once.

Stage 0 is preparation (removing ambiguity). Stages 1–4 are enforcement. Stage 5 is prevention.

## See Also
- [[ZFC Level-Up Architecture]] — architecture this plan implements
- [[LevelUpArchitecture]] — pre-ZFC architecture this replaces
- [[RewardsEngine]] — the single file that owns formatting across all stages
