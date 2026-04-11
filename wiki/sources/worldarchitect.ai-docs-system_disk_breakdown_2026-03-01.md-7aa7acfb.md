---
title: "System Disk Breakdown Report (2026-03-01)"
type: source
tags: [disk-space, storage-analysis, cleanup, system-maintenance]
sources: []
source_file: docs/system_disk_breakdown_2026-03-01.md
date: 2026-03-01
last_updated: 2026-04-07
---

## Summary

System-wide disk usage analysis revealing 99.2% disk capacity used (986.4 GB of 994.7 GB). The /Users directory dominates at 94.6% of Data volume (882.2 GB), with ~/projects containing the largest consumption at 135 GB. Cleanup operations freed 151 GB total, primarily from harness worktrees (71 GB) and stale GitHub Actions workspaces (80 GB).

## Key Claims

- **99.2% Disk Usage**: APFS total 994.7 GB, used 986.4 GB — system near capacity
- **/Users Dominates**: 882.2 GB (94.6% of Data volume), far exceeding other top-level paths
- **Largest Consumers**: ~/projects (135 GB), ~/Library (99 GB), ~/projects_other (51 GB), ~/project_ai_universe (50 GB), ~/actions-runner (47 GB), ~/.codex (39 GB), ~/.cache (24 GB)
- **Docker & iMessage**: Docker (31 GB) and iMessage attachments (23 GB) are the largest ~/Library subdirectories
- **Harness Worktrees**: orch_worldarchitect.ai contained 73 GB across 274 harness* directories (~1 GB each)
- **Cleanup Impact**: Removed 71 GB from harness worktrees and 80 GB from stale GitHub Actions workspaces
- **Actions Runners**: Two runners consuming 89 GB combined (47 GB + 42 GB)

## Key Quotes

> "/Users dominates at ~94.6% of Data" — primary storage consumer location

> "orch_worldarchitect.ai: 73 GB | 274 harness* worktree dirs (~1 GB each)" — largest single directory consuming disk space

## Connections

- [[Blueplane Telemetry Core]] — local telemetry could help track disk usage patterns over time
- [[GitHub Development Statistics]] — Actions runners contributing to storage usage

## Contradictions

- None identified — this is a fresh system analysis report
