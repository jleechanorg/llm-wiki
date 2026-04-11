---
title: "PR #106: fix: correct catch-up narration level gain calculation (WC-dln)"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-106.md
sources: []
last_updated: 2026-03-26
---

## Summary
Catch-up narration displays "gained 0 levels" when companions have actually leveled up during offline time. The root cause is that `resolveCompanionAction` only stored post-action stats (level, xp) but not the pre-action baseline, making it impossible for the catchup endpoints to compute level gains.

## Metadata
- **PR**: #106
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +510/-5 in 3 files
- **Labels**: none

## Connections
