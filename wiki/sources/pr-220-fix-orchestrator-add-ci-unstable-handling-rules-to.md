---
title: "PR #220: fix(orchestrator): add CI unstable handling rules to prevent agent stalls"
type: source
tags: []
date: 2026-03-16
source_file: raw/prs-worldai_claw/pr-220.md
sources: []
last_updated: 2026-03-16
---

## Summary
Add rules to SOUL.md (via agent-orchestrator.yaml) to prevent agents from stalling when CI is unstable:

### Changes

1. **CI Unstable / Failure — Act Immediately**: When  or any CI check shows FAILURE/in_progress:
   - Do NOT ask for permission. Do NOT wait.
   - Immediately run  to identify failing check
   - Then fix it with /copilot or direct code changes
   - This is a standing directive — never pause when CI is unstable

2. **Post-@coderabbitai Monitoring**: After posting :
   - Do NOT sto

## Metadata
- **PR**: #220
- **Merged**: 2026-03-16
- **Author**: jleechan2015
- **Stats**: +42/-0 in 2 files
- **Labels**: none

## Connections
