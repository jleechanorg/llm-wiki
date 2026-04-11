---
title: "PR #5536: Fix living-world schema drift: include last_living_world_* fields"
type: source
tags: []
date: 2026-02-15
source_file: raw/prs-worldarchitect-ai/pr-5536.md
sources: []
last_updated: 2026-02-15
---

## Summary
This PR fixes living-world schema drift on `origin/main` by adding missing top-level fields to `mvp_site/schemas/game_state.schema.json`:
- `last_living_world_turn`
- `last_living_world_time`

It also adds a regression test in `mvp_site/tests/test_game_state.py` to ensure these schema fields remain present.

## Metadata
- **PR**: #5536
- **Merged**: 2026-02-15
- **Author**: jleechan2015
- **Stats**: +76/-20 in 2 files
- **Labels**: none

## Connections
