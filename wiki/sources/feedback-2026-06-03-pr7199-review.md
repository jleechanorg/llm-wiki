---
title: "PR #7199 Review — 2026-06-03"
type: source
tags: [feedback, project, worldarchitect-ai, memory-file]
date: 2026-06-03
source_file: raw/memory_backfill_2026_06_13/feedback_2026-06-03_pr7199_review.md
---

## Summary

PR: [https://github.com/jleechanorg/worldarchitect.ai/pull/7199](https://github.com/jleechanorg/worldarchitect.ai/pull/7199) Title: "[antig] Modal conclude policy extraction + classifier exit coverage (creation + level-up)" Head: (MERGEABLE, no formal reviewDecision) The PR's stated goal is "centralize modal conclude/exit policy into shared module" — but the world_logic modal-lock path uses (visible-text-aware) while the agent-routing path uses (NOT visible-text-aware). The "V3 ZFC fix" claimed in the PR body did NOT actually land in , so the same visible-button click that exits the modal at world_logic will NOT route to the CONCLUDE phase in . This is the ("Conclude routing ignores visible finish", agents.py:3336).

## Key Claims

- "Empty structured planning_block shadowing" (line 2224) — `_extract_recent_planning_blocks` now returns `None` for empty `structured_fields.planning_block`, shadowing the legacy field.
- "Partial pending health breaks max HP" (line 2439) — `_apply_level_up_pending_selections_to_player_data` can persist `hp_current > hp_max` when only one of `hp_current`/`hp_max` is in pending selections.
- "Finish reads cleared pending selections" — hydration reads from `_merged_custom_campaign_state` instead of `custom_state` (current_game_state_dict), missing same-turn LLM clear.
- "Explicit pending HP values silently overwritten by hp_gain" (line 2392) — explicit `hp_current`/`hp_max` in pending selections is overridden by `hp_gain` math.
- "Visible CC finish skips conclude" (agents.py:3339) — `CharacterCreationAgent.matches_input` correctly routes visible-text to conclude, but the world_logic modal-lock path does not.
- "Visible level-up finish drifts agents" (modal_conclude_policy.py:129) — visible-text-aware path used in world_logic, but agent routing does not.
- "Level-up finish during creation only" (world_logic.py:2727) — when only CC is active, `CHOICE:finish_level_up_return_to_game` is still treated as level-up finish.
- "Honor visible finish labels before falling back to the classifier" (modal_conclude_policy.py:176) — same as Cursor HIGH finding.

## Key Quotes

_(No blockquotes in source)_

## Connections

- [[Skeptic Gate]]
- [[beads]]
- [[level-up]]
- [[7-green]]
- [[CodeRabbit]]
