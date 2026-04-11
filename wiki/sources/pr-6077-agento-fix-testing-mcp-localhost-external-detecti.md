---
title: "PR #6077: [agento] fix(testing_mcp): localhost external detection + level-up atomicity test"
type: source
tags: []
date: 2026-04-02
source_file: raw/prs-worldarchitect-ai/pr-6077.md
sources: []
last_updated: 2026-04-02
---

## Summary
- `_build_test_identity_headers`: use same localhost detection as `start_server()` so `http://127.0.0.1:`/`http://localhost:` not classified as external
- `test_level_up_rewards_planning_atomicity`: proves level-up badge and planning_block are atomic; accepts dict|string|None; uses getattr guard; proves inject path fired

## Metadata
- **PR**: #6077
- **Merged**: 2026-04-02
- **Author**: jleechan2015
- **Stats**: +375/-9 in 3 files
- **Labels**: none

## Connections
