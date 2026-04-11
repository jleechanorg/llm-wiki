---
title: "PR #388: refactor: centralize latency summary logging"
type: source
tags: [codex]
date: 2025-10-18
source_file: raw/prs-/pr-388.md
sources: []
last_updated: 2025-10-18
---

## Summary
- centralize latency summary logging in the shared LatencyTracker with structured summaries and context allowlisting
- update SecondOpinionAgent to record cost/token metrics consistently and delegate summary logging to the shared helper
- document the latency artifact path and new summary helper usage in backend and library READMEs

## Metadata
- **PR**: #388
- **Merged**: 2025-10-18
- **Author**: jleechan2015
- **Stats**: +216/-101 in 5 files
- **Labels**: codex

## Connections
