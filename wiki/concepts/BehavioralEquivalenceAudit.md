---
title: "Behavioral Equivalence Audit"
type: concept
tags: [worldarchitect.ai, level-up, rewards-engine, design-doc, behavioral-audit]
date: 2026-04-15
---

## Definition

A **behavioral equivalence audit** verifies whether two functions with the same signature produce identical outputs for identical inputs. Unlike structural grep checks (which verify imports and call sites), behavioral audits test actual runtime outputs against real game state.

## Why It Matters

Design docs often claim "function X in module A maps to function Y in module B." These claims may be **structurally true but behaviorally false** — same signature, different logic, different outputs.

**Example from PR #6276 v4 design:**
- Design doc claim: `_should_emit_level_up_rewards_box` (world_logic) ↔ `should_show_rewards_box` (rewards_engine) — equivalent
- Behavioral truth: **NOT equivalent** — world_logic version cross-checks `game_state` flags, rewards_engine version only checks `rewards_box` content
- Same input game state → different output decisions

## The Three Non-Equivalent Pairs (rev-v4ci05 Audit)

| world_logic Function | rewards_engine Function | Why Not Equivalent |
|---------------------|----------------------|-------------------|
| `_should_emit_level_up_rewards_box` | `should_show_rewards_box` | world_logic: needs `game_state` cross-check; rewards_engine: checks `rewards_box` only |
| `_enforce_rewards_box_planning_atomicity` | `_enforce_atomicity` | world_logic: injection + scrubbing logic; rewards_engine: null-check only |
| `_project_level_up_ui_from_game_state` | `project_level_up_ui` | Return type mismatch: world_logic returns `{rewards_box, level_up_active}`; rewards_engine returns `(rewards_box, planning_block)` tuple |

## Two Philosophies

The non-equivalence stems from two fundamentally different design philosophies:

1. **XP-threshold/causal** (rewards_engine): Compute from XP values — if `current_xp >= xp_needed_for_level(target)`, trigger level-up
2. **Flag-driven/stateful** (world_logic): Check persisted flags — if `level_up_pending=true`, emit rewards_box regardless of XP math

Both are **correct** within their own context, but they produce different outputs when the flag and XP state disagree.

## Connection to Design Doc Drift

Behavioral equivalence audits prevent **design doc drift** — the pattern where PRs merge with structural gates passing but behavioral goals unmet.

**When to audit:**
- When a design doc claims "X maps to Y" between two modules
- Before redirecting call sites from old to new implementation
- After any refactor that claims "drop-in replacement"

**How to audit:**
1. Enumerate all function pairs claimed equivalent in design doc
2. For each pair, collect 5+ real game state snapshots (pre-level-up, post-level-up, stuck-path, etc.)
3. Run both functions on identical inputs
4. Compare outputs — structurally and semantically
5. Document which pairs are truly equivalent vs. divergent

## Connections
- [[LevelUpV4Architecture]] — where the equivalence claims were made
- [[rewardsEngine]] — the new module
- [[worldLogic]] — the legacy module
- [[DesignDocDrift]] — the failure pattern this audit addresses
