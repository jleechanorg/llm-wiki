---
title: "PR #1824: fix: Guard httpx/a2a imports in A2A integration tests"
type: source
tags: []
date: 2025-10-03
source_file: raw/prs-worldarchitect-ai/pr-1824.md
sources: []
last_updated: 2025-10-03
---

## Summary
Fixes P1 critical issue identified in PR #60 code review: httpx and A2AClient were used without importing in `orchestration/tests/test_a2a_integration.py`, causing ModuleNotFoundError during pytest collection when A2A SDK dependencies are unavailable.

## Metadata
- **PR**: #1824
- **Merged**: 2025-10-03
- **Author**: jleechan2015
- **Stats**: +14/-2 in 2 files
- **Labels**: none

## Connections
