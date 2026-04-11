---
title: "PR #5384: Add passwordless clock sync for self-hosted runner auto-recovery"
type: source
tags: [infrastructure]
date: 2026-02-13
source_file: raw/prs-worldarchitect-ai/pr-5384.md
sources: []
last_updated: 2026-02-13
---

## Summary
Adds passwordless clock sync for self-hosted runner auto-recovery and reorganizes all runner-related content into a dedicated `self-hosted/` top-level directory.

**Problem**: After offline periods, runners with clock drift (+10min) cannot reconnect to GitHub:
1. Computer goes offline with clock +10min ahead
2. Runner loses connection to GitHub
3. Computer comes back online, runner tries to reconnect
4. GitHub validates token timestamp, sees future timestamp
5. GitHub rejects authentication → Ru

## Metadata
- **PR**: #5384
- **Merged**: 2026-02-13
- **Author**: jleechan2015
- **Stats**: +185/-24 in 8 files
- **Labels**: infrastructure

## Connections
