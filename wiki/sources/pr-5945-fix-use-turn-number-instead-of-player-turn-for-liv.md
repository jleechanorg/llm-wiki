---
title: "PR #5945: fix: use turn_number instead of player_turn for living world triggers"
type: source
tags: []
date: 2026-03-12
source_file: raw/prs-worldarchitect-ai/pr-5945.md
sources: []
last_updated: 2026-03-12
---

## Summary
- Fix living world events never triggering because trigger logic used `player_turn` which was always 0
- Now uses `turn_number` which is properly incremented

## Metadata
- **PR**: #5945
- **Merged**: 2026-03-12
- **Author**: jleechan2015
- **Stats**: +684/-2 in 4 files
- **Labels**: none

## Connections
