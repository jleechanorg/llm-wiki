---
title: "PR #4080: fix: Use modern Firestore count API to fix campaign list latency"
type: source
tags: []
date: 2026-01-26
source_file: raw/prs-worldarchitect-ai/pr-4080.md
sources: []
last_updated: 2026-01-26
---

## Summary
- Fixes campaign list API latency from ~1.2s to ~0.1s by using the correct Firestore count aggregation API
- Removes deprecated AggregationQuery class usage that was causing errors

## Metadata
- **PR**: #4080
- **Merged**: 2026-01-26
- **Author**: jleechan2015
- **Stats**: +27/-62 in 1 files
- **Labels**: none

## Connections
