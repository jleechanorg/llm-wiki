---
title: "jleechanclaw — Agento Proactive Recovery Design"
type: source
tags: [jleechanclaw, agent-orchestration, proactive-recovery, lifecycle, ao]
date: 2026-03-14
source_file: jleechanclaw/roadmap/AGENTO_PROACTIVE_RECOVERY_DESIGN.md
---

## Summary

Agento sessions require too much manual intervention. Four recurring failure modes drive this design: (1) sessions run for hours after PR merges, (2) killed/stuck sessions block respawn, (3) stuck sessions are abandoned after 3 nudges with no respawn action, (4) reactions fire for new events only — pre-existing review comments don't trigger bugbot on newly spawned sessions.

## Key Claims

### Failure Modes

| # | Symptom | Root Cause |
|---|---------|-----------|
| 1 | Sessions run for hours after PR merges | ao-backfill.sh only spawns, never stops |
| 2 | Killed/stuck sessions block respawn | Backfill skips PRs with any session, even dead ones |
| 3 | Stuck sessions abandoned after 3 nudges | AO has no `respawn` action; `requiresManualIntervention: true` is terminal |
| 4 | Reactions fire for new events only | Pre-existing review comments don't trigger bugbot-comments |

### Design Options Evaluated

**Option A — External scripts (ao-backfill.sh)** [Best for immediate fixes]
- Extend existing ao-backfill.sh to: cleanup merged PRs (`gh pr view --json state,merged` → `ao stop`), force respawn dead sessions older than 30min
- Pros: zero AO repo changes, fits 15-min cron cadence, easy to audit
- Cons: polling lag (up to 15min), brittle text parsing of `ao session ls`

**Option B — AO Plugin** [Right long-term, wrong for immediate]
- New `lifecycle-hook` plugin slot with `respawn` action
- Pros: clean integration, upstreamable to ComposioHQ
- Cons: plugins are statically compiled, requires TypeScript/npm fork work

**Option C — notifier-webhook → openclaw gateway** [Recommended for event-driven]
- AO already sends lifecycle events to `http://127.0.0.1:18800/ao-notify`. Gateway receives but ignores them.
- Implement handler: `AO lifecycle event → POST /ao-notify → openclaw handler → ao stop / ao spawn / alert`
- Events: `merge.completed` → `ao stop`, `reaction.escalated` (agent-stuck) → `ao spawn`

## Connections

- [[AgentStallRecovery]] — watchdog timers and recovery strategies
- [[AO-Daemon-Incident]] — documented WebSocket streaming daemon failure
- [[AO-Blocker-Matrix]] — 7-green PR criteria
- [[SessionManagement]] — session lifecycle, zombie detection
- [[OpenClaw]] — gateway handler for lifecycle events
