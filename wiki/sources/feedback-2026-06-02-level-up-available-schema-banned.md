---
title: "Rule"
type: source
tags: [feedback, project, worldarchitect-ai, memory-file]
date: 2026-06-02
source_file: raw/memory_backfill_2026_06_13/feedback_2026-06-02_level_up_available_schema_banned.md
---

## Summary

is a backend-derived field — set by / . Adding it to the schema makes the LLM echo it back, and the backend then trusts the echo. This is a circular dependency: backend sets a field → LLM includes it in output → backend reads it as a "model-owned" signal → the field means nothing.

## Key Claims

- If the game_state field is set by the backend (e.g. `ensure_rewards_box`), do NOT propagate it through the schema
- Replace with `target_level > current_level` using `rewards_box.new_level` / `rewards_box.resolved_target_level` vs `player_character_data.level`
- PR: https://github.com/jleechanorg/worldarchitect.ai/pull/7221
- Commit removing it again: `20372341397403affbd4346014563d345c86ca53`
- Original removal commit: `cf0f21da43` (2026-05-04)
- Bead: rev-1pmyg (closed)
- Related: [[zfc-leveling-roadmap]], [[level-up-signal-contract]]

## Key Quotes

_(No blockquotes in source)_

## Connections

- [[level-up]]
- [[rewards_box]]
