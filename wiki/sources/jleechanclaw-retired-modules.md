---
title: "jleechanclaw-retired-modules"
type: source
tags: [jleechanclaw, deprecated, migration]
date: 2026-04-14
source_file: jleechanclaw/src/orchestration/retired-modules.md
---

## Summary
Multiple orchestration modules have been migrated to agent-orchestrator (AO). These modules now raise ImportError on import to fail loudly if any caller has not yet migrated. Each retired module documents its AO equivalent and migration path.

## Key Retired Modules

### session_registry.py
- Was: Session registry tracking
- AO equivalent: session-manager.ts
- Migration: `ao session ls` or `ao status`

### anomaly_detector.py
- Was: Anomaly detection and escalation monitoring
- AO equivalent: observability.ts / ao status
- Migration: Use `ao status` for session health; lifecycle-worker handles escalation monitoring

### escalation_router.py
- Was: Fork reaction handlers for escalation routing
- AO equivalent: fork-reaction-handlers.ts
- Migration: Use `reactions:` in agent-orchestrator.yaml

### action_executor.py
- Was: Action execution via reactions
- AO equivalent: fork-reaction-handlers.ts
- Migration: AO executes actions via send-to-agent reactions

### reviewer_agent.py
- Was: Review backlog management and review dispatch
- AO equivalent: review-backlog.ts + ao send
- Migration: AO dispatches review via review-requested reaction; use `ao send <session>` to communicate

### mctrl_status.py
- Was: Session status queries
- AO equivalent: ao session ls, ao status
- Migration: Use AO CLI for session status queries

### supervisor.py
- Was: Lifecycle worker management
- AO equivalent: ao lifecycle-worker command
- Migration: Run `ao lifecycle-worker <project>` (managed by launchd plist)

### gh_integration.py
- Was: GitHub integration for PR/intake workflows
- AO equivalent: scm-github plugin
- Migration: Use `gh` CLI directly or `ao` commands

### escalation.py
- Was: Escalation reaction handling
- AO equivalent: reactions config
- Migration: Use `reactions:` in agent-orchestrator.yaml

## Key Claims
- All retired modules raise ImportError to fail loudly on unmigrated callers
- Migration path always goes through agent-orchestrator
- Documentation lives in agent-orchestrator.yaml in this repo

## Connections
- [[jleechanclaw-pr-review-decision]] — active PR review module (not retired)
- [[jleechanclaw-merge-gate]] — deprecated but still functional stubs

## Contradictions
- None — migration is intentional and documented