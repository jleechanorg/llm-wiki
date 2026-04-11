---
title: "PR #4547: fix(frontend): display dice roll label when purpose field is missing"
type: source
tags: []
date: 2026-02-02
source_file: raw/prs-worldarchitect-ai/pr-4547.md
sources: []
last_updated: 2026-02-02
---

## Summary
- Backend now normalizes `label` → `purpose` in action_resolution rolls for frontend compatibility

**Key themes:**
- Single source of truth (backend handles field mapping, not frontend)
- Cleaner architecture (frontend stays simple, backend normalizes data)

## Metadata
- **PR**: #4547
- **Merged**: 2026-02-02
- **Author**: jleechan2015
- **Stats**: +61/-1 in 2 files
- **Labels**: none

## Connections
