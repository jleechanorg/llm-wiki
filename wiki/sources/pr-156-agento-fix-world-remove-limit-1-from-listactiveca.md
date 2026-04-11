---
title: "PR #156: [agento] fix(world): remove LIMIT 1 from listActiveCampaigns to return all active campaigns"
type: source
tags: []
date: 2026-03-30
source_file: raw/prs-worldai_claw/pr-156.md
sources: []
last_updated: 2026-03-30
---

## Summary
listActiveCampaigns() in packages/backend/src/world/sqlite_world_store.ts was changed in PR #63 to return at most one campaign (the most recently updated within 2 hours). All other active campaigns were silently excluded from the scheduler loop and would never tick.

## Metadata
- **PR**: #156
- **Merged**: 2026-03-30
- **Author**: jleechan2015
- **Stats**: +130/-18 in 5 files
- **Labels**: none

## Connections
