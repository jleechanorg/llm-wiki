---
title: "Agent Orchestrator doctor.sh v2"
type: concept
tags: [doctor-sh, alerting, ao-doctor, ao-health, ao-update, monitoring, agent-orchestrator]
date: 2026-06-10
---

## Definition

**`doctor.sh` v2** is the proposed next-generation health-check and alerting script for the Agent Orchestrator system. It consolidates the three current scripts (`ao-doctor.sh`, `ao-doctor-monitor.sh`, `ao-health.sh`, `ao-update.sh`) into a single tiered observability surface with loud-WARN code-path integration, multi-channel alerting (Slack/email/desktop/tmux), and a 3-tier watchdog-of-watchdogs architecture. Targeted for `scripts/ao-doctor-v2.sh` + `scripts/ao-doctor-monitor-v2.sh` + new `ai.agento.health-guardian` launchd plist.

## Goals

1. **Detect silent-failure paths** — replace ad-hoc grep recipes (e.g., `grep -c "scm:" ~/.hermes/agent-orchestrator.yaml`) with structured checks
2. **Bound maximum blindness window** to 60 minutes via 3-tier watchdog chain
3. **Restore broken Slack alerting** — re-create `/Users/jleechan/.hermes/scripts/hermes-watchdog.sh` (30-line shim)
4. **Add 9 missing alerting channels** — Slack push, desktop notif, tmux status, PR auto-comment, bead auto-creation, etc.
5. **Add 17 new checks** for unmonitored signals identified in 2026-06-10 audit

## New Check Categories (17 unmonitored signals → checks)

