---
title: "PR #425: [agento] fix(core): address deferred bugs from PR #421 session-prefix work"
type: source
tags: []
date: 2026-04-11
source_file: raw/prs-worldai_claw/pr-425.md
sources: []
last_updated: 2026-04-11
---

## Summary
Follow-up to PR #421 addressing the two bugs deferred due to scope constraints.

### Fixes

**1. `isOrchestratorSessionRecord` ignores metadata role when prefix is set** (cursor #3063372527)

When `project.sessionPrefix` is set, `isOrchestratorSessionRecord` only checked session ID, not `raw["role"]`. A session with `role="worker"` but a matching ID pattern would be misclassified as orchestrator. Fix: add early return `if (raw["role"] === "worker") return false` so metadata role takes precedence

## Metadata
- **PR**: #425
- **Merged**: 2026-04-11
- **Author**: jleechan2015
- **Stats**: +4/-2 in 2 files
- **Labels**: none

## Connections
