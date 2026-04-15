---
title: "Rewards Engine Refactor"
type: concept
tags: [rewards-engine, level-up, refactor, v4, single-responsibility]
sources: ["pr6276_design_doc_v4_summary"]
last_updated: 2026-04-15
---

## Definition
Rewards Engine Refactor (v4) consolidates all rewards and progression decisions into `rewards_engine.py`, making it the single source of truth for level-up detection, XP math, rewards box normalization, and planning atomicity enforcement.

## Public API (rewards_engine.py)
After PR #6276, `rewards_engine.py` exposes:
- `is_level_up_active()` — check if level-up is active
- `resolve_level_up_signal()` — detect level-up signal from game state
- `ensure_rewards_box()` — build canonical rewards_box
- `ensure_planning_block()` — ensure planning block present
- `normalize_rewards_box()` — canonicalize for UI/persistence
- `should_show_rewards_box()` — determine if rewards should display
- `canonicalize_rewards()` — **single call site** in llm_parser.py
- `project_level_up_ui()` — polling path entry point
- `_canonicalize_core()` — shared computation (internal)
- `_enforce_atomicity()` — atomic pair enforcement
- `_is_state_flag_true()` — canonical definition
- `_is_state_flag_false()` — canonical definition

## Problem Solved
Before v4:
- `_is_state_flag_true` existed in 3 files (rewards_engine.py, world_logic.py, game_state.py)
- `canonicalize_rewards` called TWICE in non-streaming path (Firestore + response)
- `world_logic.py` had 25+ rewards-related functions
- No clear single call site for rewards decisions

## Key Files
| File | Lines | Role |
|------|-------|------|
| `rewards_engine.py` | 491 | Single rewards/progression decisions source |
| `llm_parser.py` | 1060 | Single orchestration root, calls rewards_engine once |
| `world_logic.py` | 8729→1500 | Thin modal wrapper (in progress) |
| `game_state.py` | 4387 | XP math + Firestore I/O |
