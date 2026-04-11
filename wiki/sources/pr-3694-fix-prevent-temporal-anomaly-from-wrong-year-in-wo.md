---
title: "PR #3694: fix: prevent temporal anomaly from wrong year in world_time"
type: source
tags: []
date: 2026-01-17
source_file: raw/prs-worldarchitect-ai/pr-3694.md
sources: []
last_updated: 2026-01-17
---

## Summary
- Fixed prompt instruction that caused LLM to use real-world year (2026) instead of in-game year (1492 DR)
- Added explicit cross-reference between `session_header` Timestamp and `world_data.world_time`

## Metadata
- **PR**: #3694
- **Merged**: 2026-01-17
- **Author**: jleechan2015
- **Stats**: +409/-45 in 7 files
- **Labels**: none

## Connections
