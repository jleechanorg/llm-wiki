---
title: "Behavioral Equivalence Audit"
type: concept
<<<<<<< HEAD
tags: [layer3-clean, world-logic, rewards-engine, refactor, v4]
sources: ["pr6276-layer3-clean-2026-04-15"]
last_updated: 2026-04-15
---

## Definition
A behavioral equivalence audit compares two functions that claim to be equivalent replacements to verify they actually produce identical outputs for identical inputs. Required before redirecting call sites in Layer 3 CLEAN.

## Problem: Design Doc Equivalence Assumption Doesn't Hold

The v4 design doc maps 5 world_logic deprecated functions to rewards_engine equivalents, assuming behavioral equivalence. Audit reveals:

### Case 1: `_should_emit_level_up_rewards_box` vs `should_show_rewards_box`
- **world_logic signature**: `_should_emit_level_up_rewards_box(game_state_dict, rewards_box)`
- **rewards_engine signature**: `should_show_rewards_box(rewards_box)`
- **world_logic behavior**: calls `_resolve_level_up_signal(game_state_dict, rewards_box)` for cross-check against game state
- **rewards_engine behavior**: only checks `rewards_box.get("level_up_available")` and `xp_gained > 0`
- **Gap**: world_logic version has game_state cross-check that rewards_engine version lacks

### Case 2: `_enforce_rewards_box_planning_atomicity` vs `_enforce_atomicity`
- **world_logic signature**: `_enforce_rewards_box_planning_atomicity(rewards_box, planning_block, game_state_dict, allow_injection)`
- **rewards_engine signature**: `_enforce_atomicity(rewards_box, planning_block)`
- **world_logic behavior**: choice injection (calls `_inject_levelup_choices_if_needed`), stale choice scrubbing (removes level_up_now/continue_adventuring when game state doesn't support level-up), suppression logic
- **rewards_engine behavior**: if either rewards_box or planning_block is None, returns (None, None) — simple null-check
- **Gap**: world_logic version is much richer; rewards_engine version is minimal

### Case 3: `_project_level_up_ui_from_game_state` vs `project_level_up_ui`
- **world_logic return**: `rewards_box` (single dict)
- **rewards_engine return**: `(rewards_box, planning_block)` (tuple)
- **Gap**: return type mismatch

## Resolution Options
1. **Align rewards_engine** to match world_logic behavior (extend `_enforce_atomicity` to add injection/scrubbing)
2. **Keep world_logic wrapper** that adds missing behavior before/after calling rewards_engine
3. **Change call sites** to handle the difference (unwrap tuple, add cross-check, etc.)

## Why This Matters
Redirecting without audit = introducing subtle bugs. A function that "looks like" the replacement is not the same as "behaves like" the replacement. The design doc was written at architecture level and didn't capture the behavioral nuances accumulated in world_logic versions.

## Bead
rev-v4ci05: "Layer 3 CLEAN: audit behavioral equivalence before function redirect"
=======
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
>>>>>>> origin/fix/br-4bk-green-gate-design-doc-v2
