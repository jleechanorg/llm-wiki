---
title: "PR #2915: fix(social-hp): Auto-inject Social HP enforcement for god-tier NPCs"
type: source
tags: []
date: 2026-01-09
source_file: raw/prs-worldarchitect-ai/pr-2915.md
sources: []
last_updated: 2026-01-09
---

## Summary
Fixes a bug where God/Primordial tier NPCs (like Empress Sariel, Level 35) were not properly triggering the Social HP skill challenge system, allowing single-roll persuasion bypasses.

**Bug Evidence:**
- **Dragon Knight Evil**: Empress Sariel (Level 35 God-Empress) NEVER had Social HP tracked
- **Dragon Knight Good**: Prefect Gratian (Lord tier) properly got `Social HP: 5/5` tracking

This is backwards - God-tier NPCs should have MORE protection (15+ HP), not less.

## Metadata
- **PR**: #2915
- **Merged**: 2026-01-09
- **Author**: jleechan2015
- **Stats**: +3872/-114 in 36 files
- **Labels**: none

## Connections
