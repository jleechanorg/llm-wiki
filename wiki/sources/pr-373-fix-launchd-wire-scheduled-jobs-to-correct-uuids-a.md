---
title: "PR #373: fix(launchd): wire scheduled jobs to correct UUIDs, add missing scripts"
type: source
tags: []
date: 2026-03-24
source_file: raw/prs-worldai_claw/pr-373.md
sources: []
last_updated: 2026-03-24
---

## Summary
6 schedule plists had dead UUIDs silently failing every scheduled run. jobs.json was migrated to new healthcheck jobs but the plists were never updated. Two scripts referenced by newer templates also did not exist.

## Metadata
- **PR**: #373
- **Merged**: 2026-03-24
- **Author**: jleechan2015
- **Stats**: +125/-373 in 14 files
- **Labels**: none

## Connections
