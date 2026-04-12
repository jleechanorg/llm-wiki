---
title: "PR #6150: prompts: make currency setting-aware (not always gold)"
type: source
tags: []
date: 2026-04-09
source_file: raw/prs-worldarchitect-ai/pr-6150.md
sources: []
last_updated: 2026-04-09
---

## Summary
Updates prompt documentation to prevent hardcoded "gold" wording in reward/loot examples. The `rewards_box.gold` canonical numeric field is preserved, but narrative-facing labels now require setting-appropriate currency names (crowns, credits, scrip, etc.). Six core prompt files were updated across rewards, game state, planning, living world, and mechanics systems.

## Key Claims
- 6 prompt files updated: rewards_system_instruction, game_state_instruction, planning_protocol, living_world_instruction, mechanics_system_instruction, mechanics_system_instruction_code_execution
- `rewards_box.gold` remains canonical numeric currency storage
- Prompt contract metadata (`prompt_tool_contracts.json`) versions/sha256 updated
- Regression tests added to prevent gold-only wording regression

## Key Quotes
> "Prompt guidance currently defaults many reward and loot examples to gold wording, which pushes responses toward a single fantasy-currency style even when campaign tone/setting suggests different currency names."

## Metadata
- **PR**: #6150
- **Merged**: 2026-04-09
- **Author**: jleechan2015
- **Stats**: +222/-63 in 10 files
- **Labels**: none

## Connections
- [[rewards_box]] — `gold` field preserved as canonical numeric storage
- [[Campaign Settings]] — currency naming now setting-aware
