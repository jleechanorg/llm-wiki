---
title: "PR #157: [agento] fix(mem0): fix autoRecall userId mismatch (Python snake_case vs Node.js camelCase)"
type: source
tags: []
date: 2026-03-15
source_file: raw/prs-worldai_claw/pr-157.md
sources: []
last_updated: 2026-03-15
---

## Summary
- Node.js `openclaw-mem0` extension filters Qdrant by `userId` (camelCase)
- Python `mem0` library stores with `user_id` (snake_case)
- This caused all Python-ingested facts (1,531 points) to be invisible to autoRecall

## Metadata
- **PR**: #157
- **Merged**: 2026-03-15
- **Author**: jleechan2015
- **Stats**: +311/-1 in 6 files
- **Labels**: none

## Connections
