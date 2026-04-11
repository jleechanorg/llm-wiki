---
title: "PR #519: fix: prefer port 2000 when running local server"
type: source
tags: [codex]
date: 2025-11-03
source_file: raw/prs-/pr-519.md
sources: []
last_updated: 2025-11-03
---

## Summary
- update run_local_server.sh to probe port 2000 before launching and set environment hints when it is unavailable
- allow the run-local-server TypeScript helper to honor preferred or minimum port overrides when selecting a port

## Metadata
- **PR**: #519
- **Merged**: 2025-11-03
- **Author**: jleechan2015
- **Stats**: +210/-52 in 2 files
- **Labels**: codex

## Connections
