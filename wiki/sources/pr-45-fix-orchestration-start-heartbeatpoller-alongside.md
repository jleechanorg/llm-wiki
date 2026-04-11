---
title: "PR #45: fix(orchestration): start HeartbeatPoller alongside TaskPoller (ORCH-uti)"
type: source
tags: []
date: 2026-03-05
source_file: raw/prs-worldai_claw/pr-45.md
sources: []
last_updated: 2026-03-05
---

## Summary
- `run_service()` started `TaskPoller` but never `HeartbeatPoller` → agents were never registered in Mission Control
- Health check always showed ❌ for \"MC agents registered\"
- Fixes ORCH-uti

## Metadata
- **PR**: #45
- **Merged**: 2026-03-05
- **Author**: jleechan2015
- **Stats**: +585/-0 in 5 files
- **Labels**: none

## Connections
