---
title: "PR #6070: fix: align level-up narrative injection with canonical level-up signal"
type: source
tags: []
date: 2026-04-01
source_file: raw/prs-worldarchitect-ai/pr-6070.md
sources: []
last_updated: 2026-04-01
---

## Summary
- **Root cause**: `_inject_levelup_narrative_if_needed` gated only on raw `rewards_pending.level_up_available`, while `_inject_levelup_choices_if_needed` uses `_resolve_level_up_signal` (including stale guards: explicit `level_up_in_progress=False`, `level_up_pending=False`). That split produced **LEVEL UP narrative / indicator messaging without `level_up_now` / `continue_adventuring` in the planning block** when stale modal flags suppressed the canonical signal but leftover `rewards_pending` re

## Metadata
- **PR**: #6070
- **Merged**: 2026-04-01
- **Author**: jleechan2015
- **Stats**: +41/-3 in 2 files
- **Labels**: none

## Connections
