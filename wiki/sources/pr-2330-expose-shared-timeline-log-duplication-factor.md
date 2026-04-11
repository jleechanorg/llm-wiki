---
title: "PR #2330: Expose shared timeline log duplication factor"
type: source
tags: [codex]
date: 2025-12-09
source_file: raw/prs-worldarchitect-ai/pr-2330.md
sources: []
last_updated: 2025-12-09
---

## Summary
- move `TIMELINE_LOG_DUPLICATION_FACTOR` to module scope in `llm_service` for reuse
- update the timeline log budget end-to-end test to import the shared constant and clean up imports
- use the shared duplication factor throughout the test output to stay aligned with the production value

## Metadata
- **PR**: #2330
- **Merged**: 2025-12-09
- **Author**: jleechan2015
- **Stats**: +402/-286 in 1 files
- **Labels**: codex

## Connections
