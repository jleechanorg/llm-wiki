---
title: "PR #6273 — Rewards Engine v4 Single-Responsibility Pipeline"
type: source
tags: [level-up, rewards-engine, architecture, refactor]
date: 2026-04-14
source_file: wiki/sources/pr6273_rewards_engine_v4_single_responsibility.md
---

## Summary
Centralizes level-up rewards/progression logic into new `rewards_engine.py` with dual entry points (`canonicalize_rewards` for LLM/streaming path, `project_level_up_ui` for polling path). Renames `streaming_orchestrator.py` → `llm_parser.py` to reflect its dual streaming/non-streaming role. 24 tests pass. Layer 3 CLEAN (world_logic strip) deferred to follow-up PR.

## Key Claims
- Single-responsibility rewards engine replaces scattered inline logic across world_logic.py
- Dual entry points: canonicalize_rewards (streaming/LLM) + project_level_up_ui (polling)
- Ownership: `_is_state_flag_true`/`_is_state_flag_false` consolidated to one canonical copy in rewards_engine.py
- D&D ASI fixes: multiclass ASI now checks total character level, correct 5e rule
- Supersedes PRs #6262, #6263, #6264, #6268 (all closed)

## Key Quotes
> "Canonicalizes level-up rewards/progression logic into new `mvp_site/rewards_engine.py`, providing `canonicalize_rewards()` (LLM/streaming) and `project_level_up_ui()` (polling) with a strict atomic `(rewards_box, planning_block)` invariant" — PR description

## Technical Details
- **New file**: `rewards_engine.py` — 437 lines, 16 contract tests
- **Rename**: `streaming_orchestrator.py` → `llm_parser.py`
- **Wiring**: `llm_parser.py` calls `rewards_engine.canonicalize_rewards()` as single canonicalization call site
- **Test results**: 24 passed, 1 skipped, 1 pre-existing failure
- **Layer status**: RED (contract tests) GREEN | GREEN (rewards_engine) GREEN | WIRE (llm_parser wiring) GREEN | CLEAN (strip world_logic) SKIPPED

## Connections
- [[Level-Up Engine]] — v4 design supersedes v3
- [[rewards_box Normalization]] — atomic (rewards_box, planning_block) invariant
- Supersedes: PR #6262, #6263, #6264, #6268
- Followed by: PR #6276 (Layer 3 CLEAN incomplete — world_logic.py not yet stripped)
