---
title: "God Mode Planning Blocks Tests"
type: source
tags: [python, testing, god-mode, planning-block, choices]
source_file: "raw/test_god_mode_planning_blocks.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite validating that God mode responses include planning blocks when offering choices to users. Tests verify the god: prefix requirement for choice IDs and mandatory return_story option.

## Key Claims
- **Planning block support**: God mode responses can include planning_block with thinking, context, and choices fields
- **Choice ID prefix**: All God mode choices must use "god:" prefix in their id field
- **Mandatory return_story**: Every God mode planning block must include god:return_story choice
- **Mode switching**: god:return_story should explicitly set switch_to_story_mode to true

## Key Quotes
> "As the omniscient game master, I present several plot directions for your campaign." — God mode response header

> "Must include 'god:return_story' as default choice" — Test assertion

## Connections
- [[God Mode Narrative Validation Placeholder Tests]] — Related God mode validation tests
- [[God Mode Placeholder Bug End-to-End Test]] — Related God mode bug reproduction
- [[GOD MODE End-to-End Integration Tests]] — Full stack God mode testing

## Contradictions
- None identified
