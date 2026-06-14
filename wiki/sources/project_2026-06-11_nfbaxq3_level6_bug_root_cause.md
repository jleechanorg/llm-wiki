---
title: "NFBaxQ3mIUe17UlAAGlE Level 6 Bug — Root Cause (LLM prompt defect, not backend override)"
type: source
tags: [project, level-up, llm-prompt, zfc, root-cause, worldarchitect, nfbaxq3]
date: 2026-06-11
source_file: raw/project_2026-06-11_nfbaxq3_level6_bug_root_cause.md
---

## Summary
The NFBaxQ3mIUe17UlAAGlE "level 5 instead of 6" bug is an LLM prompt/schema defect, NOT a backend override. The LLM consistently emits `rewards_box.new_level=6`, `level_up_signal.target_level=6`, L6 features, and L6 HP — but leaves `state_updates.player_character_data.level=5` in the same `state_updates` block. Cloud Logging surfaces this as `SESSION_HEADER_LEVEL_MISMATCH: LLM-emitted session header displays level 6, but persisted level is 5`. Per ZFC, the fix belongs in the LLM prompt and model-side schema rejection, NOT in a backend clamp. PR #7434 does NOT fix this — it has zero `level = 6` writes in production code and addresses a different bug class entirely.

## Key Claims
- The user's "god mode override" hypothesis was REFUTED — the flow was a normal CHARACTER-mode level-up, not a god-mode turn
- Root cause: LLM fails to write `player_character_data.level` in the same `state_updates` block where it writes L6 features and HP
- PR #7434 (`fix/level-up-daily-cron-combined`) is a 3-PR stack (PR-A god-mode rewards_box persistence, PR-B modal turn revert, PR-C codex quota skip); it does NOT touch `level` writes
- Per ZFC, adding a server-side "if rewards_box.new_level > current_level, override player_character_data.level" is forbidden without explicit human approval
- Suggested fix (out of scope for PR #7434): update the level-up agent's system prompt to require `state_updates.player_character_data.level` whenever `rewards_box.new_level` or `level_up_signal.target_level` is written
- Convert `SESSION_HEADER_LEVEL_MISMATCH` from a silent warning into a "rejection-and-retry" signal back to the model

## Key Quotes
> "**LLM prompt/schema defect, not backend override.** The LLM consistently emits: `rewards_box.new_level: 6` (correct) ... `state_updates.player_character_data.features.append: [L6 features]` (correct) ... `state_updates.player_character_data.health: {hp: 56, hp_max: 56}` (L6 HP, correct) ... **`state_updates.player_character_data.level: 5`** ❌ (left at pre-L5 value)"

> "Cloud Logging surfaces this as `SESSION_HEADER_LEVEL_MISMATCH: LLM-emitted session header displays level 6, but persisted level is 5`."

> "PR #7434 (`fix/level-up-daily-cron-combined`) is a 3-PR stack ... The diff has **zero** literal `level = 6` / `"level": 6` / `override_level` writes in production code."

## Connections
- [[stale-level-up-complete-cleared-2to3]] — sibling 2→3 fix landed earlier same session
- [[ZeroFrameworkCognition]] — principle that backend clamp is forbidden; fix belongs in prompt
- [[LevelUpAgentPrompt]] — the prompt that needs to be updated
- [[SESSION_HEADER_LEVEL_MISMATCH]] — the warning that should become a rejection signal
- [[PR_7434]] — the PR that does NOT fix this bug
- [[PR_7516]] — related PR for unrelated bug class
- [[NFBaxQ3mIUe17UlAAGlE]] — the campaign where the bug was reproduced
- [[AstarionMulticlass]] — Astarion Lvl 5 Gloomstalker/Assassin/Whispers multiclass
- [[RootCauseFirstEngineering]] — principle that LLM prompt should be fixed first
- [[rev-d6qgj]] — bead for the related feedback
