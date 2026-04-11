---
title: "PR #191: docs: post-ingest 5% recall results + userId/user_id mismatch finding"
type: source
tags: []
date: 2026-03-16
source_file: raw/prs-worldai_claw/pr-191.md
sources: []
last_updated: 2026-03-16
---

## Summary
- Adds post-ingest results to `testing_llm/mem0_feb_recall_baseline_20260315.md`
- 0/10 known recall after 5% Feb sample (268 Qdrant points)
- Root cause: random sample dominated by worldarchitect.ai sessions
- Found userId/user_id payload mismatch: 56 autoCapture facts invisible to search

## Metadata
- **PR**: #191
- **Merged**: 2026-03-16
- **Author**: jleechan2015
- **Stats**: +85/-10 in 3 files
- **Labels**: none

## Connections
