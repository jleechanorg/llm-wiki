---
title: "PR #90: feat(system): add STRICT XP & state change consistency rule"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-90.md
sources: []
last_updated: 2026-03-26
---

## Summary
The LLM system instruction lacked an explicit, dedicated consistency rule for XP and permanent state changes. While the CAMPAIGN PROGRESSION, LIVING WORLD, AND REWARDS COHERENCE section covered the high-level requirement (XP in scene_text must match state_delta), a standalone "STRICT" enforcement clause was missing — making it easy for the LLM to accidentally narrate rewards without corresponding state mutations.

## Metadata
- **PR**: #90
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +133/-0 in 2 files
- **Labels**: none

## Connections
