---
title: "PR #386: fix(P0/P1): agent-exited respawn guard + bug-hunt jq fail-closed"
type: source
tags: []
date: 2026-03-24
source_file: raw/prs-worldai_claw/pr-386.md
sources: []
last_updated: 2026-03-24
---

## Summary
Two bugs identified via post-merge review of PRs from the last 3 days:
- **orch-t63 (P0)**: PR #354 introduced `agent-exited` → `send-to-agent` reaction with no `retries`/`escalateAfter` guard, creating unbounded respawn loops
- **orch-pwo (P1)**: PR #378 introduced `jq` parsing of AO spawn output that silently drops bug findings on parse failure

## Metadata
- **PR**: #386
- **Merged**: 2026-03-24
- **Author**: jleechan2015
- **Stats**: +15/-4 in 2 files
- **Labels**: none

## Connections
