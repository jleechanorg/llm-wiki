---
title: "Daily Bug Hunt"
type: concept
tags: [bug-hunt, daily, cron, multi-agent, parallel, github, slack, beads]
last_updated: 2026-03-26
sources: [jleechanclaw-orchestration-system-design, jleechanclaw-bug-hunt-20260326]
---

## Summary
The Daily Bug Hunt is a 9am Pacific weekday cron job that spawns 4 parallel AI agents (Codex, Cursor, Minimax, Gemini) to scan recently merged PRs for bugs. Each agent creates bug reports and beads for critical findings. A summary posts to Slack #bug-hunt channel, and OpenClaw is asked to fix critical bugs via agento.

## How It Works

```
9am weekdays (Pacific)
  → Get PRs merged in last 2 days from jleechanorg repos
  → Spawn 4 parallel agents (codex, cursor, minimax, gemini)
  → Each agent:
    - Reviews PRs for bugs
    - Creates bug_reports/*.md files
    - Creates beads for critical bugs
  → Post summary to #bug-hunt Slack channel
  → Ask OpenClaw to fix via agento
```

## Components

| Component | Path | Description |
|-----------|------|-------------|
| Bug hunt script | `scripts/bug-hunt-daily.sh` | Main orchestration script |
| Launchd plist | `launchd/ai.openclaw.schedule.bug-hunt-9am.plist` | macOS scheduler |
| OpenClaw cron | `daily-bug-hunt-9am-pacific` | Gateway cron job |
| Bug reports | `bug_reports/` | Output directory for bug reports |

## Repos Scanned
- `jleechanorg/jleechanclaw`
- `jleechanorg/worldarchitect.ai`
- `jleechanorg/ai_universe`
- `jleechanorg/beads`

## Bug Report Format

Each bug report includes:
- Repository and PR number
- File path and line number
- Bug description
- Severity (1-5)
- Suggested fix

Bugs are automatically converted to beads for tracking.

## Relationship to Orchestration System

The bug hunt is an application of the Autonomous Agent Loop pattern:
- Headless agents (Codex, Cursor, Minimax, Gemini) spawned in parallel
- Each agent gets fresh context (PR diff + codebase)
- Results aggregated and posted to Slack
- Critical bugs trigger AO session → agento dispatch for fix

## Why 4 Parallel Agents?

Different agents catch different bug patterns. Running 4 in parallel:
- Covers more PRs in the same time window
- Different model families catch different issue types
- First bug found by any agent is flagged; duplicates are deduplicated

## History

- 2026-03-26: 27 PRs reviewed, 0 bugs found across jleechanclaw and worldarchitect.ai
- Multiple recent jleechanclaw PRs were hygiene/quality fixes (harness changes, monitor improvements, thread fixes) with no bugs
- The `fix(bug-hunt)` PRs show the system has been iteratively improved (jq fail-closed, @openclaw escalation gating on positive bug count)

## Related Concepts
- [[MultiAgentBugScanning]]
- [[AutonomousAgentLoop]]
- [[ProactiveSessionRecovery]]