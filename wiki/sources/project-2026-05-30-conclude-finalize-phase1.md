---
title: "Project 2026-05-30 Conclude Finalize Phase1"
type: source
tags: [project, worldarchitect-ai, memory-file]
date: 2026-05-30
source_file: raw/memory_backfill_2026_06_13/project_2026-05-30_conclude_finalize_phase1.md
---

## Summary

Branch (worktree ). Implements the unified conclude/finalize prompt so the MODEL owns the canonical level commit + derived-stat cascade. Path B, replaces PR #7175 — do NOT merge until real-LLM green + human .

## Key Claims

- `mvp_site/constants.py`: SRD tables PROFICIENCY_BONUS_BY_LEVEL (1-20), HIT_DIE_BY_CLASS, SPELL_SLOTS_BY_LEVEL, FULL_CASTER_CLASSES (ZFC-exempt).
- `mvp_site/derived_stats.py`: pure `recompute_derived_stats(level,class,scores)` (arity 3) + `reconcile(snapshot)` (arity 1, sorted list[str], checks only present fields, never mutates).
- `mvp_site/schemas/conclude_snapshot.py`: ConcludeSnapshot (level 1-20, rejects >20, coerces stringy ints — level coercion is plain int() NOT DefensiveNumericConverter, which clamps 0→1 and would defeat ge=1).
- `mvp_site/prompts/_conclude_core.md` (4 clauses, reconcile adapted/scoped from god_mode_instruction.md:185-223) + thin headers level_up_conclude_instruction.md / character_creation_conclude_instruction.md; wired via PROMPT_TYPE_* + *_PATH in constants + agent_prompts.PATH_MAP.
- `agents.py`: `select_conclude_phase()` helper + `_detect_conclude_signal()` (finish-choice id OR FastEmbed exit-intent). LevelUpAgent/CharacterCreationAgent gained a `phase` attr + conclude `prompt_order()` (swap in-progress prompt → *_conclude header + append _conclude_core; level-up conclude OMITS in-progress modal override + FINAL CONTRACT). NEW early branch in `get_agent_for_input` (before modal locks + CC completion override) forces domain agent in conclude phase on finish signal, metadata["phase"]="conclude". agents.py must NOT import world_logic (world_logic imports agents) — used a local CHOICE/JSON extractor.
- `backend_adjustment_specs.py`: warn-only AdjustmentSpec `conclude.reconcile_derived_stats` (CORRECTION, must go in ACTIVE_PR_6958 tuple lines 29-1023, NOT the location tuple at 1053). `conclude_invariant.py` emitter LOGS `conclude_derived_stats_mismatch` on mismatch + returns state unmutated (NOOP); wired in `world_logic.validate_game_state_updates` scoped to MODE_LEVEL_UP/MODE_CHARACTER_CREATION.

## Key Quotes

_(No blockquotes in source)_

## Connections

- [[rebase]]
- [[LevelUp]]
- [[level-up]]
