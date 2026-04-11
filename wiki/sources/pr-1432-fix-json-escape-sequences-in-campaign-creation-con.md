---
title: "PR #1432: Fix JSON escape sequences in campaign creation - Convert instead of clean"
type: source
tags: [bug, enhancement, backend]
date: 2025-08-24
source_file: raw/prs-worldarchitect-ai/pr-1432.md
sources: []
last_updated: 2025-08-24
---

## Summary
Fixes JSON escape sequences appearing in campaign descriptions by implementing proper conversion during campaign creation rather than cleaning during retrieval.

**Problem**: Dragon Knight campaign descriptions showed `\\n\\n` instead of proper paragraph breaks
**Solution**: Convert JSON escape sequences (`\\n`, `\\t`, `\\"`, etc.) during campaign prompt building

## Metadata
- **PR**: #1432
- **Merged**: 2025-08-24
- **Author**: jleechan2015
- **Stats**: +536/-55 in 5 files
- **Labels**: bug, enhancement, backend

## Connections
