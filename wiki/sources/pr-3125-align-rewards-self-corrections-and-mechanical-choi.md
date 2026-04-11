---
title: "PR #3125: Align rewards self-corrections and mechanical choice tests"
type: source
tags: [codex]
date: 2026-01-06
source_file: raw/prs-worldarchitect-ai/pr-3125.md
sources: []
last_updated: 2026-01-06
---

## Summary
- Persist `pending_system_corrections` in the initial game_state save (all modes) and clear stale corrections; avoid redundant Firestore write.
- Validate `LLMRequest.system_corrections` list type + item strings to ensure clean prompt injection.
- Tighten rewards tests: require REWARDS corrections, verify `RewardsAgent.matches_game_state()` is false once `rewards_processed=True`, and allow `continue_adventure` as the safe mechanical choice.
- Note: rewards handling uses detection + LLM self-corr

## Metadata
- **PR**: #3125
- **Merged**: 2026-01-06
- **Author**: jleechan2015
- **Stats**: +274/-107 in 12 files
- **Labels**: codex

## Connections