| # | Check | Source signal | Severity |
|---|-------|---------------|----------|
| 1 | tmux pane alive but Claude Code process dead | tmux capture-pane shows prompt ❯ but no agent activity | FAIL |
| 2 | dist loaded in memory vs new dist on disk | md5sum `/Users/jleechan/bin/ao` vs `packages/cli/dist/index.js` | WARN |
| 3 | orchestrator-prompt cache staleness | grep for expected content in `~/.agent-orchestrator/*/orchestrator-prompt*.md` | WARN |
| 4 | pnpm global store version match | `pnpm store path` matches expected | WARN |
| 5 | git ENOENT inside forked process | grep `ao-health.log` for `spawn git ENOENT` | FAIL |
| 6 | running.json existence after reboot | `~/.agent-orchestrator/running.json` exists | WARN |
| 7 | AO_BOT_GH_TOKEN validity in env | `gh auth status` succeeds with the token | FAIL |
| 8 | scmFailureCount fleet aggregation | sum across all workers; > 10 = WARN | WARN |
| 9 | 24h age filter presence in skeptic-cron | grep for `updatedAt < ` in skeptic-cron-local.ts | INFO |
| 10 | paused project opt-out sentinel | no `~/.agent-orchestrator/paused/<projectId>` exists | INFO |
| 11 | backfillAllPRs default in new schemas | new project YAML has explicit `backfillAllPRs: false` | WARN |
| 12 | aging memory files claiming fixes | `git log -S <symbol>` returns 0 commits | WARN |
| 13 | Vitest OOM empty failed-count handling | ci.yml OOM recovery treats missing 'failed' as 0 | INFO |
| 14 | ZFC violations in new code | grep for `if (text.includes(` `, `\.match(`, `\.test(` in packages/ | WARN |
| 15 | compaction firing on skills/hooks | per-turn context bloat from UserPromptSubmit hook | INFO |
| 16 | auto-merge race with skeptic-cron | `enablePullRequestAutoMerge=false` for skeptic-managed repos | INFO |
| 17 | stale background monitor | monitor event handler gates on SHA match | INFO |

## Alerting Channels (9 to add)

| # | Channel | Rationale | Library |
|---|---------|-----------|---------|
| 1 | Slack push on silent skeptic returns | Direct visibility when `if (!scm?.listOpenPRs) return 0` fires | direct curl + SLACK_USER_TOKEN |
| 2 | Desktop notification on "running but broken" workers | `osascript -e 'display notification'` | macOS native |
| 3 | tmux status line for prompt/dist staleness | `set -g status-interval 30; set -g status-right ...` | tmux config |
| 4 | PR auto-comment when memory age > 30d claims a fix | `gh api PATCH` on PR with reactivation prompt | gh CLI |
| 5 | **bead auto-creation on fragility pattern detection** | would have caught bd-rgk0 automatically | br CLI |
| 6 | Terminal bell on chronic 0% rate automation | `printf '\a'` | shell escape |
| 7 | Slack/email digest of fragile areas | weekly summary with top patterns | cron + digest script |
| 8 | Per-project spawn storm alarm | >5 active sessions for a project = immediate `ao stop` recommendation | inotifywait-style poll |
| 9 | Health-check probe of `ao start` binary SHA | detect dist desync automatically | inline check |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ Tier 3: com.ao-runner-watchdog (1h)                          │
│   Watches: Tier 2 plist + log freshness                      │
│   Action: bootstrap Tier 2 if missing, Slack alert          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Tier 2: ai.agento.health-guardian (60 min)  [NEW]           │
│   Watches: Tier 1 plist + log freshness                      │
│   Action: bootstrap Tier 1 from scripts/frozen/, Slack alert │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Tier 1: ai.agento.health (5 min)  [EXISTING]                │
│   Watches: lifecycle workers, main repo, WAFER_API_KEY      │
│   Action: start missing workers, kill orphans               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Doctor Layer: ao doctor v2 (manual + cron + on-demand)      │
│   17 new checks above + auto-fix where possible             │
│   9 alerting channels                                       │
└─────────────────────────────────────────────────────────────┘
```

## Implementation Phases

**Phase 1 (1-2 days):** Restore broken `ai.hermes-watchdog` (30-line shim to recreate `/Users/jleechan/.hermes/scripts/hermes-watchdog.sh`). This alone restores the original prod-system Slack alerting path.

**Phase 2 (2-3 days):** Add the 17 new checks to `ao-doctor.sh` and `ao-doctor-monitor.sh`. Each check is a 10-30 line function with structured JSON output.

**Phase 3 (1-2 days):** Create `ai.agento.health-guardian` plist + script (Tier 2). Extend `com.ao-runner-watchdog` to also bootstrap Tier 2 (Tier 3 expansion).

**Phase 4 (1 day):** Add the 9 alerting channels. Each is a 20-50 line function with channel-specific config (Slack webhook, terminal-notifier path, etc.).

**Phase 5 (ongoing):** Add loud-WARN logs at every silent-failure guard in code paths. This is the durable fix — once operators can see WHEN the silent guard fires, they can fix the upstream cause.

## Backward Compatibility

- `ao doctor` CLI command stays as-is; the new checks are additive
- `ao doctor --fix` behavior is unchanged; new auto-fix capabilities are opt-in
- Existing launchd plists are not modified; only NEW plists are added (no removal of existing)
- The broken `ai.hermes-watchdog` is restored, not removed
- All existing memory entries (50+) remain valid; new checks are additive

## Related Concepts

- [SilentFailurePathPattern](SilentFailurePathPattern.md)
- [WatchdogOfWatchdogsArchitecture](WatchdogOfWatchdogsArchitecture.md)
- [OrchestrationSystemFragility](OrchestrationSystemFragility.md)
- [SLOAlerting](SLOAlerting.md)
- [Launchd](Launchd.md)

## Memory

- Source: `~/llm_wiki/raw/agent-orchestrator-fragility-2026-06-10.md`
- Source page: `~/llm_wiki/wiki/sources/agent-orchestrator-fragility-2026-06-10.md`
- Related: `feedback_2026-05-11_unified_health_launchd.md`
