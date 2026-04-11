---
title: "PR #119: chore: reconcile Firestore indexes with deployed state"
type: source
tags: []
date: 2025-11-23
source_file: raw/prs-/pr-119.md
sources: []
last_updated: 2025-11-23
---

## Summary
- Synced firestore.indexes.json with what is actually deployed in production
- Added userId + createdAt DESC index (was deployed but missing from JSON)
- Removed unused userId + archived index (covered by 3-field archived index)

## Metadata
- **PR**: #119
- **Merged**: 2025-11-23
- **Author**: jleechan2015
- **Stats**: +7/-7 in 1 files
- **Labels**: none

## Connections
