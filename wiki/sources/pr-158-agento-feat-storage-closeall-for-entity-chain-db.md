---
title: "PR #158: [agento] feat(storage): closeAll() for entity chain DB cleanup (worldai_claw-b9d)"
type: source
tags: []
date: 2026-03-31
source_file: raw/prs-worldai_claw/pr-158.md
sources: []
last_updated: 2026-03-31
---

## Summary
- Add `closeAll()` function that closes all tracked SQLite database connections and clears the entity chain cache. Call during application shutdown.
- Track database instances in a parallel `dbByCacheKey` map so `closeAll()` can clean them up.
- Fix LRU eviction path to also remove entries from `dbByCacheKey` when evicting.

## Metadata
- **PR**: #158
- **Merged**: 2026-03-31
- **Author**: jleechan2015
- **Stats**: +46/-2 in 2 files
- **Labels**: none

## Connections
