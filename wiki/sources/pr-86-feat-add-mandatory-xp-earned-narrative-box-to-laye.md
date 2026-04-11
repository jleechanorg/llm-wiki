---
title: "PR #86: feat: add MANDATORY XP EARNED narrative box to Layer 6 (level_up)"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-86.md
sources: []
last_updated: 2026-03-26
---

## Summary
- Add MANDATORY XP EARNED narrative box mandate to CHARACTER STATE & LEVEL-UP MANDATE (Layer 6) in system instruction
- When XP threshold is crossed, LLM must display dedicated box in scene_text with: total XP gained, current XP, and progress toward next level
- Values in the box must match state_delta XP updates for that same turn
- TDD: 5 new tests covering all Layer 6 requirements

## Metadata
- **PR**: #86
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +57/-1 in 2 files
- **Labels**: none

## Connections
