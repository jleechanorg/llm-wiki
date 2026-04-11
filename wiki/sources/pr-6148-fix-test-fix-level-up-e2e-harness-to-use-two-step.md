---
title: "PR #6148: fix(test): fix level-up E2E harness to use two-step routing verification"
type: source
tags: []
date: 2026-04-09
source_file: raw/prs-worldarchitect-ai/pr-6148.md
sources: []
last_updated: 2026-04-09
---

## Summary
The `LevelUpAgent` routing was being hijacked by the `CharacterCreationAgent` because `world_logic.py` was unconditionally setting the `level_up_pending` flag even when a character creation session was in progress. This led to a "modal deadlock" where the user was presented with level-up choices that would fail to process because the active agent was still in character creation mode.

## Metadata
- **PR**: #6148
- **Merged**: 2026-04-09
- **Author**: jleechan2015
- **Stats**: +731/-152 in 9 files
- **Labels**: none

## Connections
