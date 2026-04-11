---
title: "PR #2116: Fix parallel request handling with ThreadPoolExecutor"
type: source
tags: []
date: 2025-11-27
source_file: raw/prs-worldarchitect-ai/pr-2116.md
sources: []
last_updated: 2025-11-27
---

## Summary
- Fixed blocking I/O serialization in asyncio routes by adding ThreadPoolExecutor
- Added `run_blocking_io()` helper to offload Firestore calls to thread pool
- Increased Cloud Run containerConcurrency from 10 to 80
- Executor threads set to 80 for maximum parallelism

## Metadata
- **PR**: #2116
- **Merged**: 2025-11-27
- **Author**: jleechan2015
- **Stats**: +2639/-132 in 28 files
- **Labels**: none

## Connections
