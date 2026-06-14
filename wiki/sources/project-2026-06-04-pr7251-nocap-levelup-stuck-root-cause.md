---
title: "Stuck LevelUpAgent — No-Cap Prompt Fix (PR #7251) GREEN Validated"
type: source
tags: ["levelup", "pr-7251", "worldarchitect-ai", "no-cap", "gemini-block"]
date: 2026-06-04
source_file: project_2026-06-04_pr7251_nocap_levelup_stuck_root_cause.md
---

## Summary
Dev campaign `mXhtOccHYGHgV2Tdf0lc` stuck at L20 with 6.4M XP. Real cause = PROHIBITED_CONTENT block (NOT level-20 cap, NOT thinking-exhaustion). Prompt-only no-cap fix GREEN-validated on benign copy; does NOT fix the real blocked campaign.

## Key Claims
- Stuck at level 20, experience.current=6,432,000 (XP implies level 141 via unbounded level_from_xp)
- Root cause: promptFeedback.blockReason: PROHIBITED_CONTENT (lives in recent story entries seq ~1111–1123)
- safetySettings: BLOCK_NONE cannot disable PROHIBITED_CONTENT (non-configurable category)
- Fix = prompt-only, mvp_site/prompts/level_up_instruction.md (+60/-9): 'Availability Recognition — No Level Cap' section
- GREEN validated: 2/2 pass, classification FULL_CATCHUP(141), rewards_box = {current_level:20, new_level:141, resolved_target_level:141, level_up_available:true, source:model}

## Key Quotes
> No backend logic → no ZFC violation; mirrors already-unbounded `game_state.level_from_xp`

## Connections
- [[LevelUpStuck]] — concept
- [[PR7251]] — fix PR
- [[GeminiContentBlock]] — root cause class
