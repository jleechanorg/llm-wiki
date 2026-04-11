---
title: "PR #320: [agento] fix: retire ao-pr-poller plist, add ao lifecycle-worker for agent-orchestrator"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldai_claw/pr-320.md
sources: []
last_updated: 2026-03-21
---

## Summary
Two beads identified during /auton diagnostic (2026-03-20):
- **orch-oox**: `ai.ao-pr-poller.plist` references the deprecated `scripts/ao-pr-poller.sh` shell script. The script was crashing (exit 32512 = command not found) on every 5-min invocation. The real PR polling mechanism is `ao lifecycle-worker` (npm binary) running via `com.agentorchestrator.lifecycle-*` launchd plists.
- **orch-ies**: No `com.agentorchestrator.lifecycle-agent-orchestrator` launchd plist existed. The 4 open PRs in `jlee

## Metadata
- **PR**: #320
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +4/-1 in 2 files
- **Labels**: none

## Connections
