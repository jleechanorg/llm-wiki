---
title: "PR #4947: fix(automation): rolling 24h window + per-commit retry limit + push refspec"
type: source
tags: []
date: 2026-02-08
source_file: raw/prs-worldarchitect-ai/pr-4947.md
sources: []
last_updated: 2026-02-08
---

## Summary
Three bug fixes discovered from PR #4572 receiving 23 fixpr comments (limit: 10):

1. **Rolling 24h window** - Fix never merged from PR #4820 (only version bump got merged)
2. **Per-commit retry limit** - Prevent wasting 12 runs on same unfixable commit
3. **Push refspec instructions** - Agents told to use bare git push on fixpr branches with no tracking

**Key themes:**
- Safety limit enforcement
- Agent push reliability
- Preventing wasted automation runs

## Metadata
- **PR**: #4947
- **Merged**: 2026-02-08
- **Author**: jleechan2015
- **Stats**: +380/-38 in 4 files
- **Labels**: none

## Connections
