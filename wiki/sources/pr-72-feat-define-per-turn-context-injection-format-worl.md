---
title: "PR #72: feat: define per-turn context injection format (worldai_claw-n3o)"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-72.md
sources: []
last_updated: 2026-03-26
---

## Summary
The original `game_state_instruction.md` is 36,443 tokens — far too large for the system prompt. Per the design (`roadmap/worldai_claw_mvp.md`, "Exact 50k Context Business Logic"), game state must be injected into the 40k non-system context budget alongside existing memory blocks.

This PR defines the per-turn context injection format: how the `ContextBuilder` assembles the per-turn context payload.

## Metadata
- **PR**: #72
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +594/-37 in 6 files
- **Labels**: none

## Connections
