---
title: "PR #2161: feat: Centralize 100-thread executor for blocking I/O operations"
type: source
tags: []
date: 2025-11-28
source_file: raw/prs-worldarchitect-ai/pr-2161.md
sources: []
last_updated: 2025-11-28
---

## Summary
- Centralizes ThreadPoolExecutor configuration in infrastructure/executor_config.py
- Increases concurrent thread capacity from 80 to **100 workers**
- Configures asyncio default executor so asyncio.to_thread() calls in world_logic.py automatically use the shared pool

## Metadata
- **PR**: #2161
- **Merged**: 2025-11-28
- **Author**: jleechan2015
- **Stats**: +381/-7 in 4 files
- **Labels**: none

## Connections
