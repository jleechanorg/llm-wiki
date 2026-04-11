---
title: "PR #5813: fix: cache context reclassification — eliminate double-billing + evidence quality"
type: source
tags: []
date: 2026-03-07
source_file: raw/prs-worldarchitect-ai/pr-5813.md
sources: []
last_updated: 2026-03-07
---

## Summary
- **Cache/provably-fair compatibility fix (REV-wvh)**: Provably fair seed moved from `system_instruction` to a prepended content part — system_instruction stays static and cacheable. Cache is **never disabled**
- **Silent cache disable eliminated (REV-8gz)**: Removed all `effective_cache_name = None` patterns in `gemini_provider.py` that silently killed cache in code_execution and native tool flows
- **Double-billing fix**: Old story entries were sent in both cache prefix ($0.05/M) AND live JSON

## Metadata
- **PR**: #5813
- **Merged**: 2026-03-07
- **Author**: jleechan2015
- **Stats**: +3855/-429 in 36 files
- **Labels**: none

## Connections
