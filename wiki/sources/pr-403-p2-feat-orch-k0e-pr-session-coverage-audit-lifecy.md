---
title: "PR #403: [P2] feat(orch-k0e): PR session coverage audit + lifecycle-worker diagnostic skill"
type: source
tags: []
date: 2026-03-27
source_file: raw/prs-worldai_claw/pr-403.md
sources: []
last_updated: 2026-03-27
---

## Summary
- `scripts/audit-pr-session-coverage.sh`: cross-references open PRs with active AO sessions, claims orphaned PRs (no session, stale >1h), posts Slack summary. Idempotent — safe for cron.
- `skills/diagnose-lifecycle-worker.md`: guided triage skill for `claim_failed` loops. Covers ghost worktrees, wrong main-branch state, orphaned session metadata. Escalation path via MCP mail.

## Metadata
- **PR**: #403
- **Merged**: 2026-03-27
- **Author**: jleechan2015
- **Stats**: +685/-2 in 5 files
- **Labels**: none

## Connections
