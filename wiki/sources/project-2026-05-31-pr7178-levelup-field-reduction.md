---
title: "PR 7178 level-up lifecycle field reduction"
type: source
tags: [project, memory-file]
date: 2026-05-31
source_file: raw/memory_backfill_2026_06_13/project_2026-05-31_pr7178_levelup_field_reduction.md
---

## Summary

For PR [#7178](https://github.com/jleechanorg/worldarchitect.ai/pull/7178), do not add a replacement object or any new lifecycle/status field for level-up state. Level-up lifecycle should be derived from existing fields: , , or and/or Legacy , , , and booleans may be compatibility reads while old campaigns exist, but they should not remain primary lifecycle authority. : reward atomicity is a same-award-turn invariant.

## Key Claims

- `player_character_data.level`
- `rewards_pending.target_level`, `rewards_pending.new_level`, or
- `custom_campaign_state.level_up_stage` and/or
- `rev-ufb13`: reward atomicity is a same-award-turn invariant. The XP-award turn that creates the
- `rev-0f388`: modal atomicity requires non-finish modal state purity and exactly-once finish
- Design doc:
- Nextsteps:
- Evidence basis:

## Key Quotes

_(No blockquotes in source)_

## Connections

- [[LevelUp]]
- [[level-up]]
- [[rewards_box]]
