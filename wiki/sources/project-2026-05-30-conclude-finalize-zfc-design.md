---
title: "Project 2026-05-30 Conclude Finalize Zfc Design"
type: source
tags: [project, worldarchitect-ai, memory-file]
date: 2026-05-30
source_file: raw/memory_backfill_2026_06_13/project_2026-05-30_conclude_finalize_zfc_design.md
---

## Summary

Design + plan + Dark Factory run authored 2026-05-30 (branch from HEAD). Replaces PR #7175 (Path B). Do NOT merge until human MERGE APPROVED.

## Key Claims

- `commit_expected_level_from_xp` (`rewards_engine.py:3191`) is ALREADY partially ZFC: step 1 preserves a model-set `player_character_data.level`; only step 2 (rewards_pending fallback) + step 3 (XP-table derivation) + the `level_up_in_progress=True` force-flips (`world_logic.py:2482/2610/2756`) are the override. **Staged deletion:** make the conclude prompt always hit step 1 (proven via real-LLM `/llm-testing`), THEN steps 2-3 + force-flips become dead code and are removed. Not a blind override — a fallback chain.
- Agent routing is legitimate state-based routing (NOT banned ZFC keyword routing): domain agent chosen by `level_up_in_progress`/`character_creation_in_progress`; the conclude SIGNAL (finish-choice id in `_level_up_exit_choices`, or FastEmbed `classify_level_up_exit_intent`/`classify_cc_exit_intent`) selects the PROMPT PHASE within the already-selected agent and forces the correct domain agent on finish. ALL LLM interaction stays through an agent — no agent-less prompt assembly. ("never on which agent / stays ZFC" was a wrong earlier framing.)
- Prompt composition: no `@`-include in `prompts/`; agents compose via `REQUIRED_PROMPT_ORDER` + `agent_prompts.py` PATH_MAP. True reuse = one `_conclude_core.md` referenced by both LevelUpAgent + CharacterCreationAgent conclude-phase orders.
- No derived-stat tables exist yet (`constants.py` has only `XP_TABLE_5E:638`); reducer must be built once and shared. `AdjustmentSpec` is a frozen dataclass (`backend_adjustment_types.py:91`); specs are declared but NOT yet consumed at runtime → the warn-only emitter is net-new. FastEmbed exit classifier already exists (`intent_classifier.py:1267`).

## Key Quotes

_(No blockquotes in source)_

## Connections

- [[LevelUp]]
- [[level-up]]
