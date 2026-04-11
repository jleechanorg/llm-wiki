---
title: "PR #185: [agento] feat: config-driven bead task queue with maxConcurrent in lifecycle-worker"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-185.md
sources: []
last_updated: 2026-03-26
---

## Summary
Add a `taskQueue` config section to `agent-orchestrator.yaml` that lets users list beads to process with a concurrency limit. The lifecycle-worker drains the queue automatically: when an active session completes/merges, it spawns the next queued bead.

## Metadata
- **PR**: #185
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +605/-0 in 6 files
- **Labels**: none

## Connections
