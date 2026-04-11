---
title: "PR #5105: Prompt contract: require world_events on living-world turns"
type: source
tags: []
date: 2026-02-09
source_file: raw/prs-worldarchitect-ai/pr-5105.md
sources: []
last_updated: 2026-02-09
---

## Summary
- make `state_updates.world_events` explicitly REQUIRED in living-world prompt instructions (LLM contract only)
- reinforce this requirement in the runtime living-world prompt header
- resolve prompt contradictions that could cause confusion:
  - align cadence language to **every 3 turns OR every 24 game hours**
  - clarify `state_updates` emission guidance so minigame-specific delta guidance does not conflict with global `state_updates` presence requirement
  - clarify living-world payload shou

## Metadata
- **PR**: #5105
- **Merged**: 2026-02-09
- **Author**: jleechan2015
- **Stats**: +91/-33 in 8 files
- **Labels**: none

## Connections
